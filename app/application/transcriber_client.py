import requests
import logging
import mimetypes
import os
from app.core.config import settings

logger = logging.getLogger(__name__)

class TranscriberClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.MODEL_SERVICE_URL

    def infer_file(self, file_path: str, timeout: int | None = None) -> dict:
        timeout = timeout or settings.REQUEST_TIMEOUT
        mime_type = mimetypes.guess_type(file_path)[0] or "audio/wav"

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, mime_type)}
            try:
                logger.info(f"Enviando archivo {file_path} como {mime_type} a {self.base_url}/infer")
                resp = requests.post(f"{self.base_url}/infer", files=files, timeout=timeout)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.exception("Error llamando al modelo: %s", e)
                raise
