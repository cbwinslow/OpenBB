import weaviate

class WeaviateClient:
    def __init__(self, url="http://localhost:8080"):
        """
        Initialize a Weaviate client connected to the specified URL.
        
        Parameters:
            url (str, optional): The URL of the Weaviate instance to connect to. Defaults to "http://localhost:8080".
        """
        self.client = weaviate.Client(url)

    def create_schema(self):
        """
        Create a schema in Weaviate for storing news articles with predefined properties.
        
        Defines a "News" class in the Weaviate instance, specifying fields for title, summary, URL, source, and publication date, and sets the vectorizer to "text2vec-transformers".
        """
        schema = {
            "classes": [
                {
                    "class": "News",
                    "description": "A news article",
                    "vectorizer": "text2vec-transformers",
                    "properties": [
                        {
                            "name": "title",
                            "dataType": ["string"],
                            "description": "The title of the news article",
                        },
                        {
                            "name": "summary",
                            "dataType": ["text"],
                            "description": "The summary of the news article",
                        },
                        {
                            "name": "url",
                            "dataType": ["string"],
                            "description": "The URL of the news article",
                        },
                        {
                            "name": "source",
                            "dataType": ["string"],
                            "description": "The source of the news article",
                        },
                        {
                            "name": "published_at",
                            "dataType": ["date"],
                            "description": "The publication date of the news article",
                        },
                    ],
                }
            ]
        }
        self.client.schema.create(schema)

    def load_news(self, articles):
        """
        Batch imports a list of news articles into the "News" class in Weaviate.
        
        Parameters:
            articles (list): A list of article objects, each with attributes for title, summary, url, source, and published_at.
        """
        with self.client.batch as batch:
            for article in articles:
                batch.add_data_object(
                    {
                        "title": article.title,
                        "summary": article.summary,
                        "url": article.url,
                        "source": article.source,
                        "published_at": article.published_at,
                    },
                    "News",
                )

if __name__ == "__main__":
    # This part will not work until the Weaviate instance is running
    # client = WeaviateClient()
    # client.create_schema()
    # from .news_pipeline import latest_news
    # articles = latest_news(100)
    # client.load_news(articles)
    # print("News loaded into Weaviate")
    pass
