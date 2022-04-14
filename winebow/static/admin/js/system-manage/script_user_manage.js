const user_creation_modal = new bootstrap.Modal(document.getElementById('modal_create_user'), {
    keyboard: false
});

function clearCreationModal() {
    const creation_inputs = document.getElementById('divCreateUser').getElementsByClassName('form-control');
    for(el of creation_inputs) {
        el.value = ''
    }
    document.getElementById('creation_error_msg').textContent = '';
}

function clearUpdateModal(id_to_update) {
    const id = document.getElementById(`permId${id_to_update}`).dataset.value;
    const name = document.getElementById(`permName${id_to_update}`).dataset.value;
    const codename = document.getElementById(`permCodename${id_to_update}`).dataset.value;

    document.getElementById('id_update').value = id;
    document.getElementById('name_update').value = name;
    document.getElementById('codename_update').value = codename;
    updateUrlText(
        document.getElementById('codename_update'),
        'update_url_alerter'
    );
}

function updateErrorText(el, alerter_id) {
    url = el.value;
    url_alerter = document.getElementById(alerter_id);
    if (url === '') {
        url_alerter.innerHTML = '<i class="fa" aria-hidden="true" ></i>접근 권한을 설정할 URL을 입력하세요.';
    } else {        
        url_alerter.innerHTML = `<code>${url}</code>` + "에 대한 메뉴 접근 권한이 생성됩니다.";
    }
}

function searchUser() {
    const param_builder = new URLSearchParams();

    const criteria = document.getElementById('criteriaSelect').value;
    const search_keyword = document.getElementById('searchKeywordInput').value;

    param_builder.append('criteria', criteria);
    param_builder.append('search_keyword', search_keyword);
    
    const params = param_builder.toString();
    const url = ''; 

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                parser = new DOMParser();
                updated_table = parser.parseFromString(xhr.response, "text/html")
                    .getElementById('contentDiv');
                document.getElementById('contentDiv').replaceWith(updated_table);

            } else {
                err_elem.textContent = xhr.responseText;  
            }
        } 
    }; 
    xhr.open('GET', `${url}?${params}`); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(null); 
}

function getPage(page = undefined) {
    const param_builder = new URLSearchParams();

    const criteria = document.getElementById('criteria').value;
    const search_keyword = document.getElementById('searchKeyword').value;
    if (!page) {
        page = document.getElementById('currentPage').value || 1;
    }

    param_builder.append('criteria', criteria);
    param_builder.append('search_keyword', search_keyword);
    param_builder.append('page', page);

    const params = param_builder.toString();
    const url = ''; 

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                parser = new DOMParser();
                updated_table = parser.parseFromString(xhr.response, "text/html")
                    .getElementById('contentDiv');
                document.getElementById('contentDiv').replaceWith(updated_table);

            } else {
                err_elem.textContent = xhr.responseText;  
            }
        } 
    }; 
    xhr.open('GET', `${url}?${params}`); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(null); 

}

function createUser() {
    const err_elem = document.getElementById('creation_error_msg');
    
    const param_builder = new URLSearchParams();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;

    param_builder.append('username', username);
    param_builder.append('password', password);
    param_builder.append('first_name', firstName);
    param_builder.append('last_name', lastName);
    param_builder.append('email', email);

    for(i of param_builder.values()) {
        if (!i){
            err_elem.textContent = "필드값을 모두 입력하세요.";
            return;
        }
    }

    const groupId = document.getElementById('groups').value;
    if (!groupId) {
        err_elem.textContent = "그룹을 지정하세요.";
        return;
    }
    param_builder.append('groups', groupId);
    
    const params = param_builder.toString();
    const url = ''; 

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                getPage();
                user_creation_modal.hide();
            } else {
                err_elem.textContent = xhr.responseText;  
            }
        } 
    }; 
    xhr.open('POST', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}

function startInputMode(item_id) {
    // Change button.
    const btn = document.getElementById(`btn_mode${item_id}`);
    btn.textContent = '저장';
    btn.classList.remove('btn-warning');
    btn.classList.add('btn-success');
    btn.setAttribute('onclick', `saveChanges(${item_id})` );

    // Make input enable.
    const input_list = [];
    input_list.push(document.getElementById(`groups${item_id}`));
    input_list.push(document.getElementById(`firstName${item_id}`));
    input_list.push(document.getElementById(`lastName${item_id}`));
    input_list.push(document.getElementById(`email${item_id}`));
    input_list.push(document.getElementById(`isActive${item_id}`));
    for(el of input_list){ 
        el.disabled = false;
    }
}

function saveChanges(item_id){

    // Change button.
    const btn = document.getElementById(`btn_mode${item_id}`);
    btn.textContent = '수정';
    btn.classList.remove('btn-success');
    btn.classList.add('btn-warning');
    btn.setAttribute('onclick', `startInputMode(${item_id})`);

    // Make input disable.
    const input_list = [];
    input_list.push(document.getElementById(`groups${item_id}`));
    input_list.push(document.getElementById(`firstName${item_id}`));
    input_list.push(document.getElementById(`lastName${item_id}`));
    input_list.push(document.getElementById(`email${item_id}`));

    const param_builder = new URLSearchParams();
    param_builder.append('id', item_id);
    for(input of input_list) {
        input.disabled = true;
        param_builder.append(input.name, input.value);
    } 
    elem_is_active = document.getElementById(`isActive${item_id}`);
    elem_is_active.disabled = true;
    param_builder.append(elem_is_active.name, elem_is_active.checked);

    const params = param_builder.toString();

    const url = ''; 
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                getPage();

            } else {
                alert("요청에 실패하였습니다. 잠시 후 다시 시도해주세요.");  
            }
        } 
    }; 
    xhr.open('PUT', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}

function deleteUser(id) {
    if (id === '' || !confirm('해당 사용자를 삭제하시겠습니까? ')) {
        return;
    }
     
    const params = `id=${id}`
    const url = ''; 
    

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                getPage();
                
            } else {
                alert(`Error: ${xhr.responseText}`);
            }
        } 
    }; 
    xhr.open('DELETE', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}