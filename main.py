from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine
from models import Document
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional 
from enum import Enum
from authentication import get_password_hash,verify_password,create_access_token,decode_access_token
from schema import UserCreate
from models import User
from fastapi.security import OAuth2PasswordBearer

# This tells FastAPI to look for a token in the request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from database import base, engine
base.metadata.create_all(bind=engine)

app = FastAPI()

class DocumentCreate(BaseModel):
    file_name: str
    file_path: str
    file_type: str
    user_id: int

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/documents")
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = Document(
        file_name=document.file_name,
        file_path=document.file_path,
        file_type=document.file_type,
        user_id=document.user_id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    results = db.query(Document).all()
    return results

@app.get("/documents/{document_id}")
def get_document(document_id : int , db: Session = Depends(get_db)):
    results = db.query(Document).filter(Document.id == document_id).first()
    if results is None:
      raise HTTPException(status_code=404, detail="Document not found")
    return results 

class DocumentStatus(str,Enum):
  pending = "pending"
  processed = "processed"
  failed = "failed"

class DocumentUpdate(BaseModel): 
  file_name: Optional[str] = None 
  file_path:Optional[str] = None 
  file_type:Optional[str] = None 
  user_id:Optional[int] = None 
  status:Optional[DocumentStatus] = None

@app.put("/documents/{document_id}")
def update_document(document_id: int, document: DocumentUpdate , db: Session = Depends(get_db)):
   results = db.query(Document).filter(Document.id == document_id).first()

   if results is None:
         raise HTTPException(status_code=404, detail="Document not found")
   if document.file_name is not None:
    results.file_name = document.file_name
   if document.status is not None:
    results.status = document.status
   if document.file_path is not None:
    results.file_path = document.file_path
   if document.file_type is not None:
    results.file_type = document.file_type
   if document.user_id is not None:
    results.user_id = document.user_id

   db.commit()
   db.refresh(results)
   return results

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    results = db.query(Document).filter(Document.id == document_id).first()
    if results is None:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(results)
    db.commit()
    return {"message": "Document deleted successfully"}

@app.post("/signup")
def signup_user(user: UserCreate,db: Session = Depends(get_db)):
    hashed = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
def login_user(user_credentials: UserCreate,db: Session = Depends(get_db)):
   client_email = user_credentials.email
   client_password = user_credentials.password
   user = db.query(User).filter(User.email == client_email).first()
   if user is None:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
   is_valid_password = verify_password(client_password,user.hashed_password)
   if is_valid_password is False:
               raise HTTPException(status_code=401, detail="Incorrect email or password")
   access_token = create_access_token(data={"sub":user_credentials.email})
   return {"access_token":access_token,"token_type":"bearer"}

@app.get("/protected-data")
def get_protected_data(token: str = Depends(oauth2_scheme)):
    # 1. Verify the token isn't forged or expired
    payload = decode_access_token(token)
    # 2. If verification fails (returns None), kick them out
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    # 3. If valid, let them see the data!
    return {"message": "You are in!", "user_email": payload.get("sub")}

   
   