# Prompt-Based Annotated Bibliography Generator

TODO: add abstract here

## Codebase + Evironment Setup
```
$ git clone https://github.com/eoinFlynn-NU/NLPProject.git
$ cd NLPProject
$ bash create_conda_enc.script
```
## Vector Database Setup
```
TODO: make accessible through git lfs
```

## Running Demo:
```
$ cd src
$ python Demo.py
```

## Running Tests:
```
$ cd src
$ python Testing.py
```

## Setting up your own VectorDB:
- Register for access and download 2018 Metadata-only dataset [here](https://core.ac.uk/documentation/dataset#dataset2018)
- (Optional) Split your dataset into multipltle folders with `python src/SplitDirectoryFiles.py`
- Reduce file sizes for processing with `python src/ChunkLargeFile.py`
  - edit the `FOLDERS` variable to point to whatever directories to chunk
- Create a completed json tracker with `touch completed.txt`
- Begin processing your dataset with `python src/ProcessDataBuildDB.py <read_folder_path> <completed_file_path>`
