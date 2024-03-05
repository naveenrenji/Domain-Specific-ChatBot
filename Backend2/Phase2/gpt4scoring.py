import openai

openai.api_key = "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"
conversation_history = []

def response_generator(description):
    global conversation_history
    
    conversation_history.append({
        "role": "user",
        "content": f"Design Description : {description}"
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    system_message = {
        "role": "system",
        "content": "You are a engineering design expert who will score the provided washing machine desgin description with a score ranging for 1 ( not at all novel engineering design description for a washing machine ) to 5 ( a cmpletely novel idea for a washing machine engineering design). You will only respond with a number between 1 to 5 and nothing else at all."
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
    
    # Extract the response text
    response_text = response['choices'][0]['message']['content'].strip()
    
    # Append the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })

    # Ensure that only the last 5 messages are kept after the response is added
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    return response_text

# Example usage:
description = "A washing machine that is engineered to reuse water used my collecting it and filtering the water to remove impurtities and bacteria using UV and charcoal filters"

print(response_generator(description))
