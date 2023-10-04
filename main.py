import uvicorn
import asyncio
from fastapi import FastAPI
from app.routers import users
from app.service import db_service

app = FastAPI()
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Fast API in Python"}
    
async def main():
    await db_service.build()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())