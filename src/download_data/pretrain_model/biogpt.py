# from transformers import AutoTokenizer, BioGptModel
# import torch

# tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")
# model = BioGptModel.from_pretrained("microsoft/biogpt")

# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")

# outputs = model(**inputs)

# print(outputs)

from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")
model = AutoModelForCausalLM.from_pretrained("microsoft/biogpt")

# Input text
text = "Hello, my dog is cute"

# Tokenize input text
input_ids = tokenizer.encode(text, return_tensors="pt")

# Generate text
output = model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7)

# Decode and print generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
