from fastapi import FastAPI

from db.connection import start_db_connections, stop_db_connections

from .api.ads import router as ad_router
from .api.authors import router as author_router
from .api.categories import router as category_router
from .api.delivery import router as delivery_router
from .api.reason_closing import router as reason_closing_router
from .api.statuses import router as status_router

app = FastAPI(
    title='Ad Test Api',
)
app.include_router(author_router, tags=['Author'])
app.include_router(ad_router, tags=['Ad'])
app.include_router(category_router, tags=['Category'])
app.include_router(status_router, tags=['Status'])
app.include_router(delivery_router, tags=['Delivery'])
app.include_router(reason_closing_router, tags=['ReasonClosing'])


@app.on_event('startup')
def startup_event():
    start_db_connections()


@app.on_event('shutdown')
def shutdown_event():
    stop_db_connections()
