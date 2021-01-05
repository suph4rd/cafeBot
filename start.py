from aiogram import Dispatcher


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp
    print("Start bot")
    executor.start_polling(dp, on_shutdown=shutdown)