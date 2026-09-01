from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

# users details table blue print
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

# recipes details table blue print
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    ingredients = Column(String(1000))
    instructions = Column(String(2000))
    user_id = Column(Integer, nullable=False)
    price=Column(Integer, nullable=False)

# cart recipes table
class Cart(Base):
    __tablename__="cart_table"

    id= Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    quantity=Column(Integer, nullable=False)
    recipe = relationship("Recipe")
    user = relationship("User")