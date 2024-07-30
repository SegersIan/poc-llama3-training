import os
from datasets import Dataset
from transformers import LlamaTokenizer, LlamaForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling

# Step 1: Read the consolidated text file
text_file_path = os.path.abspath('../temp/combined_markdown_content.txt')
print(f"Full path of the learning data: {text_file_path}")
with open(text_file_path, 'r', encoding='utf-8') as file:
    corpus = file.read()

# Step 2: Create a Hugging Face dataset from the text
dataset = Dataset.from_dict({'text': [corpus]})

# model_file_path = os.path.expanduser('~/.ollama/models/blobs/sha256-6a0746a1ec1aef3e7ec53868f220ff6e389f6f8ef87a01d77c96807de94ca2aa')
# model_file_path = os.path.expanduser('llama3:latest')
model_file_path = "meta-llama/Meta-Llama-3-8B"
print(f"Full path of the model: {model_file_path}")
# Step 3: Load the tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained(model_file_path)
model = LlamaForCausalLM.from_pretrained(model_file_path)

# Step 4: Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Step 5: Set up the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Step 6: Define the data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Step 7: Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    data_collator=data_collator,
)

# Step 8: Train the model
trainer.train()

# Step 9: Evaluate the model
results = trainer.evaluate()
print(results)

# Step 10: Save the trained model
model.save_pretrained("../output/trained_llama3_model")
tokenizer.save_pretrained("../output/trained_llama3_model")
