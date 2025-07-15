from transformers import pipeline
from .weaviate_client import WeaviateClient

class RagChatbot:
    def __init__(self, weaviate_client, model_name="distilbert-base-cased-distilled-squad"):
        """
        Initialize the RagChatbot with a Weaviate client and a Hugging Face question-answering pipeline.
        
        Parameters:
            model_name (str, optional): Name of the pretrained model to use for the question-answering pipeline. Defaults to "distilbert-base-cased-distilled-squad".
        """
        self.weaviate_client = weaviate_client
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer(self, question):
        """
        Answers a question by retrieving relevant news summaries from a Weaviate database and applying a question-answering model.
        
        Parameters:
            question (str): The question to be answered.
        
        Returns:
            str: The answer extracted from the aggregated news summaries.
        """
        response = self.weaviate_client.client.query.get(
            "News", ["title", "summary"]
        ).with_near_text(
            {"concepts": [question]}
        ).with_limit(3).do()

        articles = response["data"]["Get"]["News"]
        context = ""
        for article in articles:
            context += article["summary"] + " "

        result = self.qa_pipeline(question=question, context=context)
        return result["answer"]

if __name__ == "__main__":
    # This part will not work until the Weaviate instance is running
    # weaviate_client = WeaviateClient()
    # chatbot = RagChatbot(weaviate_client)
    # answer = chatbot.answer("What is the latest news about Apple?")
    # print(answer)
    pass
