"""
Main module, takes the apis from router and routes to app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route_auto import automl


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(automl)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
