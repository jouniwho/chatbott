"""
Script for worker implementation
"""

import torch
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
from openai import OpenAI

client = OpenAI(api_key="YOUR OPENAI API KEY")

def get_response(query):

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"{query}"}
    ]
    )
    return completion.choices[0].message.content

def get_response_from_GPT2(query):
    """
    PyTorch GPT 2
    """
    # Load pre-trained model tokenizer (vocabulary)
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    # Encode the query inputs
    indexed_tokens = tokenizer.encode(query)

    # Convert indexed tokens in a PyTorch tensor
    tokens_tensor = torch.tensor([indexed_tokens])

    # Load pre-trained model (weights)
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # Set the model in evaluation mode to deactivate the DropOut modules
    model.eval()

    # If you have a GPU, put everything on cuda
    tokens_tensor = tokens_tensor.to('cuda')
    model.to('cuda')

    # Predict all tokens
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    # Get the predicted next sub-word
    predicted_index = torch.argmax(predictions[0, -1, :]).item()
    predicted_text = tokenizer.decode(indexed_tokens + [predicted_index])
    
    return predicted_text
