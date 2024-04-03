import os
from collections import deque
from transformers import AutoTokenizer, AutoModel
from torch import torch



from ChunkLargeFile import chunk_xz_file
from PreprocessDataBase import process_file
from EmbeddingGenerator import generate_embedding

def shouldChunkFile(filepath, min_size_MB):
    return (os.path.getsize(filepath) / 1000.0) > (min_size_MB * 1000.0)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

FOLDER_PATH = './test_json'
XZ_MIN_SIZE_MB = 150

if __name__ == '__main__':
    # Load SciBERT tokenizer
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    tokenizer = tokenizer.to(device)

    # Load SciBERT model
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
    model = model.to(device)

    files = deque(filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH)))

    while not files.empty():
        file = files.popleft()
        path = FOLDER_PATH + '/' + file

        if shouldChunkFile(path, XZ_MIN_SIZE_MB):
            chunked_files = chunk_xz_file(path)
            files.extend(chunked_files)
        else:
            embeddings = process_file(path, lambda title, abstract, topics: generate_embedding(model, tokenizer, title, abstract, topics))
            # TODO: save to Vector DB
