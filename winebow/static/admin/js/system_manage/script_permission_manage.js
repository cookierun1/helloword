const menu_creation_modal = new bootstrap.Modal(document.getElementById('modal_create_menu'), {
    keyboard: false
});

const menu_update_modal = new bootstrap.Modal(document.getElementById('modal_update_menu'), {
    keyboard: false
});



function clearCreationModal() {
    document.getElementById('name').value = '';
    document.getElementById('codename').value = '';
    updateUrlText(
        document.getElementById('codename'),
        'create_url_alerter'
    );
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

function searchPerm() {
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

function updateUrlText(el, alerter_id) {
    url = el.value;
    url_alerter = document.getElementById(alerter_id);
    if (url === '') {
        url_alerter.innerHTML = '<i class="fa" aria-hidden="true" ></i>접근 권한을 설정할 URL을 입력하세요.';
    } else {        
        url_alerter.innerHTML = `<code>${url}</code>` + "에 대한 메뉴 접근 권한이 생성됩니다.";
    }
}

function createMenu() {
    const err_elem = document.getElementById('error_msg');
    const menu_name = document.getElementById('name').value;
    const menu_codename = document.getElementById('codename').value;
    
    if (menu_name === '' || menu_codename === '') {
        err_elem.textContent = "필드값을 모두 입력하세요.";
        return;
    }
     
    const params = `name=${menu_name}&codename=${menu_codename}`
    const url = ''; 

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                getPage();
                menu_creation_modal.hide();

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


function updateMenu() {
    const err_elem = document.getElementById('update_error_msg');
    const menu_id = document.getElementById('id_update').value;
    const menu_name = document.getElementById('name_update').value;
    const menu_codename = document.getElementById('codename_update').value;
    
    if (menu_name === '' || menu_codename === '') {
        err_elem.textContent = "필드값을 모두 입력하세요.";
        return;
    }
     
    const params = `id=${menu_id}&name=${menu_name}&codename=${menu_codename}`
    const url = ''; 

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                getPage();
                menu_update_modal.hide();

            } else {
                err_elem.textContent = `${xhr.status} ${xhr.statusText}: 접근 권한이 없습니다.`;  
            }
        } 
    }; 
    xhr.open('PUT', url); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params); 
}


function deleteMenu(id) {
    if (id === '' || !confirm('권한을 삭제하시겠습니까? ')) {
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