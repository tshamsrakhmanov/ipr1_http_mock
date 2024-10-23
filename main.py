from fastapi import FastAPI
from pydantic import BaseModel
import enum
import random
import logging
from logging import FileHandler
import sys


class Currency(enum.Enum):
    dollar = "USD"
    euro = "EU"
    rouble = "RUB"


# input json model
class BalanceSheet(BaseModel):
    rqUID: str
    clientId: int
    account: int
    openDate: str
    closeDate: str


# main application method
def make_fastapi_application() -> FastAPI:
    # Logger implementation

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # handler for Docker-run cases
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # handler for standalone run cases (file logging)
    handler2 = FileHandler("stub.log", encoding='utf-8')
    handler2.setLevel(logging.DEBUG)
    handler2.setFormatter(formatter)
    root.addHandler(handler2)

    # application entry point implementation

    application = FastAPI()

    @application.get("/about")
    async def about():
        return {"Эмулятор для закрытия карточки ИПР1"}

    @application.post("/get_balance/")
    async def get_balance(balance_sheet: BalanceSheet):

        logging.info(f'Message recieved:{balance_sheet}')

        answer = dict()

        answer.setdefault("rqUID", balance_sheet.rqUID)
        answer.setdefault("clientId", balance_sheet.clientId)
        answer.setdefault("account", balance_sheet.account)

        if str(balance_sheet.clientId)[0] == '8':
            # clientID starts with 8 -> USD
            answer.setdefault("currency", Currency.dollar)
            answer.setdefault("maxLimit", "2000.00")
            answer.setdefault("balance", str(round(random.uniform(0, 1), 2) + random.randint(0, 2000)))
        elif str(balance_sheet.clientId)[0] == '9':
            # clientID starts with 9 -> EU
            answer.setdefault("currency", Currency.euro)
            answer.setdefault("maxLimit", "1000.00")
            answer.setdefault("balance", str(round(random.uniform(0, 1), 2) + random.randint(0, 1000)))
        else:
            answer.setdefault("currency", Currency.rouble)
            answer.setdefault("maxLimit", "9999.99")
            answer.setdefault("balance", str(round(random.uniform(0, 1), 2) + random.randint(0, 9999)))

        logging.info(f'Message returned:{balance_sheet}')
        return answer

    return application


# entry point
if __name__ == '__main__':
    app = make_fastapi_application()
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=1234)
