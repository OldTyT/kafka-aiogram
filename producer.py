import asyncio
import logging
import sys
from os import getenv
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

from logger import logger

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TOKEN")


KAFKA_CONF = {"bootstrap.servers": "127.0.0.1:9092"}

producer = Producer(KAFKA_CONF)

dp = Dispatcher()


def delivery_report(err, msg):
    if err is not None:
        logger.error("Message delivery failed: {}".format(err))
    else:
        logger.debug(
            "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
        )


class KafkaMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Update, data: Dict[str, Any]):
        json_data = event.model_dump_json()
        producer.produce(
            "telegram_update", key="update", value=json_data, callback=delivery_report
        )
        producer.flush()
        return await handler(event, data)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.update.outer_middleware(KafkaMiddleware())
    await dp.start_polling(bot)


def prepare_kafka():
    admin_client = AdminClient(KAFKA_CONF)
    topic_telegram_update = NewTopic(
        topic="telegram_update", num_partitions=3, replication_factor=1
    )
    fs = admin_client.create_topics([topic_telegram_update])
    for topic, f in fs.items():
        try:
            f.result()
            logger.info(f"Topic {topic} success created")
        except Exception as e:
            logger.warning(f"Error when topic creating {topic}: {e}")


if __name__ == "__main__":
    prepare_kafka()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
