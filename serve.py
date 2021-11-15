from logging import getLogger
import os

import requests

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

from chemdataextractor import Document

LOGGER = getLogger(__name__)

app = FastAPI(root_path=os.environ.get('ROOT_PATH'))

class TextRequest(BaseModel):
    type: str
    features: Optional[dict] = None
    content: str
    mimeType: str

@app.post("/")
async def processPOST(request: TextRequest):
    text = request.content
    
    # get the binary data from the request body
    doc = Document(text)
    
    cems = [cem_annotation(cem) for cem in doc.cems]
    
    return dict(response = { 'type':'annotations', 'annotations':{'ChemicalEntity':cems} })
    
def cem_annotation(cem):
    """Converts a Chemical Entity Mention (CME) into an ELG-compliant annotation"""
    return {
      'start':cem.start, 'end':cem.end,
      'features':{'string':cem.text}
    }

