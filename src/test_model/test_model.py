from transformers import BertTokenizer, BertForQuestionAnswering
import torch

# Load the trained model and tokenizer
model = BertForQuestionAnswering.from_pretrained("bert_question_answering_model")
tokenizer = BertTokenizer.from_pretrained("bert_question_answering_model")

# Define a function to predict answers
def predict_answer(context, question):
    # Tokenize inputs
    inputs = tokenizer(question, context, return_tensors="pt")

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)
        # print("Model outputs:", outputs)
    
    # Extract start_scores and end_scores from outputs
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    # print("start_scores type:", type(start_scores))
    # print("end_scores type:", type(end_scores))

    # Ensure start_scores and end_scores are tensors
    start_scores = start_scores.squeeze(0)  # Remove the batch dimension
    end_scores = end_scores.squeeze(0)      # Remove the batch dimension

    # Get the most likely answer
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    # Check if the predicted answer span is valid
    if end_index < start_index or torch.max(start_scores) < 0 or torch.max(end_scores) < 0:
        return "No answer found."

    answer_tokens = inputs["input_ids"][0][start_index:end_index]
    answer = tokenizer.decode(answer_tokens)

    return answer

# Test the model
context = "The quick brown fox jumps over the lazy dog."
question = "What does the fox jump over?"
predicted_answer = predict_answer(context, question)

print("Predicted Answer:", predicted_answer)
