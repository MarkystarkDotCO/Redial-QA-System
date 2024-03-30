from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from torch.utils.data import DataLoader, TensorDataset
# from transformers import AdamW
from torch.optim import AdamW

from torch.nn.utils.rnn import pad_sequence
import json
from datetime import datetime

def train(filename):
    # Read JSON data from file
    with open(filename, "r") as file:
        triplets = json.load(file)

    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForQuestionAnswering.from_pretrained("bert-base-uncased")

    # Tokenize and encode the triplets
    inputs = []
    max_length = 0
    for triplet in triplets:
        for question, answer in zip(triplet["questions"], triplet["answers"]):
            encoded = tokenizer(question, triplet["context"], return_tensors="pt")
            inputs.append({"input_ids": encoded["input_ids"].squeeze(0), "attention_mask": encoded["attention_mask"].squeeze(0)})
            max_length = max(max_length, encoded["input_ids"].size(1))

    # Pad the input sequences to the same length
    padded_input_ids = pad_sequence([x["input_ids"] for x in inputs], batch_first=True, padding_value=tokenizer.pad_token_id)
    padded_attention_mask = pad_sequence([x["attention_mask"] for x in inputs], batch_first=True, padding_value=0)  # Assuming tokenizer.pad_token_id corresponds to 0

    # Prepare data loader
    dataset = TensorDataset(padded_input_ids, padded_attention_mask)
    loader = DataLoader(dataset, batch_size=8, shuffle=True)

    # Define optimizer and loss function
    optimizer = AdamW(model.parameters(), lr=5e-5)
    loss_fn = torch.nn.CrossEntropyLoss()

    # Training loop
    epochs = 3
    for epoch in range(epochs):
        total_loss = 0
        for input_ids, attention_mask in loader:
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask)
            start_scores, end_scores = outputs.start_logits, outputs.end_logits
            # Since we have multiple question-answer pairs, we calculate the loss for each pair separately
            start_positions = torch.argmax(input_ids, dim=1)
            end_positions = torch.argmax(input_ids, dim=1)
            loss = (loss_fn(start_scores, start_positions) +
                    loss_fn(end_scores, end_positions)) / 2  # Cross-entropy loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(loader)}")

    # Save the trained model
    model.save_pretrained("bert_question_answering_model")
    tokenizer.save_pretrained("bert_question_answering_model")

if __name__ == "__main__":

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f'../../data/processed/redial_dataset_{current_date}_train.json'
    # data/processed/redial_dataset_2024-03-30_train.json
    train(filename)