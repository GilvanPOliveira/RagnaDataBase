from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.item_routes import router as item_router
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(
    title="RagnaDataBase API",
    version="1.0.0",
    default_response_class=JSONResponse
)

app.include_router(item_router, tags=["Item Search"])

@app.middleware("http")
async def convert_null_to_empty(request: Request, call_next):
    response = await call_next(request)
    response_body = [section async for section in response.body_iterator]
    body = b''.join(response_body).decode()

    if response.headers.get("content-type") == "application/json":
        data = json.loads(body)
        
        def replace_null(obj):
            if isinstance(obj, dict):
                return {k: replace_null(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_null(item) for item in obj]
            elif obj is None:
                return ""
            return obj

        data = replace_null(data)
        
        # Remover o header 'Content-Length' original
        headers = dict(response.headers)
        headers.pop('content-length', None)

        return JSONResponse(
            content=data,
            status_code=response.status_code,
            headers=headers
        )

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
