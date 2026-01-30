from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin, ModelView

import tables
import api.v1.subs
from db.postgres import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title='Subs',
    lifespan=lifespan,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

app.include_router(api.v1.subs.router)


admin = Admin(app, engine)


class PlanAdmin(ModelView, model=tables.Plan):
    ...


class SubscriptionAdmin(ModelView, model=tables.Subscription):
    can_create = False
    can_edit = False


admin.add_view(PlanAdmin)
admin.add_view(SubscriptionAdmin)
