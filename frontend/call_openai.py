from openai import OpenAI

client = OpenAI(
    api_key='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',
)

def preprocess_messages(messegas):
    preprocessed_messages = [{'role':message['sender'], 'content':message['message']} for message in messegas]
    if preprocessed_messages[0]['role'] != 'system':
        preprocessed_messages.insert(0, {'role':'system', 'content': 'You are a semantic parser. Your job is to write a list of user needs based on the context it provides.'})
    return preprocessed_messages

def call_openai(messages, context):
    if context:
        messages.append({'role':'system','content':context})
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
        response = "**error - no response from openai**"
    return response

if __name__ == '__main__':
    messages = [{'sender': 'User', 'message': 'Hello! I will have seminar session at my university next week. I will present the topic of cancer treatment in cats. Could you help me with preparing to this task?'}]
    r = preprocess_messages(messages)
    print(r)