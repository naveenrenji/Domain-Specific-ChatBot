import openai
import re

openai.api_key = "apikey"
conversation_history = []

def novelty_score(description):
    global conversation_history
    
    conversation_history.append({
        "role": "user",
        "content": f"Design Description : {description}"
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    system_message = {
        "role": "system",
        "content": """You are an engineering design expert tasked with evaluating a provided washing machine design description, scoring its novelty on a scale from 1 (not at all novel) to 5 (highly novel). Assess the novelty based on the following criteria:

Uniqueness: If the design presents an idea that is not commonly implemented or discussed in current washing machines, it is considered novel.

Innovation: If the design introduces a fundamental change in how a washing machine operates, cleans, or interacts with users, it is deemed novel.

Technological Advances: If the design involves the introduction of new technology or an innovative application of existing technology in a manner not previously seen in washing machines, it is considered novel.

User Experience: If the design offers a significantly new and different user experience compared to existing washing machines, it can be viewed as novel.

Environmental Impact: If the design proposes a new method for saving energy or reducing waste, it qualifies as novel.

Your response should be a single number between 1 and 5, reflecting your assessment of the design's novelty based on these criteria. Please provide only this number as your response, with no additional text.
"""
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

# description = "A washing machine that is engineered to reuse water used my collecting it and filtering the water to remove impurtities and bacteria using UV and charcoal filters"
# print(novelty_score(description))

# description = "A washing machine that uses nuclear power to run"
# print(novelty_score(description))
