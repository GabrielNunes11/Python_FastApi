from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=True)
    sobrenome = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False)
    senha = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    criador = relationship("ArtigoModel", cascade='all,delete-orphan', back_populates="criador", uselist=True, lazy="joined")