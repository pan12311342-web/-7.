import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("MODEL_API_KEY", "")
    base_url: str = os.getenv("MODEL_BASE_URL", "https://api.openai.com/v1")
    model_name: str = os.getenv("MODEL_NAME", "")
    max_image_bytes: int = int(os.getenv("MAX_IMAGE_BYTES", "10000000"))
    max_image_side: int = int(os.getenv("MAX_IMAGE_SIDE", "1600"))

settings = Settings()
