import boto3
from dotenv import load_dotenv
import os

# 1. Cargamos el .env
load_dotenv()

# 2. Creamos la conexión con el servicio SNS de Amazon
sns = boto3.client(
    'sns',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# 3. El ARN (la dirección única) de tu megáfono
topic_arn = os.getenv('SNS_TOPIC_ARN')


def enviar_alerta():
    try:
        print(f"📢 Conectando con Amazon SNS...")

        # Publicamos el mensaje en el tópico
        respuesta = sns.publish(
            TopicArn=topic_arn,
            Subject='🚨 ALERTA NEXUS: Prueba de Sistema',
            Message='¡Atención Mauro! El sistema de alertas por SNS está en línea y respondiendo perfectamente.'
        )

        print(f"✅ ¡Alerta publicada con éxito!")
        print(f"🆔 ID del mensaje en SNS: {respuesta['MessageId']}")

    except Exception as e:
        print(f"❌ Error al enviar la alerta: {e}")


if __name__ == "__main__":
    enviar_alerta()