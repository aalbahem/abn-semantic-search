from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer


def get_encoder(model_name="intfloat/e5-small-v2"):
    return SentenceTransformer(model_name)

import streamlit as st

def get_clinet():
    client = OpenSearch('http://localhost:9200', http_auth=('admin', 'opensearch-ABN-ameer-2024!'), use_ssl=True,
                        verify_certs=False, ssl_assert_hostname=False,
                        ssl_show_warn=False)
    return client

def embedding_search(search, encoder):
    search_embedding = encoder.encode("query:"+search)
    client = get_clinet()
    query_embeddings = search_embedding.tolist()
    body ={
        "size": "10",
      "query": {
            "knn": {
                "company_embeddings": {
                    "vector": query_embeddings,
                    "k": 10
                }
            }
        }
    }
    response = client.search(index='abn',body=body)
    return response['hits']['hits']

def keyword_search(search):
    client = get_clinet()
    body = {
        "id":"company_keyword_search_template",
        "params": {
            "company_name": search
        }
    }
    response = client.search_template(index='abn', body=body)
    return response['hits']['hits']
def main():
    st.title('Search Australian Business Register')
    search = st.text_input('Enter search words:')

    if st.button('Search'):
        col1, col2 = st.columns(2)

        with col1:
            st.header("Keyword Search")
            search_results = keyword_search(search)
            if len(search_results) == 0:
              st.write("No results found")
            for result in search_results:
                c = st.container(border=True)
                company_name = result['_source'].get('company_name', 'N/A')
                state = result['_source'].get('state', 'N/A')
                c.write(f"Company: {company_name}")
                c.write(F"State: {state}")

        with col2:
            st.header("Embedding Search")
            encoder = get_encoder()
            search_results = embedding_search(search,encoder)
            if len(search_results) == 0:
              st.write("No results found")
            for result in search_results:
                c = st.container(border=True)
                company_name = result['_source'].get('company_name', 'N/A')
                state = result['_source'].get('state', 'N/A')
                c.write(f"Company: {company_name}")
                c.write(F"State: {state}")

if __name__ == '__main__':
    main()