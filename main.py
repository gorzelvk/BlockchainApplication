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
    return {"hash": blockchaintools.compute_hash("test", "best", "kest")}


@app.get("/blockcreation")
async def blockcreation():
    DIFFICULTY = 4
    b0 = blockchaintools.Block()
    b1 = blockchaintools.Block(b0)
    b2 = blockchaintools.Block(b1)
    b3 = blockchaintools.Block(b2)
    b0.mine(DIFFICULTY)
    b1.mine(DIFFICULTY)
    b2.mine(DIFFICULTY)
    b3.mine(DIFFICULTY)
    return {str(b0), str(b1), str(b1), str(b2), str(b3)}



if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)


