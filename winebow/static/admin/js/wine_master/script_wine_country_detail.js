const btn_delete = document.getElementById("btn-delete");

btn_delete.addEventListener("click", async() => {
    if (!confirm("정말 삭제하시겠습니까?")) {
        return false;
    }
    try{
        const response = await fetch('',{
            method: 'DELETE',
            headers: {'X-CSRFToken': csrftoken},
        })
        const result = await response.json()
        if (result.success == false) {
            alert(result.message);
        }
        else {
            location.href='/system-manage/wine_country'
        }
    }
    catch(error){
        alert(error);
        return false;
    }
});