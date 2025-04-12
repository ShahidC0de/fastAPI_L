from fastapi import FastAPI
app = FastAPI()
@app.get('/')
async def read_root():
    return {"message": "hello world"}
@app.get('/message')
async def read_message():
    return "I am the message"