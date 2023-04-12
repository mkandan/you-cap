from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World","var":123}

@app.get("/test")
async def root():
    return {"message": "test World","var":789}
