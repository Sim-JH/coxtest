from fastapi import APIRouter

from .faq import router as faq_router

api_router = APIRouter()
api_router.include_router(faq_router, prefix='/faq', tags=['FAQ'])
