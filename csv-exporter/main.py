from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from converter import json_to_csv
from converter import make_safe
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
    # check everything first so bad requests get a 400 instead of crashing (500)

    # body needs to be an object like {"data": [...]}
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object with a data field.")

    if not isinstance(body.get("data"), list):
        raise HTTPException(status_code=400, detail="data must be an array of objects")

    # empty list gets EMPTY_DATA. return instead of raise so the handler
    # above doesn't change it to INVALID_INPUT
    if len(body["data"]) == 0:
        return JSONResponse(status_code=400, content={"error": "EMPTY_DATA", "message": "data must have at least one record"})

    # each row has to be an object
    for record in body["data"]:
        if not isinstance(record, dict):
            raise HTTPException(status_code=400, detail="data must be an array of objects")

    # columns is optional but has to be a list of strings if its there
    columns_sent = body.get("columns")
    if columns_sent is not None:
        if not isinstance(columns_sent, list):
            raise HTTPException(status_code=400, detail="columns must be an array of column names")
        for col in columns_sent:
            if not isinstance(col, str):
                raise HTTPException(status_code=400, detail="columns must be an array of column names")

    # csv injection guard (see make_safe in converter.py)
    body["data"] = make_safe(body["data"])


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
