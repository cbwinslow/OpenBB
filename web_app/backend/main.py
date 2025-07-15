from fastapi import FastAPI
from scripts.db_connections import ConnectionManager
from scripts.trading_db import list_strategies
from scripts.weaviate_client import WeaviateClient
from scripts.rag_chatbot import RagChatbot
from scripts.data_pipeline import fetch_equity, load_prices

app = FastAPI()
cm = ConnectionManager({"type": "postgres"})
# weaviate_client = WeaviateClient()
# chatbot = RagChatbot(weaviate_client)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/strategies")
def get_strategies():
    return list_strategies(cm)

@app.post("/chatbot")
def chat(question: str):
    # answer = chatbot.answer(question)
    # return {"answer": answer}
    return {"answer": "This feature is not available yet."}

@app.get("/prices/{symbol}")
def get_prices(symbol: str):
    with cm.context() as conn:
        cur = conn.cursor()
        cur.execute("SELECT date, open, high, low, close FROM prices WHERE symbol = %s ORDER BY date", (symbol,))
        rows = cur.fetchall()
        cur.close()
        return [
            {
                "time": row[0].strftime("%Y-%m-%d"),
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
            }
            for row in rows
        ]
