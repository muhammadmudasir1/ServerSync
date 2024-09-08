async function handleLogin(ev){
    ev.preventDefault();
    let username = document.getElementById("username").value;
    let password = document.getElementById("Password").value;
    const error_section = document.getElementById("login_error")
    if (username == "" || password == "") {
        error_section.innerHTML = "Please Enter Username and Password";
        return;
    }
    try {
        const response =await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username: username, password: password}),
        })
        if (response.status !=200){
            const data=await response.json()
            error_section.innerHTML = data.message;

        }
        if(response.redirected){
            window.location.href = response.url;
        }

        
    } catch (error) {
        error_section.innerHTML = error;
    }
    // console.log(data)
}

function handleChange(event) {
    document.getElementById("login_error").innerHTML = "";
}