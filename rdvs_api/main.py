import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dependencies import get_token_header
from services import user, company, job, charts, industry, common

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    charts.router,
    prefix="/charts",
    tags=["charts"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


