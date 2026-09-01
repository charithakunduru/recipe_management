from pydantic import BaseModel
 # register schema to take input from user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
 # login schema to take input from user
class UserLogin(BaseModel):
    email: str
    password: str

 # creating the recipe schema to take input from user
class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    price:int