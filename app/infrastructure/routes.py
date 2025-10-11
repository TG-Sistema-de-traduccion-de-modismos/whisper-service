from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile, os, logging
from app.application.transcriber_client import TranscriberClient
from app.domain.models import TranscriptionResponse
from pydub import AudioSegment
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)
transcriber_client = TranscriberClient()


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):

    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser audio")

    tmp_path = None
    wav_path = None

    try:
        suffix = os.path.splitext(file.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            wav_path = tmp_wav.name

        try:
            audio = AudioSegment.from_file(tmp_path)
            audio = audio.set_channels(settings.CHANNELS).set_frame_rate(settings.SAMPLE_RATE)
            audio.export(wav_path, format="wav")
            file_to_send = wav_path
        except Exception as e:
            logger.warning("No se pudo convertir el audio, se envía el original: %s", e)
            file_to_send = tmp_path

        result = transcriber_client.infer_file(file_to_send)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en /transcribe: %s", e)
        raise HTTPException(status_code=500, detail=f"Error procesando audio: {str(e)}")
    finally:
        for f in [tmp_path, wav_path]:
            try:
                if f and os.path.exists(f):
                    os.unlink(f)
            except Exception:
                pass


@router.get("/health")
def health():

    import requests
    try:
        r = requests.get(f"{transcriber_client.base_url}/health", timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {"status": "ok", "model_health": data}
        else:
            return {"status": "degraded", "model_health": None}
    except Exception as e:
        logger.warning("No se pudo contactar al model server: %s", e)
        return {"status": "degraded", "model_health": None}
