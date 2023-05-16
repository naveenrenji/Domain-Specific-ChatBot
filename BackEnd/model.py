# from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


#Models tested - gpt2, microsoft/DialoGPT-medium, PygmalionAI/pygmalion-6b , facebook/blenderbot-400M-distill

# tokenizer = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6b")
# model = AutoModelForCausalLM.from_pretrained("PygmalionAI/pygmalion-6b")

model = GPT2LMHeadModel.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = GPT2Tokenizer.from_pretrained("microsoft/DialoGPT-medium", padding_side='left')

# tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")

def generate_response(question, context):
    question = question +  '<|endoftext|>'
    input_text = f'{context} {question}'
    print(input_text)
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    # Set the max_length and temperature parameters
    outputs = model.generate(input_ids, max_length=100, temperature=0.8, pad_token_id=tokenizer.eos_token_id)
    # Start decoding from the end of the input_ids
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)[len(tokenizer.decode(input_ids[0], skip_special_tokens=True)):]
    # Limit the response to two sentences
    sentences = response.split('. ')
    truncated_response = '. '.join(sentences[:2])

    return truncated_response
