import json
from openai import OpenAI
from tqdm import tqdm
import tiktoken
from time import sleep
import random
import numpy as np
import pandas as pd

def prompt_template(description):
    messages = \
    [
        {
        "role": "system",
        "content": "You are providing generic applications of the AI tool based on its description. The answer should be an enumerated list of use cases - up to three items. Items in list should be laconic and formal, eg, 'makes presentations' and 'teaches new language'. Cut the overexaggerated parts of descriptions"
        },
        {
        "role": "user",
        "content": "Tutor Me - Your personal AI tutor by Khan Academy! I'm Khanmigo Lite - here to help you with math, science, and humanities questions. I won’t do your work for you, but I will help you learn how to solve them on your own. Can you tell me the problem or exercise you’d like to solve?"
        },
        {
        "role": "assistant",
        "content": "1. Assisting with math problems\n2. Providing explanations for science questions\n3. Offering guidance on humanities topics"
        },
        {
        "role": "user",
        "content": "CANVA - Effortlessly design anything: presentations, logos, social media posts and more."
        },
        {
        "role": "assistant",
        "content": "1. Creating presentations\n2. Designing logos\n3. Generating social media content"
        },
        {
        "role": "user",
        "content": description
        }
    ]
    return messages, sum([len(encoding.encode(message['content'])) for message in messages])


def analyse_description(description, max_tries=3):
    if max_tries == 0:
        return [], 0
    
    sleep(0.4)

    global total_token_count_prompt
    global total_token_count_response

    messages, prompt_tokens = prompt_template(description)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = response.choices[0].message.content
    except:
        response = []

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
    
    return [line[3:] for line in response], max_tries

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
    # read data from data_small.csv into pandas dataframe
    df = pd.read_csv('database_initialization/data_extended/data_small.csv')
    df = df.dropna()

    data = []
    # structure: gpt_id,name,description
    for _, row in tqdm(df.iterrows()):
        full_description = row['name'] + ' - ' + row['description']
        use_cases, max_tries = analyse_description(full_description)

        print("full_description:", full_description)
        print("use_cases:", use_cases)
        print(f"attempts: {3-max_tries}")
        print()

        if not use_cases:
            continue
        data.append({
            'title': row['name'],
            'description': row['description'],
            'url': row['gpt_id'],
            'usage_scenarion': use_cases,
        })

    print(f"Prompt token count: {total_token_count_prompt} ~ {total_token_count_prompt / 1000000}$")
    print(f"Response token count: {total_token_count_response} ~ {total_token_count_response / 500000}$")
    print(f"Total cost: {(total_token_count_prompt / 1000000) + (total_token_count_response / 500000)}")

    with open('database_initialization/data_extended/preprocessed_small.json', 'w') as f:
        json.dump(data, f, indent=4)