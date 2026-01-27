from fastapi import APIRouter, Depends, HTTPException, status , Request , Response
from sqlalchemy.orm import Session
from app.database import get_db
from app  import schemas 
from app import models
from app import utils
from app import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router =  APIRouter(tags=['Authentication'])

@router.post("/login" , response_model=schemas.Token)
def login(user_credintials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):


    user = db.query(models.User).filter(
        models.User.email == user_credintials.username).first()

    if user is None :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    
    if not utils.verify(user_credintials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credintial")
    

    # create a Token
    # return Token

    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token,"token_type" :"bearer"}


    
