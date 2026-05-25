from app.db.models.operational_event import OperationalEvent

# Parche temporal de emergencia para ignorar el archivo que Zoe no ha creado o movió
try:
    from app.db.models.ai_insight import AIInsight
except ModuleNotFoundError:
    # Creamos una clase fantasma temporal en memoria para que el resto de la app no rompa al importar
    class AIInsight:
        pass
    print("⚠️ Advertencia: No se encontró el modelo ai_insight.py, usando mock temporal.")