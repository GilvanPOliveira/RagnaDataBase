from fastapi import FastAPI
from routes.item_routes import router as item_router
from routes.search_routes import router as search_router
from routes.auth_routes import router as auth_router
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="RagnaDataBase API", version="1.0.0")

app.include_router(item_router, tags=["Item Search"])
app.include_router(search_router, tags=["Item Name Search"])
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)


#para executar o projeto:
# uvicorn app:app --host 127.0.0.1 --port 8000 --reload
