function setGroupPermission(permId, groupId) {

    const url = '';

    const isChecked = document.getElementById(`Perm${permId}`).checked;

    const paramBuilder = new URLSearchParams();
    paramBuilder.append('group_id', groupId);
    paramBuilder.append('permission_id', permId);
    paramBuilder.append('has_perm', isChecked);
    
    const params = paramBuilder.toString();

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                $(`#permRow${permId}`).replaceWith($(xhr.response).find(`#permRow${permId}`));
                
            } else {
                showErrorToast(xhr.response, 3700);
                $('#permTableBody').html('권한 정보를 변경하는 도중 오류가 발생했습니다. 새로고침 후, 다시 시도해주세요.');
            }
        } 
    }; 
    xhr.open('POST', `${url}`); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(params);

}

function getGroupPermissionList() {
    const url = 'permissions';

    const selectedGid = document.getElementById('groupsSelect').value;
    if (!selectedGid) {
        return;
    }

    const paramBuilder = new URLSearchParams();
    paramBuilder.append('group_id', selectedGid);

    const params = paramBuilder.toString();

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => { 
        if (xhr.readyState == xhr.DONE) { 
            if (xhr.status === 200 || xhr.status === 201) {
                parser = new DOMParser();
                updated_table = parser.parseFromString(xhr.response, "text/html")
                    .getElementById('contentDiv');
                document.getElementById('contentDiv').replaceWith(updated_table);

                $('#btn_grp_delete').replaceWith($(xhr.response).find('#btn_grp_delete'));
                
                //initializePermListTable();
                //searchPermList();
            } else {
                //showErrorToast(xhr.response);
                $('#permTableBody').html('권한 정보를 받아오는 도중 오류가 발생했습니다. 새로고침 후, 다시 시도해주세요.');
            }
        } 
    }; 
    xhr.open('GET', `${url}?${params}`); 
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader('X-CSRFToken', csrftoken); 
    xhr.send(null);

}

function searchPerm() {
    const selectedGid = document.getElementById('groupsSelect').value;
    if (!selectedGid) {
        return;
    }

    const paramBuilder = new URLSearchParams();

    const criteria = document.getElementById('criteriaSelect').value;
    const search_keyword = document.getElementById('searchKeywordInput').value;

    paramBuilder.append('criteria', criteria);
    paramBuilder.append('search_keyword', search_keyword);
    paramBuilder.append('group_id', selectedGid);
    
    const params = paramBuilder.toString();
    const url = 'permissions';

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
    const selectedGid = document.getElementById('groupsSelect').value;
    if (!selectedGid) {
        return;
    }

    const paramBuilder = new URLSearchParams();

    const criteria = document.getElementById('criteria').value;
    const search_keyword = document.getElementById('searchKeyword').value;
    if (!page) {
        page = document.getElementById('currentPage').value || 1;
    }

    paramBuilder.append('criteria', criteria);
    paramBuilder.append('search_keyword', search_keyword);
    paramBuilder.append('page', page);
    paramBuilder.append('group_id', selectedGid);

    const params = paramBuilder.toString();
    const url = 'permissions';

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