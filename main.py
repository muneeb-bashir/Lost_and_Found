from sqlalchemy.orm import Session
import json
from datetime import date
from fastapi import FastAPI, Depends , responses
from database import SessonLocal, engine
from typing import Optional
from sqlalchemy import or_
from models import models, schemas
from validators import username_valid, password_is_valid, email_is_valid
app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/create_user')
def create_user(name: str, email: str,password: str, contact :str, db: Session = Depends(get_db)):
        """
    sends a POST request .
    takes username and password.
    checks empty entries in username and password.
    if a user exists, returns a 409 authentication error.
    validates password with password regex.
    :return: user id with 201 response status.
    """
    if not name:
        return json.dumps({"msg": "missing username"}), 400

    if not password:
        return json.dumps({"msg": "missing password"}), 400

    if not email:
        return json.dumps({"msg": "missing email"}), 400

    if not contact:
        return json.dumps({"msg": "missing contact"}), 400

    if db.query(models.User).filter(models.User.email == email).first():
        return json.dumps({"msg": "Email  already exist"}), 409

    if not email_is_valid(email):
        return json.dumps({"msg": "Invalid email Format"})

    if username_valid(name):
        return json.dumps({"msg": "Invalid username"}), 400

    if not password_is_valid(password):
        return json.dumps({"msg": "Invalid password format."}), 400
    
    existing_user = db.query(models.User).filter(models.User.name == request.name).first()
    if existing_user:
        response= json.dumps({'ERROR':'USER WITH NAME ALREADY EXISTS IN DATABASE'}) 
        return response
    
    new_user= models.User(name=request.name, email=request.email, password=request.password, contact=request.contact)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return json.dumps({'user_id': new_user.id}), 201

@app.get('/login')
def login( username: str, password: str, db: Session = Depends(get_db)):
        """
    sends a GET request.
    takes username and password.
    checks if user exists and password matches.
    :return: success message
    """
    if not username:
        return json.dumps({"msg": "missing username"}), 400

    if not password:
        return json.dumps({"msg": "missing password"}), 400

    existing_user = db.query(models.User).filter(models.User.name == username).first()

    if not existing_user:
        return json.dumps({"msg": "User does not exist"}), 404

    if existing_user.password != password:
        return json.dumps({"msg": "Wrong Password"}), 401

    return json.dumps({"msg": "Login successful"})


@app.post('/add_item')
def create_item(request : schemas.Item, db: Session = Depends(get_db)):
        """This function takes item name ,
    description as input and put the all these
    details in database in order to create a new item.
    """
    newitem= models.Item(name=request.name, description=request.description, status= request.status, 
    lost_location=request.lostlocation, found_location=request.foundlocation, date=request.Date, user_id=request.user_id)
    
    db.add(newitem)
    db.commit()
    db.refresh(newitem)

    return newitem


@app.get('/item')
  """This function takes no argument ,
    and provies details in database to view all Items.
    """
def view_item(db: Session = Depends(get_db)):
    Item = db.query(models.Item).all()
    return Item

@app.get('/search_Item')
def search(id: Optional[int]=None, name: Optional[str]="", location: Optional[str]="" , db: Session = Depends(get_db)):
    
    item = db.query(models.Item).filter(or_(models.Item.id == id, models.Item.name == name, models.Item.lost_location == location, models.Item.Found_Location == location)).all()

    return item

@app.put('/update_Item')
def search(id: int,name: Optional[str]="", description: Optional[str]="", status: Optional[bool]="", 
    lost_location : Optional[str]="" ,found_location : Optional[str]="", date: Optional[date]="",db: Session = Depends(get_db)):
    """This function takes Id as input to update
      the Item details include description,
      name and all details.
      """

    existing_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not existing_item:
        return json.dumps({'Error':'Item with id does not exist'})
 
    if name:
        existing_item.name = name

    if  lost_location:
        existing_item.lost_location = lost_location
    
    if found_location:
        existing_item.found_location = found_location

    if description:
        existing_item.description = description

    if date:
        existing_item.date = date
        
    db.commit()
    db.refresh(existing_item)

    return ("ITEM UPDATED SUCCESSFULLY", existing_item)


@app.delete('/delete_item')
def delete_item(id:int, db: Session = Depends(get_db)):
    """This functions takes the id delete the required item """
    existing_item = db.query(models.Item).filter(models.Item.id == id).delete()
     
    if not existing_item :
         
        return("Item Does Not Exist ")

    db.commit()

    return("Item deleted with coressponding Id",id)

    

