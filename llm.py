from openai import OpenAI
from datetime import datetime
import requests, json
import os

openai_api_key = os.environ.get('OPENAI_API_KEY')
assemblyai_api_key = os.environ.get('ASSEMBLYAI_API_KEY')

client = OpenAI(
    api_key=openai_api_key,
)

with open('menu.txt', 'r') as f:
    menu_items = f.read() #.split('\n')

def chat(text):
    # text = "Number 16, pint. It's one ton soup."
    now = datetime.now()
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f'''You are an dilligent spell checker. You will read food orders I give you in <order></order> brackets and correct the spelling of the menu items. I will give you the name of the menu item and their correct spellings. You will return original order with the fixed spelling. If there are no mispellings, return the order sentence verbatim.

                    To help you I will point out the low confidence words in the sentence by surround them with brackets [ ].
                    
                    <menu_items>
                    {menu_items}
                    </menu_items>
                    ''',
                },
                {
                    "role": "user",
                    "content": f"<order>Number 16, pint. It's one ton soup.</order>", 
                },
                {
                    "role": "assistant",
                    "content": f"Number 16, pint. It's wonton soup.",
                },
                {
                    "role": "user",
                    "content": f"<order>{text}</order>",
                },
            ],
            model="gpt-3.5-turbo",
            timeout=60,
        )
        # print(datetime.now() - now)
        return chat_completion.choices[0].message.content
    except Exception as e:
        return text

def complete(text):
    # text = "Number 16, pint. It's one ton soup."
    
    completion = client.completions.create(
        prompt= f'''Analyze the following text for menu item misspellings. Compare the text with this list of correctly spelled menu items:
        {menu_items}

        Text to check: {text}

        If any menu item is misspelled in the text, list the misspellings in a comma-separated format. If there are no misspellings, respond with "none".''',
        model="text-davinci-003"
    )
    return completion.choices[0].text

def lemur(text):
    url = "https://api.assemblyai.com/lemur/v3/generate/task"

    headers = {
        "authorization": assemblyai_api_key,
    }

    payload = {
        "input_text": f"<order>{text}</order>",
        "prompt": f'''You are an dilligent spell checker. You will read food orders I give you in <order></order> tags and correct the spelling of the menu items. I will give you the name of the menu item and their correct spellings. You will return original order with the fixed spelling. If there are no mispellings, return the order sentence verbatim.

                To help you I will point out the low confidence words in the sentence by surround them with brackets [ ].
                
                <menu_items>
                {menu_items}
                </menu_items>
        ''',
        "final_model": "basic"
    }

    response = requests.post(url, json=payload, headers=headers)
    # print(json.dumps(payload, indent=4))
    # print(response.json())
    # print(response.headers)
    return response.json()['response']

# start = datetime.now()
# response = chat()
# end = datetime.now()
# print(response)
# print(end - start)

# start = datetime.now()
# response = lemur('And then Number 34 Beef Lomaine.')
# end = datetime.now()
# print(response)
# print(end - start)
