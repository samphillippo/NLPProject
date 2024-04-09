import sys
from collections import deque
import os
from ChunkLargeFile import chunk_xz_file

def shouldChunkFile(filepath, min_size_MB):
    return (os.path.getsize(filepath) / 1000.0) > (min_size_MB * 1000.0)

XZ_MIN_SIZE_MB = 150

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python GenerateFileList.py <all_file_path>")
        sys.exit(1)

    print("Creating file queue")
    allFilePath = sys.argv[1]
    files = []
    with open(allFilePath, 'r') as file:
        for line in file:
            files.append(line.rstrip('\n'))
    files = deque(files)


    all_files = []
    while len(files) > 0:
        file = files.popleft()

        #checks if file exists:
        if not os.path.exists(file):
            print("File does not exist: {}".format(file))
            continue

        if shouldChunkFile(file, XZ_MIN_SIZE_MB):
            print("Chunking...")
            all_files.extend(chunk_xz_file(file))
        else:
            all_files.append(file)

    #OVERRWRITES FILE:
    with open(allFilePath, 'w') as file:
        for fileName in all_files:
            file.write(fileName + '\n')
