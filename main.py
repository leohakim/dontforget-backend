import uvicorn
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# RUN THE APP
if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
    )
