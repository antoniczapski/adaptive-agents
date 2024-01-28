from flask import jsonify
from openai import OpenAI
import chromadb
import numpy as np
import chromadb.utils.embedding_functions as embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key='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',
    model_name="text-embedding-ada-002"
)

chroma_client = chromadb.PersistentClient(path=".")
collection = chroma_client.get_collection(name="sample_collection", embedding_function=openai_ef)

def process_query(prompt):
    closest_documents = collection.query(
        query_texts=[prompt],
        n_results=3
    )
    return '\n\n'.join([f'{metadata["title"].strip()}\n{metadata["description"].strip()}\n{metadata["url"].strip()}' for metadata in closest_documents['metadatas'][0]])
     
if __name__ == '__main__':
    message = "I need to analyse PDFs"

    closest_documents = collection.query(
        query_texts=[message],
        n_results=3
    )

    for i, (usage_scenarion, metadata) in enumerate(zip(closest_documents['documents'][0], closest_documents['metadatas'][0])):
        print(f'{i+1}-th closest tool: {metadata["title"]}')
        print(usage_scenarion)
        print(metadata)
        print()
