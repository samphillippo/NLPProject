from transformers import AutoTokenizer, AutoModel
from torch import torch

# Load SciBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

# Load SciBERT model
model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")

abstract = "Your research paper abstract goes here."

# Tokenize the abstract
tokens = tokenizer.tokenize(abstract)

token_embeddings = []
for token in tokens:
    # Tokenize the token separately and get the token ID
    token_ids = tokenizer(token, return_tensors="pt")["input_ids"]

    # Get the embedding for the token
    with torch.no_grad():
        output = model(input_ids=token_ids)
        token_embedding = output.last_hidden_state.mean(dim=1).squeeze()

    token_embeddings.append(token_embedding)

# Average all token embeddings
average_embedding = torch.stack(token_embeddings).mean(dim=0)
