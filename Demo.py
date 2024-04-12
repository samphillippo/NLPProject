
from ProcessDataBuildDB import setupTokenizerAndModel
from EmbeddingGenerator import generate_embedding_from_text
from LocalVectorDB import LocalVectorClient

class Demo:

    def __init__(self):
        self.device, self.tokenizer, self.model = setupTokenizerAndModel()
        self.db = LocalVectorClient()

    def getAnnotations(self, researchObjective, responseLimit=6):
        """

        Expect response from vectorDB to look like:
        [
            [
                {
                    "id": 240,
                    "distance": 0.0694073885679245,
                    "entity": {
                        "annotation": "..."
                    }
                },
                ...
            ]
        ]
        """
        print("Generating Embedding for:", researchObjective)
        embedding = generate_embedding_from_text(self.model, self.tokenizer, self.device, researchObjective)
        print("Querying database for similar matches")
        response = self.db.search(embedding, responseLimit)

        return response[0].matches



if __name__ == '__main__':

    demo = Demo()

    while True:
        query = input("Write a research objective: ")

        documents = demo.getAnnotations(query)

        print('Annotated Bibliography:\n')

        for doc in documents:
            print(doc.text, '\n')
        print('\n\n')
