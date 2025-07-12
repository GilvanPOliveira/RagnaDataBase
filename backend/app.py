import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User
from db.session import get_session
from passlib.hash import bcrypt
from routes.user_routes import router as user_router
from routes.item_routes import router as item_router
from routes.search_routes import router as search_router
from routes.auth_routes import router as auth_router
from routes.inventory_routes import router as inventory_router
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="RagnaDataBase API", version="1.0.0")

app.include_router(user_router)
app.include_router(item_router, tags=["Item Search"])
app.include_router(search_router, tags=["Item Name Search"])
app.include_router(auth_router)
app.include_router(inventory_router)

@app.on_event("startup")
async def create_admin_user():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("Variáveis de ambiente do admin não configuradas.")
        return

    db_gen = get_session()
    db = await anext(db_gen)
    try:
        query = await db.execute(select(User).where(User.email == admin_email))
        admin_user = query.scalar_one_or_none()
        if not admin_user:
            hashed_password = bcrypt.hash(admin_password)
            new_admin = User(email=admin_email, password=hashed_password, name="Administrador", is_admin=True, is_superadmin=True)
            db.add(new_admin)
            await db.commit()
            print("Usuário admin criado com sucesso.")
        else:
            print("Usuário admin já existe.")
    finally:
        await db_gen.aclose()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
