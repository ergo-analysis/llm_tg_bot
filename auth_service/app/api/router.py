from fastapi import APIRouter 
from .routes_auth import router 

api_router = APIRouter() 
api_router.include_router(router)
