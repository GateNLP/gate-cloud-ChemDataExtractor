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
    
    cems = [annotation(cem) for cem in doc.cems]
    sentences = []
    tokens = []
    
    records = {}
    
    for record in doc.records.serialize():
        for name in record["names"]:
            records[name] = record
            
    for cem in cems:
        if cem["features"]["string"] in records:
            cem["features"] = {**cem["features"], **records[cem["features"]["string"]]}
    
    for element in doc.elements:
        for sentence in element.sentences:
            sentences.append(annotation(sentence))
            posTags = sentence.pos_tagged_tokens
            for i, token in enumerate(sentence.tokens):
                annot = annotation(token)
                annot["features"]["category"]=posTags[i][1]
                annot["features"]["normalized"]=token.lex.normalized
                annot["features"]["length"]=token.lex.length
                tokens.append(annot)
    
    return dict(response = { 'type':'annotations', 'annotations':{'ChemicalEntity':cems, 'Sentence': sentences, 'Token':tokens,'Record':doc.records.serialize()} })
    
def annotation(cem):
    """Converts a Chemical Entity Mention (CME) into an ELG-compliant annotation"""
    return {
      'start':cem.start, 'end':cem.end,
      'features':{'string':cem.text}
    }

