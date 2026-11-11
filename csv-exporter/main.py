from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from converter import json_to_csv
import json

app = FastAPI(title="csv-exporter", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(HTTPException)
async def contract_error(request: Request, error: HTTPException):
    return JSONResponse(
        status_code=error.status_code, 
        content={"error": "INVALID_INPUT", "message":error.detail}
        )




@app.post("/export")
async def export(request: Request):
    try:
        body = json.loads(await request.body())
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.")


    # story3 Validation: RUSSELL


    # extract body fields 
    data = body.get("data")
    columns = body.get("columns")
    filename = body.get("filename", "export.csv")

    if not isinstance(data, list) or not data:
        raise HTTPException(status_code=400, detail="data must be a non-empty array of objects")

    # stories 1 & 2: convert data
    csv_output = json_to_csv(data, columns)

    # return CSV text
    return Response(
        content=csv_output,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
