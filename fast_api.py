from fastapi import FastAPI

app = FastAPI()


@app.get('/test')
def home():
    return {"TEST":"SERHAN"}

