import os
from collections import deque


from ChunkLargeFile import chunk_xz_file
from PreprocessDataBase import process_file
# from EmbeddingGenerator import generate_

def shouldChunkFile(filepath, min_size_MB):
    return (os.path.getsize(filepath) / 1000.0) > (min_size_MB * 1000.0)



FOLDER_PATH = './test_json'
XZ_MIN_SIZE_MB = 150

if __name__ == '__main__':
    files = deque(filter(lambda x: x.endswith('.xz'), os.listdir(FOLDER_PATH)))

    while not files.empty():
        file = files.popleft()
        path = FOLDER_PATH + '/' + file

        if shouldChunkFile(path, XZ_MIN_SIZE_MB):
            chunked_files = chunk_xz_file(path)
            files.extend(chunked_files)
        else:
            #TODO: process file, make word embeddings, save to vector DB
            # embeddings = process_file(path, embedding_func)

