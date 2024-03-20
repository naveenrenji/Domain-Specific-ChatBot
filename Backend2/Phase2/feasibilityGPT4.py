import openai
import re
openai.api_key = "apikey"
conversation_history = []

def feasibility_score(description):
    global conversation_history
    
    conversation_history.append({
        "role": "user",
        "content": f"Design Description : {description}"
    })

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    system_message = {
        "role": "system",
        "content": """You are an engineering design expert tasked with evaluating a provided washing machine design description, scoring its feasibility on a scale from 1 (not at all feasible) to 5 (highly feasible). Assess the feasibility based on the following factors:

Technological Feasibility: Is the required technology for the idea currently available or easily developed?

Economic Feasibility: Consider the implementation costs and whether the potential price increase is acceptable to consumers.

User Acceptance: Evaluate if the feature is user-friendly and adds significant value to warrant its inclusion.

Manufacturing Complexity: Can existing manufacturing processes accommodate the new feature, or is a new process necessary?

Regulatory Hurdles: Identify any legal or regulatory barriers that could impede the development or implementation of the idea.

Environmental Impact: Assess the design's effect on the environment, including potential sustainable practices or negative impacts.

Scalability: Determine if the idea can be easily scaled up for mass production.

Competitive Advantage: Consider whether the idea offers unique benefits over existing market offerings.

Time to Market: Estimate the duration from concept to a market-ready product.

Resource Availability: Evaluate the availability of necessary materials and expertise.

Integration with Existing Systems: Assess if the idea can be integrated with existing designs or requires a complete overhaul.

Your response should be a single number between 1 and 5, reflecting your assessment of the design's feasibility based on these considerations. Please provide only this number as your response, with no additional text.
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
# print(feasibility_score(description))

# description = "A washing machine that uses nuclear power to run"
# print(feasibility_score(description))
