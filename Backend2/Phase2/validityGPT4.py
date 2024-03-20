import openai
import re

openai.api_key = "apikey"
conversation_history = []

def validity_score(description):
    global conversation_history
    
    conversation_history.append({
        "role": "user",
        "content": f"Design Description : {description}"
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    system_message = {
        "role": "system",
        "content": "You are an engineering design expert tasked with evaluating a provided description related to a washing machine. Your role is to determine if the description focuses on a part, feature, or function that is directly related to the washing machine's core operations, such as washing, rinsing, spinning, drying clothes, energy, smartness, features or user interaction.  If the description pertains to these aspects, it is considered to be describing the engineering design of a washing machine, Even if it they are far fetched, as long as it is talking about a washing machine, it is valid. Your response should be a numerical score: use 1 to indicate the description is relevant to the engineering design of a washing machine, and 0 if it is not. Please provide only the number as your response, with no additional text."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[system_message] + conversation_history,
        temperature=1,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    
    response_text = response['choices'][0]['message']['content'].strip()
    
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    numbers = re.findall(r'\d+', response_text)
    return int(numbers[0]) if numbers else 1

# description = "A racecar that is engineered to reuse water used my collecting it and filtering the water to remove impurtities and bacteria using UV and charcoal filters"

# print(validity_score(description))
