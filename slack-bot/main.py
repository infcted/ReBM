import asyncio
import logging
import sys
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from config import Config
from rebm_client import ReBMClient
from slack_handlers import SlackBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        Config.validate()
        rebm_client = ReBMClient()
        if not await rebm_client.health_check():
            logger.error("Failed to connect to ReBM API.")
            return
        app = AsyncApp(token=Config.SLACK_BOT_TOKEN, signing_secret=Config.SLACK_SIGNING_SECRET)
        assert Config.SLACK_BOT_TOKEN is not None  # Validated by Config.validate()
        SlackBot(app, rebm_client, Config.SLACK_BOT_TOKEN)
        handler = AsyncSocketModeHandler(app, Config.SLACK_APP_TOKEN)
        await handler.start_async()
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
    finally:
        if 'rebm_client' in locals():
            await rebm_client.close()

if __name__ == "__main__":
    asyncio.run(main()) 