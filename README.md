# Kafka-Aiogram
A **template project** for building Python-based Telegram bots integrated with Apache Kafka, using aiogram framework.
This skeleton provides foundational components for creating scalable bot architectures while preserving all native aiogram features.

## Key Notes
* 🛠 Starter Template - Not a production-ready solution, but a minimal setup to bootstrap your own Kafka-based Telegram bot projects
* ⚙️ Extensible - Add custom handlers, middleware, and Kafka topics while maintaining the core aiogram structure
* 📦 Kafka Required - Includes Docker setup for quick Kafka deployment (see Installation section)

## Features
* **Kafka Producer/Consumer Base** - Ready-to-extend classes for message handling
* **Aiogram Integration** - All native features (FSM, filters, middleware) work out-of-the-box
* **Dockerized Kafka** - Local development setup via Docker Compose
* **Structured Logging** - Configurable log format and levels

## Installation

1. Clone and enter repository
```bash
git clone https://github.com/oldtyt/kafka-aiogram.git
cd kafka-aiogram
```
2. Start Kafka with Docker (requires Docker)
```bash
docker-compose up -d  # Starts Kafka + ui
```
3. Install Python dependencies

```bash
pip install -r requirements.txt
```
4. Run producer
```bash
python3 producer.py
```
5. Run consumer
```bash
python3 consumer.py
```

## Configuration

Create env variables:

|Variable | Description | Default |
|-|-|-|
| TELEGRAM_BOT_TOKEN | From [BotFather](https://t.me/BotFather) |	Required |
| LOG_JSON | JSON-formatted logs (true/false)| `false` |
| LOG_LEVEL	| Log verbosity (`debug, info, warning, error`)	| `info` |
| REDIS_URL | Redis URL | `redis://127.0.0.1:6379/0` |
| KAFKA_CONF_BOOTSTRAP_SERVER | Kafka bootstrap server | `127.0.0.1:9092` |
| KAFKA_CONF_AUTO_OFFSET_RESET | Kafka auto offset reset | `earliest` |
