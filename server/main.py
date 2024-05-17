import traceback

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .pre_process.embed import embed
from .infer.infer import query as run_query

app = FastAPI(app_name='rag-sample-impl')
app.debug = True

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    question: str
    history: Optional[list[str]] = []

@app.get('/')
def index():
    return {"response": "Not supported"}
    
@app.post('/embed')
def do_embed():
    try:
        embed()
        return {"response": "Done"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/infer')
def do_infer(chat_query: ChatQuery):
    question = chat_query.question
    history = chat_query.history
    try:
        res = run_query(question=question, history=history)
        return {'response': res}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))