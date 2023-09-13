# from model import generate_response
from Validation.validation import predict_validation
from Novelty.novelty import classify_novelty
from Feasibility.feasibility import classify_feasibility

# def get_bot_response(message, context):
#     response = generate_response(message, context)
#     return response

def get_validation(message):
    response = predict_validation(message)
    return response

def get_novelty(message):
    response = classify_novelty(message)
    return response

def get_feasibility(message):
    response = classify_feasibility(message)
    return response