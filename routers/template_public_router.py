from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.security_code_schema import SecurityCodeRequest
import os
import requests
from dotenv import load_dotenv
import uuid
load_dotenv()

router = APIRouter(prefix="/api/v1/template-public", tags=["TEMPLATES PUBLIC"])

@router.post("/security-code")
def security_code(data:SecurityCodeRequest):
    if data.pssw != "72580644-a24c-4862-8a06-29d9c1925617":
        return JSONResponse(content={"error": "Invalid password"}, status_code=400)
    if data.telefono != "51965938082" and data.telefono != "51901981127":
        return JSONResponse(content={"error": "Número de teléfono no permitido"}, status_code=400)
    telefono_str=str(data.telefono)
    version=os.getenv("VERSION_WPP_API")
    phone_number_id=os.getenv("ID_PHONE_NUMER_WPP")
    token=os.getenv("TOKEN_WPP")
    url = f"https://graph.facebook.com/{version}/{phone_number_id}/messages"
    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefono_str,
        "type": "template",
        "template": {
            "name": "codigo_verificacion",
            "language": {
                "code": "es_PE"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": data.codigo
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": data.codigo
                        }
                    ]
                }
            ]
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response=requests.post(url, json=body, headers=headers)

    if not response.ok:
        print("status_code:",response.status_code)
        print("response_text:",response.text)
        return JSONResponse(content={"error":response.text},status_code=500)
    return {
        "status": response.status_code,
        "response_text": response.text
    }
