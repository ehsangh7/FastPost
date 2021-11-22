from .. import models, schema, utils, database, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model = List[schema.PostOut])
def get_posts(db: Session = Depends(database.get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              search: Optional[str] = "",
              limit: int = 10,
              skip: int = 0,
              ):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Raw Sql
    # select posts.* , COUNT(votes.post_id)  from posts LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;
    results = db.query(models.Post, func.count(models.Vote.post_id)
                                            .label("votes")
                                            ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                                            ).group_by(models.Post.id
                                            ).filter(models.Post.title.contains(search)
                                            ).limit(limit).offset(skip
                                            ).all()
    
    return results

@router.get("/{id}", response_model = schema.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    # ORM
    print("userId",current_user)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id)
                                            .label("votes")
                                            ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                                            ).group_by(models.Post.id
                                            ).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"couldn't find post {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"couldn't find post {id}"}
    return post



# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schema.Post)
def create_post(post: schema.PostCreate,
                db: Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #ORM
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.dict())

    db.add(new_post) 
    db.commit()
    db.refresh(new_post)

    return new_post



# UPDATE
@router.put("/{id}", response_model = schema.Post)
def update_post(id: int, 
                post: schema.PostCreate, 
                db: Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()

    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")
    print(updated_post)
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
    
    updated_post.update(post.dict(), synchronize_session=False)
    
    db.commit()

    return updated_post.first()



# DELETE 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()

    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    # conn.commit()

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

