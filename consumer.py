import asyncio
import signal
import json
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.fsm.storage.redis import RedisStorage
from confluent_kafka import Consumer

from logger import logger
from models.config import GlobalSettings

cfg = GlobalSettings()

PROGRAM_RUNNING = True
KAFKA_CONF = {
    "bootstrap.servers": cfg.kafka_conf_bootstrap_server,
    "group.id": "bot_reader",
    "auto.offset.reset": cfg.kafka_conf_auto_offset_reset,
}

bot = Bot(token=cfg.telegram_bot_token.get_secret_value())
storage = RedisStorage.from_url(cfg.redis_url.get_secret_value())
dp = Dispatcher(storage=storage)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


def signal_handler(signal_num, current_stack_frame):
    global PROGRAM_RUNNING
    PROGRAM_RUNNING = False


async def kafka_consumer():
    global PROGRAM_RUNNING
    logger.info("Starting consumer.")
    consumer = Consumer(KAFKA_CONF)
    consumer.subscribe(["telegram_update"])
    try:
        while True:
            if not PROGRAM_RUNNING:
                break
            msg = consumer.poll(0.2)
            if msg is None:
                continue
            if msg.error():
                logger.error("Consumer error: {}".format(msg.error()))
                continue
            try:
                json_msg = json.loads(msg.value().decode("utf-8"))
                update = Update(**json_msg)
                logger.debug(update)
                await dp.feed_update(bot, update)
            except Exception as e:
                logger.error(f"Error msg processing: {e}")
    finally:
        consumer.close()


async def main():
    kafka_task = asyncio.create_task(kafka_consumer())
    await kafka_task


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())
    logger.warning("Remaining processes finished!, shutting down now.")
