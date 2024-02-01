from pytz import timezone
from pydantic import EmailStr

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/usuario/login'
)


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None
        
        return usuario
    

def _criar_token(tipoToken: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}

    sp = timezone('AMERICA/SAO_PAULO')
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipoToken

    payload["exp"] = expira

    payload["iat"] = datetime.now(tz=sp)

    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipoToken='access_token',
        tempo_vida=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )