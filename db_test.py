from database import base, engine
from models import Document

from sqlalchemy.orm import sessionmaker
sessionlocal = sessionmaker(bind=engine)
session = sessionlocal()

from sqlalchemy import Column,String,Integer
class test_users(base):
    __tablename__ = "test_users"
    id = Column(Integer,primary_key = True)
    name = Column(String)

base.metadata.create_all(engine)

new_user = test_users(name = "Sajawal")
session.add(new_user)
session.commit()

results = session.query(test_users).all()
for user in results:
    print(user.id,user.name)