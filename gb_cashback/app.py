from fastapi import FastAPI

from gb_cashback.routes.auth import router as auth_router
from gb_cashback.routes.cashback import router as cashback_router
from gb_cashback.routes.purchases import router as purchases_router
from gb_cashback.routes.resellers import router as resellers_router

app = FastAPI()
app.include_router(resellers_router)
app.include_router(purchases_router)
app.include_router(cashback_router)
app.include_router(auth_router)


@app.get('/')
def root():
    return {'message': 'GB Cashback'}
