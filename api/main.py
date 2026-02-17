from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from .core.security import validate_api_key
from .services.ollama_client import OllamaClient
from .services.sanitization import sanitize_ai_response

app = FastAPI(title="Kitsu Fintech Engine", version="2.0.0")
ollama = OllamaClient()

class InvoiceInput(BaseModel):
    content: str

class InvoiceResponse(BaseModel):
    vendor: Optional[str]
    tax_id: Optional[str]
    total: float
    currency: str
    employee: Optional[str]
    description: Optional[str]

@app.get("/")
def health_check():
    return {"status": "online", "message": "Kitsu Engine is running"}

@app.post("/process-invoice", dependencies=[Depends(validate_api_key)])
async def process_invoice(invoice: InvoiceInput):
    try:
        # 1. AI Inference
        raw_output = await ollama.extract_invoice_data(invoice.content)

        # 2. Sanitization
        clean_data = sanitize_ai_response(raw_output)

        # 3. Validated Return
        return {"result": InvoiceResponse(**clean_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))