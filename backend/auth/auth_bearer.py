from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_handler import verify_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            payload = verify_token(token)
            if payload is None:
                raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
            return payload
        else:
            raise HTTPException(status_code=403, detail="Credenciais de autenticação não fornecidas.")
