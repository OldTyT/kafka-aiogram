import asyncio
import json
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from confluent_kafka import Consumer

from logger import logger

KAFKA_CONF = {
    "bootstrap.servers": "127.0.0.1:9092",
    "group.id": "bot_reader",
    "auto.offset.reset": "earliest",
}
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def kafka_consumer():
    logger.info("Starting consumer.")
    consumer = Consumer(KAFKA_CONF)
    consumer.subscribe(["telegram_update"])
    try:
        while True:
            msg = consumer.poll(0.2)
            if msg is None:
                continue
            if msg.error():
                logger.error("Consumer error: {}".format(msg.error()))
                continue
            try:
                json_msg = json.loads(msg.value().decode("utf-8"))
                update = Update(**json_msg)
                await dp.feed_update(bot, update)
            except Exception as e:
                logger.error(f"Error msg processing: {e}")
    finally:
        consumer.close()


async def main():
    kafka_task = asyncio.create_task(kafka_consumer())
    await kafka_task


if __name__ == "__main__":
    asyncio.run(main())
