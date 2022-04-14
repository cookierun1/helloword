async function activateUser(userId){
    if(!confirm("가입요청을 허락하시겠습니까?")){
        return false;
    }
    const data = { user_id : userId };
    const response = await fetch('',{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .catch((error) => {
        alert(error);
    })
    const result = await response.json()
    if (result.success == false) {
        alert(result.message);
    }
    else {
        alert(result.message);
        location.reload(true);
    }
}

async function cancelUser(userId){
    if(!confirm("가입을 취소하겠습니까?")){
        return false;
    }
    const data = { user_id : userId };
    const response = await fetch('',{
        method: 'DELETE',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .catch((error) => {
        alert(error);
    })
    const result = await response.json()
    if (result.success == false) {
        alert(result.message);
    }
    else {
        alert(result.message);
        location.reload(true);
    }
}