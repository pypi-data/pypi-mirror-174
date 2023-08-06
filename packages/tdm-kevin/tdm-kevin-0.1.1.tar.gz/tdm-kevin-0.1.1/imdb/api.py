from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory='templates/')


@app.get("/")
async def root():
    """
    Returns a simple message, "Hello World!"
    Returns:
        dict: The response JSON.
    """
    return {"message": "Hello World"}