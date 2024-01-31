import chromadb
import chromadb.utils.embedding_functions as embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key='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',
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path="./extended")
collection = chroma_client.get_collection(name="sample_collection", embedding_function=openai_ef)

def process_query(prompt):
    user_needs = prompt.split('\n')
    metadatas = []
    usage_scenarios = []
    for user_need in user_needs:
        closest_documents = collection.query(
            query_texts=[user_need],
            n_results=1
        )
        metadatas.append(closest_documents['metadatas'][0][0])
        usage_scenarios.append(closest_documents['documents'][0][0])
    response = []
    for metadata,usage_scenario in zip(metadatas,usage_scenarios):
        try:
            response.append(f"""TITLE: {metadata['title']}
DESCRIPTION: {metadata['description']}
URL: https://chat.openai.com/g/g-{metadata['url']}
USAGE SCENARIO: {usage_scenario}""")
        except:
            pass
    if not response:
        return "No AI tool found."
    return '\n\n'.join(response)

if __name__ == '__main__':
    user_needs = '- help with amazon account \n - improve SEO of my products \n - generate impresive icons for my website'
    user_needs = 'I need help with SEO.\n I need help with Amazon setup.\n I need help with icon generation.'
    response = process_query(user_needs)
    print(response)
    # print(chroma_client.list_collections())
    # closest_documents = collection.query(
    #     query_texts=[message],
    #     n_results=3
    # )

    # for i, (usage_scenarion, metadata) in enumerate(zip(closest_documents['documents'][0], closest_documents['metadatas'][0])):
    #     print(f'{i+1}-th closest tool: {metadata["title"]}')
    #     print(usage_scenarion)
    #     print(metadata)
    #     print()
