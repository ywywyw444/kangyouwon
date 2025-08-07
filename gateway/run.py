import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.router.main:app",
        host=os.getenv("GATEWAY_HOST", "0.0.0.0"),
        port=int(os.getenv("GATEWAY_PORT", 8080)),
        reload=os.getenv("GATEWAY_RELOAD", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
