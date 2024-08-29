from pydantic import BaseModel
import pymongo
import traceback
import os
import sys
import uuid
from typing import List
from flask import Flask, request, jsonify
import boto3
import awswrangler as wr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_community.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain

# Environment variables
OPENAI_API_KEY = ""
S3_KEY = ""
S3_SECRET = ""
S3_BUCKET = ""
S3_REGION = ""
S3_PATH = ""

# MongoDB setup
try:
    MONGO_URL = "mongodb+srv://admin:admin@cluster0.jyupp.mongodb.net/?retryWrites=true&w=majority&ssl=true"
    client = pymongo.MongoClient(MONGO_URL, uuidRepresentation="standard")
    db = client["chat_with_doc"]
    conversationcol = db["chat-history"]
    conversationcol.create_index([("session_id")], unique=True)
except:
    print(traceback.format_exc())
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

app = Flask(__name__)

# AWS S3 session
aws_s3 = boto3.Session(
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name=S3_REGION,
)

class ChatMessageSent(BaseModel):
    session_id: str = None
    user_input: str
    data_source: str

def get_response(
    file_name: str,
    session_id: str,
    query: str,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0,
):
    print("file name is ", file_name)
    file_name = file_name.split("/")[-1]
    embeddings = OpenAIEmbeddings()
    wr.s3.download(path=f"s3://docchat/documents/{file_name}", local_file=file_name, boto3_session=aws_s3)
    
    if file_name.endswith(".docx"):
        loader = Docx2txtLoader(file_path=file_name)
    else:
        loader = PyPDFLoader(file_name)
    
    data = loader.load()
    print("splitting ..")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, separators=["\n", " ", ""]
    )
    all_splits = text_splitter.split_documents(data)
    vectorstore = FAISS.from_documents(all_splits, embeddings)
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectorstore.as_retriever(),
    )
    with get_openai_callback() as cb:
        answer = qa_chain(
            {
                "question": query,
                "chat_history": load_memory_to_pass(session_id=session_id),
            }
        )
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        answer["total_tokens_used"] = cb.total_tokens
    return answer

def load_memory_to_pass(session_id: str):
    data = conversationcol.find_one({"session_id": session_id})
    history = []
    if data:
        data = data["conversation"]
        for x in range(0, len(data), 2):
            history.extend([(data[x], data[x + 1])])
    print(history)
    return history

def get_session() -> str:
    return str(uuid.uuid4())

def add_session_history(session_id: str, new_values: List):
    document = conversationcol.find_one({"session_id": session_id})
    if document:
        conversation = document["conversation"]
        conversation.extend(new_values)
        conversationcol.update_one(
            {"session_id": session_id}, {"$set": {"conversation": conversation}}
        )
    else:
        conversationcol.insert_one(
            {
                "session_id": session_id,
                "conversation": new_values,
            }
        )

@app.route("/chat", methods=["POST"])
def create_chat_message():
    try:
        data = request.json
        chats = ChatMessageSent(**data)
        if chats.session_id is None:
            session_id = get_session()
            payload = ChatMessageSent(
                session_id=session_id,
                user_input=chats.user_input,
                data_source=chats.data_source,
            )
            response = get_response(
                file_name=payload.data_source,
                session_id=payload.session_id,
                query=payload.user_input,
            )
            add_session_history(
                session_id=session_id,
                new_values=[payload.user_input, response["answer"]],
            )
            return jsonify({
                "response": response,
                "session_id": str(session_id),
            })
        else:
            payload = ChatMessageSent(
                session_id=str(chats.session_id),
                user_input=chats.user_input,
                data_source=chats.data_source,
            )
            response = get_response(
                file_name=payload.data_source,
                session_id=payload.session_id,
                query=payload.user_input,
            )
            add_session_history(
                session_id=str(chats.session_id),
                new_values=[payload.user_input, response["answer"]],
            )
            return jsonify({
                "response": response,
                "session_id": str(chats.session_id),
            })
    except Exception:
        print(traceback.format_exc())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({"error": "An unexpected error occurred"}), 204

@app.route("/uploadFile", methods=["POST"])
def uploadtos3():
    data_file = request.files['data_file']
    filename = data_file.filename
    try:
        data_file.save(filename)
        wr.s3.upload(
            local_file=filename,
            path=f"s3://{S3_BUCKET}/{S3_PATH}{filename}",
            boto3_session=aws_s3,
        )
        os.remove(filename)
        response = {
            "filename": filename,
            "file_path": f"s3://{S3_BUCKET}/{S3_PATH}{filename}",
        }
        return jsonify(response)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
