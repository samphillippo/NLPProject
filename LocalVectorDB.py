
from docarray import BaseDoc
from docarray.typing import NdArray
from docarray import DocList
import numpy as np
from vectordb import HNSWVectorDB

class VecDoc(BaseDoc):
  text: str = ''
  embedding: NdArray[768]


class LocalVectorClient:

    def __init__(self):
        self.db = HNSWVectorDB[VecDoc](workspace='.', space='l2', num_threads=1)


    def insert(self, vectorEmbeddings):
        """
        Inserts the given vectorEmbeddings to the vector DB.

        params:
            vectorEmbeddings: a list of VecDocs
        """
        self.db.index(inputs=DocList[VecDoc](vectorEmbeddings))
        self.db.persist()


    def search(self, queryVector, responseLimit=5):
        """
        Searches for the top responseLimit vectors closest to each given query vector.

        params:
            queryVector: list of floats (vector) to search
            responseLimit: the max number of vectors to return for each given query vector
        returns:
            response object from DB
        """
        query = VecDoc(text='query', embedding=queryVector)
        results = self.db.search(inputs=DocList[VecDoc]([query]), limit=responseLimit)
        return results






# Specify your workspace path

# Index a list of documents with random embeddings
# doc_list = [VecDoc(text=f'toy doc zero {i}', embedding=[0, 0, 0]) for i in range(2)]
# db.index(inputs=DocList[VecDoc](doc_list))

# db.persist()

# # doc_list = [VecDoc(text=f'toy doc one {i}', embedding=[1, 1, 1]) for i in range(2)]
# # db.index(inputs=DocList[VecDoc](doc_list))

# # db.persist()


# # Perform a search query
# query = VecDoc(text='query', embedding=[0.2, 0.2, 0.2])
# results = db.search(inputs=DocList[VecDoc]([query]), limit=20)

# # Print out the matches
# for m in results[0].matches:
#   print(m.text)
