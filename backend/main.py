from fastapi import FastAPI, Form
from backend.models import YoutubeURL
from fastapi.responses import JSONResponse
from backend.index import get_docs, split_text
from backend.vector import create_vectorstore, get_vectorstore
from backend.chain import build_chain
app = FastAPI()

@app.get('/')
def home():
    return {"message": "Youtube transcript QnA"}

@app.post('/upload')
def upload(youtube_url: YoutubeURL):
    id = youtube_url.id

    document = get_docs(id)
    chunks = split_text(document)

    vector_store = create_vectorstore(chunks)

    return JSONResponse(content = {'message': 'url uploaded successfully','id':id},status_code=200)

@app.post('/answer')
def question(question: str = Form(...)):
    vectorstore = get_vectorstore()
    chain = build_chain(vectorstore)

    response = chain.invoke(question)
    return JSONResponse(content={'answer':response},status_code=200)

