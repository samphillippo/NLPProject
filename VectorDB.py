
from pymilvus import MilvusClient



class VectorClient:

    def __init__(self):
        try: 
            self.client = MilvusClient("50.116.63.108:19530")
            self.collectionName = "citationDB"
        except:
            print("Unable to connect to Milvus Client...")


    def insert(self, vectorEmbeddings):
        """
        Inserts the given vectorEmbeddings to the vector DB.

        params:
            vectorEmbeddings: a list of dictionaries with the format {"vector": [float, ...], "annotation": "annotation goes here..."}
        """
        res = self.client.insert(
            collection_name = self.collectionName,
            data = vectorEmbeddings
        )
        if res:
            print(res)
        else:
            print("ERROR: Milvus insert result not found")


    def search(self, queryVectors, responseLimit=5):
        """
        Searches for the top responseLimit vectors closest to each given query vector.

        params:
            queryVectors: list of list of floats (list of vectors) to search
            responseLimit: the max number of vectors to return for each given query vector
        returns:
            response object from Milvus
        """
        res = self.client.search(
            collection_name = self.collectionName,      # target collection
            data = queryVectors,                        # query vectors
            limit = responseLimit,                      # number of returned entities
            output_fields=["annotation"]                # non-indexed fields to return
        )
        return res