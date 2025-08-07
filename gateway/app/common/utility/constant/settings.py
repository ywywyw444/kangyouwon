import os
from typing import Optional

class Settings:
    def __init__(self):
        self.gateway_host = os.getenv("GATEWAY_HOST", "0.0.0.0")
        self.gateway_port = int(os.getenv("GATEWAY_PORT", 8000))
        self.gateway_reload = os.getenv("GATEWAY_RELOAD", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Service URLs
        self.account_service_url = os.getenv("ACCOUNT_SERVICE_URL")
        self.chatbot_service_url = os.getenv("CHATBOT_SERVICE_URL")
        self.company_service_url = os.getenv("COMPANY_SERVICE_URL")
        self.dashboard_service_url = os.getenv("DASHBOARD_SERVICE_URL")
        self.facility_service_url = os.getenv("FACILITY_SERVICE_URL")
        self.kospi_service_url = os.getenv("KOSPI_SERVICE_URL")
        
        # Redis settings
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db = int(os.getenv("REDIS_DB", 0))
