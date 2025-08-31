import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.manager import Manager


app = FastAPI()
manager = Manager()


@app.get("/data")
async def get_data():
    return JSONResponse(content=manager.get_process_data())


if __name__ == '__main__':
    print(manager.get_process_data())
    uvicorn.run(app, host="0.0.0.0", port=8000)