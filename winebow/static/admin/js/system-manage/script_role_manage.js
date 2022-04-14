function clearCreationModal() {
    const creation_inputs = document.getElementById('divCreateGroup').getElementsByClassName('form-control');
    for(el of creation_inputs) {
        el.value = ''
    }
    document.getElementById('creation_error_msg').value = '';
}

function createGroup() { 
    const err_elem = document.getElementById('error_msg');

    const url = '/system-manage/role-manage/';
    const groupName = document.getElementById('groupNameCreate').value;

    if (groupName == '') {
        err_elem.textContent = "생성할 그룹이름을 입력하세요.";
        return;
    }
    
    const paramBuilder = new URLSearchParams();
    paramBuilder.append('group_name', groupName);
    
    const params = paramBuilder.toString();
    
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                const res = JSON.parse(xhr.responseText); 
                if (res.success == false) { 
                    err_elem.textContent = res.message;
                } else { 
                    //showMessageToast("그룹이 생성되었습니다.", 3700);
                    //$("#modal_create_group").modal("hide");
                    window.location.reload();
                } 
            } else {
                showErrorToast("요청에 실패하였습니다. 잠시 후 다시 시도해주세요.");
            }
        } 
    }; 
    xhr.open('POST', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}


function deleteGroup(groupId) { 
    const err_elem = document.getElementById('error_msg');

    const url = '/system-manage/role-manage/';
    if (groupId == '') {
        showErrorToast("삭제 불가능한 그룹입니다.");
        return;
    }
    
    const paramBuilder = new URLSearchParams();
    paramBuilder.append('group_id', groupId);
    
    const params = paramBuilder.toString();
    
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                const res = JSON.parse(xhr.responseText); 
                if (res.success == false) { 
                    showErrorToast(res.message);
                } else { 
                    //showMessageToast("그룹이 삭제되었습니다.", 3700);
                    window.location.reload();
                } 
            } else {
                showErrorToast("요청에 실패하였습니다. 잠시 후 다시 시도해주세요.");
            }
        } 
    }; 
    xhr.open('DELETE', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}