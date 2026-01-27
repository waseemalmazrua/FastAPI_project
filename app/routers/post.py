from app import models,schemas,utils
from fastapi import APIRouter , Depends , status , HTTPException , Response 
from sqlalchemy.orm import Session
from app.database import get_db 
from typing import List , Optional
from app.oauth2 import get_current_user
from app import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)











@router.get("/" ,response_model = List[schemas.PostOUT])
def get_posts(db : Session = Depends(get_db),
              current_user : int = Depends(oauth2.get_current_user),
              limit: int = 10 , skip:int = 0 , search:Optional[str] ="" ):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()



    results = (
    db.query(models.post, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.post.id, isouter=True)
    .group_by(models.post.id).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()
)

    return [
        {
            "Post": post,
            "votes": votes
        }
        for post, votes in results
    ]


#############################################


@router.post("/" , status_code=status.HTTP_201_CREATED ,response_model=schemas.Post) 
def create_posts(post:schemas.PostCreate , db:Session = Depends(get_db) , current_user : int = 
                   Depends(oauth2.get_current_user)):
#     ما يدخل إلى السيرفر ≠ ما يخرج منه

# Input (Request body) → داخل الدالة

# Output (Response body) → في الـ decorator (response_model)

    # cursor.execute(""" INSERT INTO posts (title , content , published) VALUES (%s,%s,%s) RETURNING  * """
    #                ,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
   
    new_post = models.post(owner_id=current_user.id , **post.dict())
        
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




# find a post with id
@router.get("/{id}" ,response_model = schemas.PostOUT)
def get_post(id : int , db: Session = Depends(get_db),
             current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id = %s""" , (str(id),))
    # test_post = cursor.fetchone()

    # post = db.query(models.post).filter(models.post.id == id).first()


    post = db.query(models.post, func.count(models.Vote.post_id).label("votes")
                    ).join(models.Vote, models.Vote.post_id == models.post.id, isouter=True
                           ).group_by(models.post.id).filter(models.post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f' post with id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with  id {id} was not found'}

    post, votes = post

    return {
        "Post": post,
        "votes": votes
    }
    

####################################


# detele 

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """ , (id,))
    # deleted_post = cursor.fetchone()
    
    post_query = db.query(models.post).filter(models.post.id ==id)

    post = post_query.first()




    if post  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the index id {id} not found')
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" non autherize to perform requested action")
    # conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# ubdate

@router.put("/{id}" ,response_model=schemas.Post)
def update_post(id :int , updated_post : schemas.PostCreate , db : Session = Depends(get_db),
                 current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
    #                (post.title,post.content,post.published,id))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.post).filter(models.post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" the post id number {id} not found")
    

    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" non autherize to perform requested action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
    
