from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain.chains import LLMChain

# Define the criteria for novelty and feasibility
novelty_criteria = """
Novelty Classification Criteria:
- Uniqueness
- Innovation
- Technological Advances
- User Experience
- Environmental Impact
"""

feasibility_criteria = """
Feasibility Classification Criteria:
- Technological Feasibility
- Economic Feasibility
- User Acceptance
- Scalability
- Competitive Advantage
- Resource Availability
- Integration with Existing Systems
"""

stainability_criteria = """
Sustainability Criteria - 
- Environmental Impact
- Carbon emmission
- social impact
"""

# Ollama Llama2 LLM
llm = Ollama(model="llama3")
output_parser = StrOutputParser()

# Define critique model prompt
critique_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI trained to critique engineering design descriptions based on given criteria. You need to critique only, no suggesting improvements"),
        ("user", "Description: {description}\n\nCriteria:\n{criteria}\n\nScore:\nNovelty: {novelty_score}\nFeasibility: {feasibility_score}")
    ]
)
critique_chain = LLMChain(prompt=critique_prompt, llm=llm, output_parser=output_parser)

# # Define critique suggestion model prompt
# critique_suggestion_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an AI trained to critique and suggest improvements for engineering design descriptions based on given criteria. So just critique the description and give suggestions on improvement."),
#         ("user", "Description: {description}\n\nCriteria:\n{criteria}\n\nScore:\nNovelty: {novelty_score}\nFeasibility: {feasibility_score}\n\nSuggestions: Provide critique and suggestions based on the criteria.")
#     ]
# )
# critique_suggestion_chain = LLMChain(prompt=critique_suggestion_prompt, llm=llm, output_parser=output_parser)

# # Define design summary and final score model prompt
# design_summary_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an AI trained to generate a design summary and final score for engineering design descriptions based on given criteria and previous evaluations."),
#         ("user", "Description: {description}\n\nCriteria:\n{criteria}\n\nScore:\nNovelty: {novelty_score}\nFeasibility: {feasibility_score}\n\nChat History:\n{chat_history}\n\nSummary: Provide a summary and final scores based on the evaluations.")
#     ]
# )
# design_summary_chain = LLMChain(prompt=design_summary_prompt, llm=llm, output_parser=output_parser)

# Function to determine which model to use
def get_response_model(novelty_score, feasibility_score):
    if novelty_score < 3 or feasibility_score < 3:
        return critique_chain
    # elif novelty_score < 4 or feasibility_score < 4:
    #     return critique_suggestion_chain
    # else:
    #     return design_summary_chain

# Dummy scores for demonstration
dummy_scores = [
    {
        "novelty_score": 2,
        "feasibility_score": 3,
        "description": "A washing machine that uses ultrasonic sound waves to agitate and clean clothes, reducing water usage."
    },
    {
        "novelty_score": 2,
        "feasibility_score": 3,
        "description": "A washing machine that recycles and filters water for reuse, aiming to save water and reduce environmental impact."
    },
    {
        "novelty_score": 4,
        "feasibility_score": 2,
        "description": "A washing machine with an integrated AI system that customizes washing cycles based on fabric type and load size."
    },
    # {
    #     "novelty_score": 5,
    #     "feasibility_score": 3,
    #     "description": "A solar-powered washing machine that operates entirely off-grid, designed for remote areas with limited access to electricity."
    # },
    # {
    #     "novelty_score": 4,
    #     "feasibility_score": 5,
    #     "description": "A washing machine that uses biodegradable detergents dispensed automatically to minimize waste and environmental impact."
    # }
]

# Process each dummy case
for i, case in enumerate(dummy_scores):
    novelty_score = case["novelty_score"]
    feasibility_score = case["feasibility_score"]
    description = case["description"]
    
    response_model = get_response_model(novelty_score, feasibility_score)
    
    criteria = "noevlty criteria - " + novelty_criteria + " || and feasibility_criteria - " + feasibility_criteria
    chat_history = ""  # Initialize chat history (in a real application, this would be accumulated)
    
    response = response_model.invoke({
        "description": description,
        "criteria": criteria,
        "novelty_score": novelty_score,
        "feasibility_score": feasibility_score,
        "chat_history": chat_history
    })
    print(f"Response for case {i+1}:", response)
