# main.py
import uvicorn
import blockchaintools
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hash")
async def test():
    return {"hash": blockchaintools.compute_hash("test")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

