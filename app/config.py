from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+aiomysql://user:pass@localhost:3306/erp"
    # JWT
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_USE_OPENSSL_RAND_HEX_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "https://mekapt-ays.netlify.app"]
    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = "+14155238886"
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    # Apartment
    APARTMAN_ADI: str = "Paşa Apartmanı"
    APARTMAN_ADRES: str = "Yayla Mah. 1396 Sok. No:4, Keçiören/ANKARA"
    APARTMAN_TELEFON: str = "0530 233 29 64"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()
