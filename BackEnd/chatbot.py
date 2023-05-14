from model import generate_response

def get_bot_response(message, context):
    response = generate_response(message, context)
    return response
