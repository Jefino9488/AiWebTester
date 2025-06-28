import os
import re
import google.generativeai as genai
import faiss
import numpy as np
from lxml import etree, html as lxml_html


class AiFinder:
    def __init__(self, config):
        api_key = config['gemini']['api_key']
        if not api_key or api_key == "YOUR_GEMINI_API_KEY":
            raise ValueError("Gemini API key is not configured in config.json")
        genai.configure(api_key=api_key)
        self.embedding_model = 'models/embedding-001'
        self.generative_model = genai.GenerativeModel(config['gemini']['model_name'])

    def _clean_html(self, page_source):
        try:
            tree = lxml_html.fromstring(page_source)
            for tag in ['script', 'style', 'meta', 'link', 'head']:
                for element in tree.xpath(f'//{tag}'):
                    element.getparent().remove(element)

            comments = tree.xpath('//comment()')
            for comment in comments:
                comment.getparent().remove(comment)

            body_node = tree.find('.//body')
            if body_node is not None:
                cleaned_html = etree.tostring(body_node, pretty_print=True, method='html').decode('utf-8')
            else:
                cleaned_html = etree.tostring(tree, pretty_print=True, method='html').decode('utf-8')

            return cleaned_html
        except Exception:
            return re.sub(r'<script.*?</script>|<style.*?</style>', '', page_source, flags=re.DOTALL)

    def _chunk_html(self, cleaned_html, chunk_size=1000, overlap=200):
        lines = cleaned_html.split('\n')
        chunks = []
        current_chunk = ""
        for line in lines:
            if len(current_chunk) + len(line) > chunk_size:
                chunks.append(current_chunk)
                current_chunk = current_chunk[-overlap:] + line + '\n'
            else:
                current_chunk += line + '\n'
        if current_chunk:
            chunks.append(current_chunk)
        return [chunk for chunk in chunks if chunk.strip()]

    def _create_vector_store(self, chunks):
        if not chunks:
            return None, None

        result = genai.embed_content(
            model=self.embedding_model,
            content=chunks,
            task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings = result['embedding']

        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        return index, chunks

    def _search_vector_store(self, index, query_embedding, k=5):
        distances, indices = index.search(np.array([query_embedding]).astype('float32'), k)
        return indices[0]

    def _get_locator_from_llm(self, query, context_chunks):
        context = "\n---\n".join(context_chunks)
        prompt = f"""
        Based on the user query and HTML context, generate a robust and unique XPath locator for the described web element.
        Important: Always quote attribute values in single quotes.
        Return ONLY the XPath string. Do not add any explanation, quotes, or markdown formatting.
        Example format: //input[@id='username' and @type='text']

        User Query: "{query}"

        HTML Context:
        ```html
        {context}
        ```

        XPath:
        """
        try:
            response = self.generative_model.generate_content(prompt)
            xpath = response.text.strip().replace('`', '').replace('"', "'")
            if xpath.lower().startswith("xpath="):
                xpath = xpath.split("=", 1)[1].strip()
            return xpath
        except Exception as e:
            print(f"Error generating content from LLM: {e}")
            return None

    def find_element_locator(self, driver, query):
        page_source = driver.page_source
        cleaned_html = self._clean_html(page_source)
        html_chunks = self._chunk_html(cleaned_html)

        if not html_chunks:
            return None

        vector_index, chunks = self._create_vector_store(html_chunks)
        if vector_index is None:
            return None

        query_embedding_result = genai.embed_content(
            model=self.embedding_model,
            content=query,
            task_type="RETRIEVAL_QUERY"
        )
        query_embedding = query_embedding_result['embedding']

        top_indices = self._search_vector_store(vector_index, query_embedding, k=min(5, len(chunks)))
        context_chunks = [chunks[i] for i in top_indices]

        locator = self._get_locator_from_llm(query, context_chunks)
        return locator