let cartitems=document.querySelector(".cartitems")
async function demo(){
    let token=localStorage.getItem("token")
    if(!token){
        alert("user not yet login")
        return
    }
    try{
        let response=await fetch("http://127.0.0.1:8000/all_cart_recipes",{
            method:"GET",
            headers:{
                "authorization":`Bearer ${token}`
            }
        })
        let data=await response.json()
        let cart=data["all recipes"]
        let money=data["total price"]
        if(response.ok){
            cartitems.innerHTML = ""
            cart.forEach((item)=>{
                cartitems.innerHTML+=`
                <h2>recipe_name:${item.recipe}</h2>
                <h3>price:${item.price}</h3>
                <p>quantity:${item.qnty}</p>
                <h3>total:${item.item_total}</h3>
                <button type="button" class="del" data-id="${item.recipe_id}" onclick="console.log('INLINE CLICK WORKS')">delete</button>
                <hr>
                `               
            })
            cartitems.addEventListener("click", async (event) => {

    if (!event.target.classList.contains("del")) {
        return;
    }

    console.log("🔥 DELETE BUTTON CLICKED");

    let recipeID = event.target.dataset.id;

    console.log("Recipe ID:", recipeID);

    let token = localStorage.getItem("token");

    try {

        let response = await fetch(
            `http://127.0.0.1:8000/del_cart_item/${recipeID}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        let data = await response.json();

        console.log("Status:", response.status);
        console.log("Response:", data);

        if (response.ok) {

            alert("cart item deleted successfully");

            await demo();

        } else {

            alert(data.detail || "recipe not found");

        }

    } catch (error) {

        console.log("ERROR:", error);
        alert(error.message);

    }
});
            
            cartitems.innerHTML+=`
            <h1>total price:${money}</h1>
            `
            
        }
        
        else{
            alert(data.detail || "cart item not found")
        }
    }
    catch(error){
        alert(error.message)
    }
}


demo()