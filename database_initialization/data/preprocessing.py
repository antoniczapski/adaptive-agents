import json
from openai import OpenAI
from tqdm import tqdm
import tiktoken
from time import sleep
import random
import numpy as np

def prompt_template(description):
    messages = \
    [
        {
        "role": "system",
        "content": "You are providing generic applications of the AI tool based on its description. The answer should be an enumerated list of use cases - up to three items. Items in list should be laconic and formal, eg, 'makes presentations' and 'teaches new language'. Cut the overexaggerated parts of descriptions"
        },
        {
        "role": "user",
        "content": "Go! for personalized workout plans, fitness tips, and meal recommendations."
        },
        {
        "role": "assistant",
        "content": "1. Creating personalized workout plans\n2. Providing fitness tips\n3. Offering meal recommendations"
        },
        {
        "role": "user",
        "content": "Turn any response into a useful video in seconds! Plus, easily edit and customize your video."
        },
        {
        "role": "assistant",
        "content": "1. Generating videos from text or data\n2. Streamlining video editing and customization\n3. Automating video production processes"
        },
        {
        "role": "user",
        "content": description
        }
    ]
    return messages, sum([len(encoding.encode(message['content'])) for message in messages])


def analyse_description(description, max_tries=3):
    if max_tries == 0:
        return []
    
    sleep(0.4)

    global total_token_count_prompt
    global total_token_count_response

    messages, prompt_tokens = prompt_template(description)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        response = response.choices[0].message.content
    except:
        response = ""

    total_token_count_prompt += prompt_tokens
    total_token_count_response += len(encoding.encode(response))

    response = response.split('\n')
    if len(response) > 3:
        print(f"Tries: {max_tries}, description: {' '.join(description.split())}\nResponse:\n{response}\n\n")
        return analyse_description(description, max_tries=max_tries-1)

    for line in response:
        if not line or not line[0].isdigit() or line[1] != '.':
            print(f"Tries: {max_tries}, description: {' '.join(description.split())}\nResponse:\n{response}\n\n")
            return analyse_description(description, max_tries=max_tries-1)
    
    return [line[3:] for line in response]

if __name__ == "__main__":
    # setup
    random.seed(42)

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")

    total_token_count_prompt = 0
    total_token_count_embedding = 0
    total_token_count_response = 0

    client = OpenAI(
        api_key='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',
    )

    # preprocessing
    with open('database_initialization/data/raw.json','r',encoding='utf-8') as f:
        data = json.load(f)
        data = random.sample(data, 100)

        for sample in tqdm(data):
            # creating usage scenarios
            try:
                sample['usage_scenarion'] = analyse_description(sample['description'])
            except:
                sample['usage_scenarion'] = []

    print(f"Prompt token count: {total_token_count_prompt} ~ {total_token_count_prompt / 1000000}$")
    print(f"Response token count: {total_token_count_response} ~ {total_token_count_response / 500000}$")
    print(f"Total cost: {(total_token_count_prompt / 1000000) + (total_token_count_response / 500000)}")

    with open('database_initialization/data/preprocessed.json', 'w') as f:
        json.dump(data, f, indent=4)