import os
from typing import Optional

class Settings:
    def __init__(self):
        self.gateway_host = os.getenv("GATEWAY_HOST", "0.0.0.0")
        self.gateway_port = int(os.getenv("GATEWAY_PORT", 8080))
        self.gateway_reload = os.getenv("GATEWAY_RELOAD", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Service URLs
        self.gateway_service_url = os.getenv("GATEWAY_SERVICE_URL")
        self.chatbot_service_url = os.getenv("CHATBOT_SERVICE_URL")
        self.materiality_service_url = os.getenv("MATERIALITY_SERVICE_URL")
        self.gri_service_url = os.getenv("GRI_SERVICE_URL")
        self.grireport_service_url = os.getenv("GRIREPORT_SERVICE_URL")
        self.tcfd_service_url = os.getenv("TCFD_SERVICE_URL")
        self.tcfdreport_service_url = os.getenv("TCFDREPORT_SERVICE_URL")
        self.survey_service_url = os.getenv("SURVEY_SERVICE_URL")
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL")
        
        # Redis settings
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db = int(os.getenv("REDIS_DB", 0))
