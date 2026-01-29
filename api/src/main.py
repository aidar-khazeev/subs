from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse, HTMLResponse
from sqladmin import Admin, ModelView, action

import tables
from db.postgres import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title='Bill',
    lifespan=lifespan,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)
admin = Admin(app, engine)


class SubscriptionAdmin(ModelView, model=tables.Subscription):
    column_list = [tables.Subscription.id, tables.Subscription.user_id]

    @action(
        name="Some nice action",
        label="aslkdaslkdjlkj",
        confirmation_message="Are you sure?",
        add_in_detail=True,
        add_in_list=True,
    )
    async def approve_users(self, request: Request):
        return HTMLResponse()


admin.add_view(SubscriptionAdmin)
