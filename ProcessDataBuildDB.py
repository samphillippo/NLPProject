import os
import sys
from collections import deque
from transformers import AutoTokenizer, AutoModel
from torch import torch

from ChunkLargeFile import chunk_xz_file
from PreprocessDataBase import process_file
from EmbeddingGenerator import generate_embedding
from VectorDB import VectorClient



def shouldChunkFile(filepath, min_size_MB):
    return (os.path.getsize(filepath) / 1000.0) > (min_size_MB * 1000.0)


def setupTokenizerAndModel():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load SciBERT tokenizer
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

    # Load SciBERT model
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
    model = model.to(device)
    return device, tokenizer, model


XZ_MIN_SIZE_MB = 150

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python GenerateFileList.py <read_folder_path> <completed_file_path>")
        sys.exit(1)

    readFolderPath = sys.argv[1]
    files = deque(map((lambda file: readFolderPath + '/' + file), filter(lambda x: x.endswith('.xz'), os.listdir(readFolderPath))))

    completedFilePath = sys.argv[2]
    completedFiles = []
    with open(completedFilePath, 'r+') as file:
        for line in file:
            completedFiles.append(line.rstrip('\n'))
    completedFiles = set(completedFiles)

    print("Initializing Tokenizer and model")
    device, tokenizer, model = setupTokenizerAndModel()

    print("Initializing Vector DB Client")
    vectorClient = VectorClient()

    #print("Gathering initial files into queue")
    #files = deque(map((lambda file: FOLDER_PATH + '/' + file), filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH))))

    while len(files) > 0:
        file = files.popleft()
        if file in completedFiles:
            continue
        print("Processing file {}".format(file))

        if shouldChunkFile(file, XZ_MIN_SIZE_MB):
            print("Skipping file {} as it is too large".format(file))
            continue
        else:
            print("Processing docs and computing embeddings...")
            embeddings = process_file(file, lambda title, abstract, topics: generate_embedding(model, tokenizer, device, title, abstract, topics))
            # print(embeddings)
            print("Inserting to Vector DB")
            vectorClient.insert(embeddings)
            # denotes file has been processed
            completedFiles.add(file)
            with open(completedFilePath, 'a') as file:
                file.write(file + '\n')
