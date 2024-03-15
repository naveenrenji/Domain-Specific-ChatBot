import openai
import re

openai.api_key = "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"
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
        "content": "You are a engineering design expert who will score the provided washing machine desgin description with a score ranging for 1 ( not at all novel engineering design description for a washing machine ) to 5 ( a completely novel idea for a washing machine engineering design). Analyse based on engineering novelty on washing machines. You will only respond with a number between 1 to 5 and nothing else at all."
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
