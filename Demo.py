
from ProcessDataBuildDB import setupTokenizerAndModel
from EmbeddingGenerator import generate_embedding_from_text
from VectorDB import VectorClient

class Demo:

    def __init__(self):
        self.device, self.tokenizer, self.model = setupTokenizerAndModel()
        self.client = VectorClient()

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
        embedding = generate_embedding_from_text(self.model, self.tokenizer, self.device, researchObjective)
        response = self.client.search([embedding], responseLimit) 
        
        # only query one vector so expect response[0]
        if len(response) == 0 or len(response[0]):
            return None
        
        annotations = [resp_obj['entity']['annotation'] for resp_obj in response[0]]
        return annotations



if __name__ == '__main__':
    
    demo = Demo()

    query = input("Write a research objective: ")

    annotations = demo.getAnnotations(query)

    for annotation in annotations:
        print(annotation, '\n')