let em=document.querySelector("#email")
let pwd=document.querySelector("#password")
let btn=document.querySelector("button")

btn.addEventListener("click",async (e)=>{
    e.preventDefault()
    if(em.value!="" && pwd.value!=""){
        let formData = new URLSearchParams()
        formData.append("username", em.value)
        formData.append("password", pwd.value)
        try{
            let response=await fetch("https://backend-94supzxot-charitha-kundurus-projects.vercel.app/login",{
                method:"POST",
                headers:{
                "Content-Type":"application/x-www-form-urlencoded"
            },
            body:formData
            })
            let data=await response.json()
            console.log("Status:", response.status);
            console.log("OK:", response.ok);
            console.log("Data:", data); 
            if(response.ok){
                alert("user login successfully")
                localStorage.setItem("token",data.access_token)
                pwd.value=""
                em.value=""
            }
            else{
                alert(data.detail || "login failed")
            }
        }
        catch(error){
    console.log(error)
    alert(error.message)
}

}
    else{
        alert("plz fill all details")
    }
})
