from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api import activity_router, building_router, organization_router
from api.dependencies import verify_credentials
from utils.migrations import lifespan


app = FastAPI(
    title='Title',
    description='Description',
    version='1.0',
    root_path='/api/v1',
    lifespan=lifespan,
    dependencies=[Depends(verify_credentials)]
)

origins = ['http://localhost', 'http://localhost:8080']

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET'],
    allow_headers=['*']
)

app.include_router(activity_router, prefix='/activities', tags=['activity'])
app.include_router(building_router, prefix='/buildings', tags=['building'])
app.include_router(organization_router, prefix='/organizations', tags=['organization'])
