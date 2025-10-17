# **Whisper Service**

**Servicio orquestador para transcripción de audio.**
Este servicio actúa como intermediario entre el orquestador y whisper-model, gestionando las peticiones de transcripción de audio, validando archivos y procesando respuestas.

## **Resumen**
**Whisper Service** se encarga de:
- **Recibir** archivos de audio del orquestador
- **Validar** el formato de audio (WAV)
- **Comunicarse** con whisper-model
- **Procesar** las transcripciones
- **Formatear** y entregar los resultados textuales

---

## **Tecnologías principales**
- FastAPI
- Pydantic para validación
- httpx para comunicación asíncrona
- Python 3.10+
- Docker
- python-multipart para manejo de archivos

---

## **Estructura del proyecto**
```
whisper-service/
├── Dockerfile
├── requirements.txt
├── .env
└── app/
    ├── main.py              # Punto de entrada FastAPI
    ├── infrastructure/
    │   └── routes.py        # Endpoints HTTP
    ├── application/
    │   └── transcriber_client.py       # Lógica de comunicación con whisper-model
    ├── core/
    │   ├── config.py        # Configuración
    │   └── logging_config.py
    └── domain/
        └── models.py        # Modelos Pydantic
```

---

## **Endpoints**

### **GET /health**
Verifica:
- Estado del servicio
- Conectividad con whisper-model
- Configuración activa

### **POST /transcribe**
Endpoint principal que:
1. Recibe archivo de audio (WAV)
2. Valida formato y tamaño
3. Comunica con whisper-model
4. Procesa respuesta
5. Retorna transcripción

**Entrada:**
```
Multipart form data:
- file: archivo WAV
```

**Respuesta:**
```json
{
    "texto_transcrito": "Este es el texto transcrito del audio",
    "duracion_audio": "00:00:15",
    "tiempo_proceso": 0.234,
    "modelo_usado": "whisper-large-v3"
}
```

---

## **Docker — Build & Run**

1) Construir:
```sh
docker build -t whisper-service:latest ./whisper-service
```
> **Nota:** la imagen resultante pesa aproximadamente **1.2 GB**.

2) Ejecutar:
```sh
docker run --rm --name whisper-service \
    -p 8003:8003 \
    --env-file .env \
    whisper-service:latest
```

---

## **Configuración**
- Ajustar variables en `.env` y `config.py` según tu entorno:
  - URLs de servicios
  - Puertos
  - Timeouts
  - Límites de tamaño de archivo
  - Niveles de logging

---

## **Integración y dependencias**
- Requiere acceso a **whisper-model**
- Diseñado para trabajar con el orquestador principal
- Compatible con orquestación via docker-compose
- Se integra en el pipeline completo para procesamiento de audio

---

## **Notas operativas**
- Servicio stateless
- Optimizado para procesamiento asíncrono
- Incluye circuit breakers para fallos de whisper-model
- Logging estructurado para monitoreo
- Manejo de archivos temporales para procesamiento de audio
