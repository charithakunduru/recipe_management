from fastapi import APIRouter
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Recipe, User,Cart
from schemas import RecipeCreate
from auth import get_current_user

router = APIRouter()

@router.post('/cart_recipe/{recipe_id}')
def add_cart_recipe(
    recipe_id:int,
    quantity:int,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    recipe=db.query(Recipe).filter(Recipe.id==recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
    )
    cart_recipe = Cart(
        quantity=quantity,
        recipe_id=recipe.id,
        user_id=current_user.id
    )
    db.add(cart_recipe)
    db.commit()
    db.refresh(cart_recipe)

    return {"message":"recipe added to cart successfully",
            "cart_recipe":cart_recipe}


@router.get('/all_cart_recipes')
def cart_recipe(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    cart_items=db.query(Cart).filter(Cart.user_id == current_user.id).all()
    total=0
    result=[]
    for item in cart_items:
        item_total=(item.quantity)*(item.recipe.price)
        total+=item_total
        result.append({
            "cartid":item.id,
            "recipe_id":item.recipe_id,
            "user_id":item.user_id,
            "recipe":item.recipe.title,
            "price":item.recipe.price,
            "qnty":item.quantity,
            "item_total":item_total

        })

    return {"all recipes":result,"total price":total}

# @router.put('/upd_cart/{id}')
# def upd_qnty(
#     id:int,
#     qnty:int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)):
#     cart_item=db.query(Cart).filter(Cart.recipe_id==id,Cart.user_id == current_user.id).first()
#     if not cart_item:
#         raise HTTPException(
#             status_code=404,
#             detail="Recipe not found in cart"
#         )
#     if qnty <= 0:
#         raise HTTPException(
#             status_code=400,
#             detail="Quantity must be greater than 0"
#         )

#     cart_item.quantity=qnty
#     db.commit()
#     db.refresh(cart_item)

#     return {
#         "message": "quantity updated successfully",
#         "recipe": cart_item
#     }


@router.delete('/del_cart_item/{recipe_id}')
def delete_cart_item(
    recipe_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    cart_item=db.query(Cart).filter(Cart.recipe_id==recipe_id,Cart.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found in cart")
    db.delete(cart_item)
    db.commit()

    return {
        "message": "cart_item deleted successfully",
    }