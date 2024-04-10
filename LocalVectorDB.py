
from docarray import BaseDoc
from docarray.typing import NdArray
from docarray import DocList
import numpy as np
from vectordb import InMemoryExactNNVectorDB, HNSWVectorDB

class VecDoc(BaseDoc):
  text: str = ''
  embedding: NdArray[3]



# Specify your workspace path
db = InMemoryExactNNVectorDB[VecDoc](workspace='./test_workspace')

# # Index a list of documents with random embeddings
# doc_list = [VecDoc(text=f'toy doc {i}', embedding=[0, 0, 0]) for i in range(2)]
# db.index(inputs=DocList[VecDoc](doc_list))

# db.persist()

# doc_list = [VecDoc(text=f'toy doc {i}', embedding=[1, 1, 1]) for i in range(2)]
# db.index(inputs=DocList[VecDoc](doc_list))

# db.persist()


# Perform a search query
query = VecDoc(text='query', embedding=[0.2, 0.2, 0.2])
results = db.search(inputs=DocList[VecDoc]([query]), limit=20)

# Print out the matches
for m in results[0].matches:
  print(m)