# Prompt-Based Annotated Bibliography Generator

As the volume of scholarly literature continues to grow, finding relevant research articles for specific research topics becomes increasingly difficult. In this paper, we propose a potential solution to this problem, with our novel Natural Language Processing solution. We propose the Prompt-Based Annotated Bibliography Generator, that given a research topic of any length and complexity, will return an annotated bibliography containing relevant research articles. For this purpose, we built a large vector database, which contains SciBERT word embeddings of 55,000 documents retrieved from the CORE research paper database. Using this database, we are able to quickly retrieve the most similar research paper to a given user prompt. Our results indicate that this algorithm could be drastically improved, but are encouraging for potential future work.

## Codebase + Evironment Setup
```
$ git clone https://github.com/samphillippo/NLPProject.git
$ cd NLPProject
$ bash create_conda_env.script
$ source activate nlp_demo_env
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
- (Optional) Split your dataset into multiple folders with `python src/SplitDirectoryFiles.py`
- Reduce file sizes for processing with `python src/ChunkLargeFile.py`
  - edit the `FOLDERS` variable to point to whatever directories to chunk
- Create a completed json tracker with `touch completed.txt`
- Begin processing your dataset with `python src/ProcessDataBuildDB.py <read_folder_path> <completed_file_path>`
