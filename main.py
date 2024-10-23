from fastapi import FastAPI, HTTPException


def make_fastapi_application() -> FastAPI:
    application = FastAPI()

    @application.get("/about")
    async def about():
        return {"Тестовая заглушка для закрытия карточки ИПР1"}

    return application


if __name__ == '__main__':
    app = make_fastapi_application()
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=1234)
