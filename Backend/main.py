from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from getRawData import get_database_name as get_data
from Page1 import page1_data_query

app = FastAPI()

@app.get("/showdatabase")
def get_database():
    return get_data()

@app.get("/page1data")
def get_page_1_data():
    return page1_data_query.query_data1()

class ServiceNotFound(Exception):
    def __init__(self, name: str = "No service found"):
        self.name = name

@app.exception_handler(ServiceNotFound)
async def service_not_found_handler(request: Request, exc: ServiceNotFound):
    return JSONResponse(status_code=404, content={"message": exc.name})


def run():
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()