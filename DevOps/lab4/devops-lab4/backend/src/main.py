import uvicorn
from fastapi import FastAPI

from settings import settings
from routers import router

from db.initdb import initdb

app = FastAPI(debug=False)
app.include_router(router=router)

if __name__ == "__main__":
    initdb()
    uvicorn.run(
        app=app,
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="info"
    )