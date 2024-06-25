from fastapi import APIRouter

from workout_api.atleta.controller import router as router_atleta
from workout_api.categorias.controller import router as router_categoria
from workout_api.centro_treinamento.controller import router as router_centro_treinamento


api_router = APIRouter()
api_router.include_router(router_atleta, prefix='/atletas', tags=['Atletas'])
api_router.include_router(router_categoria, prefix='/categorias', tags=['Categorias'])
api_router.include_router(router_centro_treinamento, prefix='/centro-treinamentos', tags=['Centro de Treinamentos'])

