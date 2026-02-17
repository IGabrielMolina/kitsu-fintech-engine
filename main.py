import httpx
import json
import os
from fastapi import FastAPI, Security, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security.api_key import APIKeyHeader # <--- Corregido: solo este

app = FastAPI()

# Leemos la clave desde el .env (inyectado por Docker)
API_KEY = os.getenv("FINTECH_API_KEY", "nbii3%gWhbr2f!!dveGt974h9")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# ---------------------------- Schemes -----------------------
class FacturaInput(BaseModel):
    contenido: str

# --------------------------- Security -----------------------

async def validar_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="No autorizado, cara de perro")

# --------------------------- Main code ----------------------

@app.get("/")
def home():
    return {"mensaje": "Hola, el motor está vivo y protegido"}

@app.post("/factura")
async def procesar_factura(factura: FacturaInput, api_key: str = Depends(validar_api_key)):
    instrucciones = """
    Actúa como un contador experto auditando gastos corporativos. Tu tarea es extraer información estructurada del texto de una factura o ticket.

    Reglas ESTRICTAS de extracción:
    1. proveedor: Busca la entidad legal (S.A., S.R.L., Inc). Si es un ticket de recital, el proveedor suele ser la ticketera (ej: Movistar Arena, Ticketek), no el artista.
    2. cuit: DEBE tener formato de CUIT argentino (2 números, guion, 8 números, guion, 1 número) o ser una secuencia de 11 dígitos numéricos. Si lo que ves es un código    alfanumérico largo (como '03BAA...'), ESO NO ES UN CUIT, devuélvelo como null o string vacío.
    3. total: El monto final a pagar. Usa punto para decimales.
    4. moneda: ARS, USD, EUR.
    5. empleado: Busca etiquetas como "Nombre", "Comprador" o "Titular" para identificar quién hizo el gasto.
    6. descripcion: Breve resumen de qué se compró.

    Devuelve SOLO un JSON con este formato:
    {
        "proveedor": string,
        "cuit": string (o null),
        "total": number,
        "moneda": string,
        "empleado": string,
        "descripcion": string
    }
    """

    pedido = {
        "model": "qwen2.5:14b",
        "system": instrucciones,
        "prompt": factura.contenido,
        "stream": False,
        "format": "json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=pedido, timeout=None)
        resultado_ia = response.json()
        respuesta_texto = resultado_ia.get("response")

    try:
        resultado_final = json.loads(respuesta_texto)
        return {"Resultado": resultado_final}
    except Exception as e:
        return {
            "error": "La IA no devolvió un formato válido",
            "detalle": str(e),
            "raw": respuesta_texto
        }
