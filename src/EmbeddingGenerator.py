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


def test():
    from transformers import AutoTokenizer, AutoModel
    from torch import torch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load SciBERT tokenizer
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

    # Load SciBERT model
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
    model = model.to(device)

    # Test generate_embedding_from_text:
    assert len(generate_embedding_from_text(model, tokenizer, device, "This is a test.")) == 768
    assert generate_embedding_from_text(model, tokenizer, device, "This is a test.") != generate_embedding_from_text(model, tokenizer, device, "This is not a test")
    assert generate_embedding_from_text(model, tokenizer, device, "Test") == generate_embedding_from_text(model, tokenizer, device, "Test Test test")

    # Test generate_embedding:
    assert len(generate_embedding(model, tokenizer, device, "Test", "Test", ["Test"])) == 768
    assert generate_embedding(model, tokenizer, device, "Test", "Test", ["Test"]) != generate_embedding(model, tokenizer, device, "gibberish", "not test", ["fried egg"])
    print('All EmbeddingGenerator tests passed!')
