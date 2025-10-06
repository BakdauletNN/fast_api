from fastapi import FastAPI


my_app = FastAPI()


@my_app.get("/hi")
def get_hello():
    return 'hello'