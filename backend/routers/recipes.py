from fastapi import APIRouter
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Recipe, User,Cart
from schemas import RecipeCreate
from auth import get_current_user

router = APIRouter()

# @router.get("/recipes")
# def recipes():
#     return {"message": "Recipes"}

@router.post("/recipes")
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        user_id=current_user.id,
        price=recipe.price
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe
@router.get('/get_recipies')
def display_recipe(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    recipes=db.query(Recipe).all()
    return {"all recipes":recipes}

@router.get("/get_recipe/{recipe_id}")
def get_recipe_id(recipe_id:int,
                db:Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    recipe=db.query(Recipe).filter(Recipe.id==recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )
    return recipe

# PUT    /recipes/{id}      ← Update recipe

@router.put('/put_recipe/{recipe_id}')
def update_recipe(recipe_id:int,
                recipe: RecipeCreate,
                db:Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    user=db.query(Recipe).filter(Recipe.user_id==current_user.id,Recipe.id==recipe_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="user and Recipe not match"
        )
    user.title = recipe.title
    user.description = recipe.description
    user.ingredients = recipe.ingredients
    user.instructions = recipe.instructions
    user.price=recipe.price

    db.commit()
    db.refresh(user)

    return {
        "message": "Recipe updated successfully",
        "recipe": user
    }

@router.delete('/delete/{recipe_id}')
def delete_recipe(recipe_id:int,db:Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    recipe=db.query(Recipe).filter(Recipe.id==recipe_id,Recipe.user_id==current_user.id).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )
    db.delete(recipe)
    db.commit()

    return {
        "message": "Recipe deleted successfully",
        # "recipe": recipe
    }

@router.get('/all_mine')
def my_recipe(db:Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    mine=db.query(Recipe).filter(Recipe.user_id==current_user.id).all()
    if not mine:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )
    return{"my_recipes":mine}
