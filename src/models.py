from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

followers_table = Table(
    "followers",
    db.metadata,
    Column("follower_id", ForeignKey('user.id'), primary_key=True),
    Column("follow_id", ForeignKey('user.id'), primary_key=True),
)

class User(db.Model):
    __tablemname___ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user") 


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(String(200), nullable=False)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content
        }
    
class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

class Media (db.Model):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }
    


