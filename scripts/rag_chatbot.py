from transformers import pipeline
from .weaviate_client import WeaviateClient

class RagChatbot:
    def __init__(self, weaviate_client, model_name="distilbert-base-cased-distilled-squad"):
        self.weaviate_client = weaviate_client
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer(self, question):
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
