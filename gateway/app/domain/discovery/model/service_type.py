from enum import Enum

class ServiceType(Enum):
    AUTH = "auth"
    CHATBOT = "chatbot"
    MATERIALITY = "materiality"
    GRI = "gri"
    GRIREPORT = "grireport"
    TCFD = "tcfd"
    TCFDREPORT = "tcfdreport"
    SURVEY = "survey"
