import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
    REBM_API_URL = os.getenv("REBM_API_URL", "http://localhost:8000")
    REBM_API_TIMEOUT = int(os.getenv("REBM_API_TIMEOUT", "30"))
    BOT_NAME = os.getenv("BOT_NAME", "ReBM Bot")

    @classmethod
    def validate(cls):
        required_vars = [
            "SLACK_BOT_TOKEN",
            "SLACK_SIGNING_SECRET",
            "SLACK_APP_TOKEN"
        ]
        missing = [v for v in required_vars if not getattr(cls, v)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return True 