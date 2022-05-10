const btn_submit=document.getElementById("btn-submit");
const wine_num=document.getElementById("wine_num");
const name_en=document.getElementById("name_en");
const name_kr=document.getElementById("name_kr")
const image=document.getElementById("image")
const description=document.getElementById("description")

btn_submit.addEventListener("click", async()=>{
    const data =new FormData(document.getElementById("data-form"));

    try{
        if(validation()==false){
            return false
        }
        btn_submit.disabled=true;
        const response=await fetch('',{
            method:'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: data
        })
        const result =await response.json()
        if(result.success==false){
            btn_submit.disabled=false;
            alert(result.message);
        }
        else{
            location.href='/system-manage/wine_master_detail/' + result.data_id;
        }

    }
    catch(error){
        alert(error)
        btn_submit.disabled=false;
        return false;
    }

});

//유효성 체크 함수
function validation(){
    if(wine_num.value==''){
        wine_num.focus();
        return false;
    }

    if(name_kr.value == ''){
        name_kr.focus();
        return false;
    }
    if(name_en.value == ''){
        name_en.focus();
        return false;
    }
    return true;
}
