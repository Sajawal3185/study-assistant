from database import base 
from sqlalchemy  import Column,Integer,String,DateTime,ForeignKey
from datetime import datetime

class Document(base):
    __tablename__ = "documents"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    file_name = Column(String)
    file_type = Column(String)
    file_path = Column(String)
    status = Column(String)
    uploaded_at = Column(DateTime,default = datetime.utcnow)

class User(base): 
 __tablename__ = "users" 
 id = Column(Integer,primary_key = True)
 email = Column(String, unique=True,nullable=False)
 hashed_password = Column(String,nullable=False)
 created_at = Column(DateTime,default = datetime.utcnow)