from flask import Flask, render_template, url_for, request, jsonify
from datetime import datetime 
import requests
import json
from collections import defaultdict as dd
import os

from call_openai import call_openai, preprocess_messages


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        messages = request.get_json()
        messages = preprocess_messages(messages)
        context = perform_actions(messages)
        response = call_openai(messages,context)
        return jsonify(response)
    except Exception as e:
        app.logger.error(f'Error in run_script: {e}')
        raise e
    
def perform_actions(messages):
    available_actions = get_actions()
    actions_to_perform = choose_actions(available_actions,messages)
    actions_outputs = dd(list)
    for action_type, actions in actions_to_perform.items():
        for action_description, argument, *args in actions:
            if action_type == 'API Call':
                actions_outputs['API Call'] += [(action_description, argument, api_call(argument, args))]
            elif action_type == 'Web Browsing':
                actions_outputs['Web Browsing'] += [(action_description, argument, web_browsing(argument, args))]
            elif action_type == 'DALL-E Image Generation':
                actions_outputs['DALL-E Image Generation'] += [(action_description, argument, dall_e_image_generation(argument, args))]
            elif action_type == 'Code Interpreter':
                actions_outputs['Code Interpreter'] += [(action_description, argument, code_interpreter(argument, args))]
            elif action_type == 'File Search':
                actions_outputs['File Search'] += [(action_description, argument, database_query(argument, args))]
    
    context = "\nFollowing actions were performed in order to provide context for the response:\n<ACTIONS>"
    nl = '\n'
    for action_type, action in actions_outputs.items():
        for action_description, argument, response in action:
            context += f"""
    <{action_type}>
        <action_description>
            {action_description.strip()}
        </action_description>
        <argument>
            {argument.strip()}
        </argument>
        <response>
            {f'{nl}            '.join(response.split(nl))}
        </response>
    </{action_type}>
"""
    context += "</ACTIONS>\n"
    return context

def api_call(message, *args):
    url = args[0][0]
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json={"prompt": message})
        return response.json()['message']
    except Exception as e:
        app.logger.error(f'Error in call_backend: {e}')
        raise e

def web_browsing(action_description, *args):
    raise NotImplementedError

def dall_e_image_generation(action_description, *args):
    raise NotImplementedError

def code_interpreter(action_description, *args):
    raise NotImplementedError

def database_query(action_description, *args):
    raise NotImplementedError

def choose_actions(available_actions, messages):
    # Choose actions to perform
    # Based on available actions and user need create a dictionary
    # of pairs (action, arguments) to perform. It should be done by
    # samo kind of GPT model
    # 
    actions_dict = dd(list)
    for action_type, actions in available_actions.items():
        for action_description, *args in actions:
            is_needed = is_this_action_needed(action_description, messages)
            if is_needed:
                argument = what_arguments_should_be_passed(action_description, messages)
                actions_dict[action_type] += [(action_description, argument, *args)]
    return actions_dict

def is_this_action_needed(action_description, messages):
    # NOT IMPLEMENTED YET
    # 
    # Based on user need and task description decide if this action
    # should be performed (True) or not (False) - done by some kind
    # of GPT model
    return True

def what_arguments_should_be_passed(action_description, messages):
    prompt = f"""
Here is an action that you should use to get more insights:
<action_describtion>
    {action_description}
</action_describtion>
Provide argument for this action inside tags <arg> </arg>. For example:
<arg> lorem ipsum dolor... </arg>

Your message have to contain only information about the argument, nothing else."""
    argument = call_openai(messages.copy(), prompt)

    retries = 3
    while not argument.startswith('<arg>') or not argument.endswith('</arg>'):
        if retries == 0:
            raise ValueError(f"Action argument should be in the form <arg> argument </arg>, yet bot provided:\n{argument}")
        retries -= 1
        argument = call_openai(messages.copy(), prompt)
    return argument.replace('<arg>','').replace('</arg>','').strip()

def get_actions():
    # Get from frontend list of actions
    # NOT IMPLEMENTED YET
    file_path = os.path.join(app.static_folder, 'action_desc.txt')
    with open(file_path, 'r') as file:
        action_desc = file.read()
    return dd(list,{'API Call':[(action_desc, 'http://backend:5000/echo')]})

if __name__ == '__main__':
    # frontend
    app.run(host='0.0.0.0', port=5001, debug=True)