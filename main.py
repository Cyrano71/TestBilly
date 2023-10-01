import uvicorn
from fastapi import FastAPI
from app.routers import users
import asyncio

app = FastAPI()
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

async def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)