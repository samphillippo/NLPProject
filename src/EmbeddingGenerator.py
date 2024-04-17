from time import time
from torch import torch
import nltk

def get_stopwords_set():
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    return set(stopwords.words('english'))
stopwords_set = get_stopwords_set()



def generate_embedding(model, tokenizer, device, title, abstract, topics):
    token_text = " ".join(topics) + ". " + title + ". " + abstract
    return generate_embedding_from_text(model, tokenizer, device, token_text)



def generate_embedding_from_text(model, tokenizer, device, token_text):
    tokens = tokenizer.tokenize(token_text)
    #max length 300 words
    if len(tokens) > 300:
        tokens = tokens[:300]

    token_embeddings = []
    for token in tokens:
        if token in stopwords_set:
            continue
        # Tokenize the token separately and get the token ID
        token_ids = tokenizer(token, return_tensors="pt")["input_ids"].to(device)

        # Get the embedding for the token
        with torch.no_grad():
            output = model(input_ids=token_ids)
            token_embedding = output.last_hidden_state.mean(dim=1).squeeze()

        token_embeddings.append(token_embedding)

    # Average all token embeddings
    average_embedding = torch.stack(token_embeddings).mean(dim=0)

    return average_embedding.tolist()
