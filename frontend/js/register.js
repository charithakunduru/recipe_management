let un=document.getElementById("username")
let em=document.getElementById("email")
let pwd=document.getElementById("password")
let btn=document.querySelector("button")

btn.addEventListener("click",async (e)=>{
    e.preventDefault();
    if(un.value!="" && em.value!="" && pwd.value!=""){
        
        let n_user={
            username:un.value,
            email:em.value,
            password:pwd.value
        } 
        try{
            let response=await fetch("https://backend-94supzxot-charitha-kundurus-projects.vercel.app/register",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(n_user)

            })
            let data=await response.json()
            console.log("Status:", response.status);
            console.log("OK:", response.ok);
            console.log("Data:", data);            
            if(response.ok){
                alert("use registered successfully")
                un.value=""
                pwd.value=""
                em.value=""
                // window.location.href="login.html"
            }
            else{
                alert(data.detail || "registration failed")
            }

        }
        catch(error){
            alert("404 error")                        
        }       
}
    else{
        alert("plz fill the details")
    }

})