from fastapi import FastAPI
from pydantic import BaseModel


class BalanceSheet(BaseModel):
    rqUID: str
    clientId: int
    account: int
    openDate: str
    closeDate: str


def make_fastapi_application() -> FastAPI:
    application = FastAPI()

    @application.get("/about")
    async def about():
        return {"Тестовая заглушка для закрытия карточки ИПР1"}

    @application.post("/get_balance/")
    async def get_balance(balance_sheet: BalanceSheet):
        answer = dict()

        print(balance_sheet)

        return answer

    return application


if __name__ == '__main__':
    app = make_fastapi_application()
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=1234)
