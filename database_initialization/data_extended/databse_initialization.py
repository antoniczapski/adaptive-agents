import json
from tqdm import tqdm
from openai import OpenAI
import tiktoken
import chromadb
import numpy as np
import chromadb.utils.embedding_functions as embedding_functions

def get_embedding(usage_scenarios):
    if not usage_scenarios:
        return [], 0
    embedding = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=usage_scenarios,
            encoding_format="float"
        )
    return embedding.data[0].embedding, embedding.usage.prompt_tokens

if __name__=='__main__':
    # setup
    openai_client = OpenAI(
        api_key='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',
    )

    # loading data
    with open('database_initialization/data_extended/preprocessed.json','r',encoding='utf-8') as f:
        data = json.load(f)

    # database initialization
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key='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',
        model_name="text-embedding-3-small"
    )

    chroma_client = chromadb.PersistentClient(path="./backend/extended")
    collection = chroma_client.create_collection(name="sample_collection",embedding_function=openai_ef)
    
    total_token_count_embedding = 0
    

    for id, sample in tqdm(enumerate(data)):
        try:
            embedding, embedding_tokens = get_embedding('\n'.join(sample['usage_scenarion']))
            total_token_count_embedding += embedding_tokens
        except:
            continue
        if len(embedding) == 0:
            continue
        collection.add(
            embeddings=[embedding],
            documents=['\n'.join(sample['usage_scenarion'])],
            metadatas=[{
                "title": sample['title'],
                "url": sample['url'],
                "description": sample['description']
                }],
            ids=[sample['url']]
        )

    print(f"Embedding token count: {total_token_count_embedding} ~ {0.00013 * total_token_count_embedding / 1000}$")