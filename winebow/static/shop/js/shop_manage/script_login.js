const btn_login = document.getElementById("btn-login");

btn_login.addEventListener("click", async() => {
    const data =new FormData(document.getElementById("loginForm"));
    const id = document.getElementById('username');
    const password = document.getElementById('password')
    if(id.value == ''){
        id.focus();
        return false;
    }
    if(password.value == ''){
        password.focus();
        return false;
    }
    try{
        btn_login.disabled = true;
        const response = await fetch('',{
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: data
        })
        const result = await response.json()
        if (result.success == false) {
            alert(result.message);
            btn_login.disabled = false;
        }
        else {
            location.href = result.url;
        }
    }
    catch(error){
        alert(error);
        btn_login.disabled = false;
        return false;
    }
});

function enterkey() {
    if (window.event.keyCode == 13) {
        btn_login.click()
    }
}