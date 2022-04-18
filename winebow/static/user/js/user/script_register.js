const btn_register = document.getElementById("btn-register");
const id = document.getElementById('username');
const password = document.getElementById('password')
const password_confirm = document.getElementById('confirm-password');
const email = document.getElementById('email');
const checkbox = document.getElementById('register-checkbox');

btn_register.addEventListener("click", async() => {
    const data =new FormData(document.getElementById("registerForm"));

    if(id.value == ''){
        id.focus();
        return false;
    }
    else{
        if(!CheckID(id.value)){
            id.focus();
            return false;
        }
    }
    if(password.value == ''){
        password.focus();
        return false;
    }
    else{
        if(!CheckPassword(password.value)){
            password.focus();
            return false;
        }
    }
    if(password_confirm.value == ''){
        password_confirm.focus();
        return false;
    }
    else{
        if(!SamePassword()){
            password_confirm.focus();
            return false;
        }
    }
    if(name.value == ''){
        name.focus();
        return false;
    }
    if(email.value == ''){
        email.focus();
        return false;
    }
    else{
        if(!CheckEmail(email.value)){
            email.focus();
            return false;
        }
    }
    if(!checkbox.checked){
        checkbox.focus();
        alert('약관동의를 해주세요.');
        return false;
    }
    
    try{
        btn_register.disabled = true;
        id.disabled=true;
        password.disabled=true;
        password_confirm.disabled=true;
        email.disabled=true;
        checkbox.disabled=true;
        btn_register.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        const response = await fetch('',{
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: data
        })
        const result = await response.json()
        if (result.success == false) {
            alert(result.message);
            id.disabled=false;
            password.disabled=false;
            password_confirm.disabled=false;
            email.disabled=false;
            checkbox.disabled=false;
            btn_register.disabled = false;
            btn_register.innerHTML='Register';
        }
        else {
            location.href='/confirm-email?email='+email.value
        }
    }
    catch(error){
        alert(error);
        id.disabled=false;
        password.disabled=false;
        password_confirm.disabled=false;
        email.disabled=false;
        checkbox.disabled=false;
        btn_register.disabled = false;
        btn_register.innerHTML='Register';
        return false;
    }
});

//아이디 정규식
function CheckID(str){
    if(str == '')
        return;
    var reg_id = /^[a-z]+[a-z0-9]{5,19}$/g;

    if( !reg_id.test(str)) {
        document.getElementById('idError').innerText = '아이디는 영문자로 시작하는 6~20자 영문자 또는 숫자이어야 합니다.';
        return false;
    }
    else{
        document.getElementById('idError').innerText = ''
        return true;
    }
}

//이메일 정규식
function CheckEmail(str){                                        
    var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

    if(!reg_email.test(str)){
       document.getElementById('emailError').innerText = '잘못된 이메일 형식입니다.';
       return false;
   }         
    else{
       document.getElementById('emailError').innerText = ''
       return true;
   }             
}

//비밀번호 정규식
function CheckPassword(str){
   if(!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,16}$/.test(str)){
       document.getElementById('passwordError').innerText = '숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.';
       return false;
   }
 
   var checkNum = str.search(/[0-9]/g); // 숫자사용
   var checkEng = str.search(/[a-z]/ig); // 영문사용
 
   if(checkNum <0 || checkEng <0){
       document.getElementById('passwordError').innerText="숫자와 영문자를 조합하여야 합니다.";
       return false;
   }
   else{
       document.getElementById('passwordError').innerText="";
       return true;
   }
}
//비밀번호 일치 확인
function SamePassword(){
   if(password.value== '' || password_confirm.value =='')
       return
   if(password.value != password_confirm.value){
       document.getElementById('passwordError').innerText="비밀번호가 일치하지 않습니다.";
       return false;
   }
   else{
       document.getElementById('passwordError').innerText="";
       return true;
   }
}
