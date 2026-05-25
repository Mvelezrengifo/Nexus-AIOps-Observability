import json
import logging
import boto3  # La vieja confiable que pidió Alya
from typing import Any
from datetime import datetime, timezone
import uuid

from app.config import settings

# Usamos el logger estándar para evitar líos de importación por ahora
logger = logging.getLogger(__name__)


class EventBusClient:
    def __init__(self) -> None:
        self._initialized = False
        self._sqs_client = None
        self._use_aws = False

    def initialize(self) -> None:
        """Inicialización síncrona y robusta con Boto3."""
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            try:
                # Creamos el cliente de AWS de forma tradicional
                self._sqs_client = boto3.client(
                    "sqs",
                    region_name=settings.aws_region,
                    aws_access_key_id=settings.aws_access_key_id,
                    aws_secret_access_key=settings.aws_secret_access_key
                )
                self._use_aws = True
                logger.info("🚀 NEXUS EventBus: Conectado a AWS SQS exitosamente")
            except Exception as e:
                logger.error(f"❌ Error al conectar con AWS: {e}")
                self._use_aws = False
        else:
            logger.warning("⚠️ NEXUS EventBus: Trabajando en MODO LOCAL (Sin credenciales)")

        self._initialized = True

    def publish(self, event_type: str, data: dict[str, Any], subject: str | None = None) -> dict[str, Any]:
        """Publica el evento. Aunque es síncrono, FastAPI lo maneja bien."""
        if not self._initialized:
            self.initialize()

        message = {
            "event_type": event_type,
            "data": data,
            "subject": subject or "NEXUS_EVENT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message_id": str(uuid.uuid4())
        }

        if self._use_aws and self._sqs_client and settings.aws_sqs_queue_url:
            return self._publish_to_sqs(message)

        return self._publish_local(message)

    def _publish_to_sqs(self, message: dict[str, Any]) -> dict[str, Any]:
        try:
            # Envío directo y simple
            response = self._sqs_client.send_message(
                QueueUrl=settings.aws_sqs_queue_url,
                MessageBody=json.dumps(message)
            )
            logger.info(f"✅ Evento enviado a la nube: {message['event_type']}")
            return {"success": True, "message_id": response["MessageId"], "provider": "aws_sqs"}
        except Exception as e:
            logger.error(f"❌ Falló el envío a SQS: {str(e)}")
            return self._publish_local(message)

    def _publish_local(self, message: dict[str, Any]) -> dict[str, Any]:
        # Esto saldrá en tu consola de PyCharm
        logger.info(f"☁️ EVENTO LOCAL (Simulado): {message['event_type']}")
        return {"success": True, "message_id": message["message_id"], "provider": "local"}


# Singleton simple
_event_bus_client = None


def get_event_bus() -> EventBusClient:
    global _event_bus_client
    if _event_bus_client is None:
        _event_bus_client = EventBusClient()
        _event_bus_client.initialize()
    return _event_bus_client