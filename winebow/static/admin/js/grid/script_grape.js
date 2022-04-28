const itemGrid = $("#itemGrid");
var lastSelected = null;
$.ajaxSetup({
    headers : {
        'X-CSRFToken': csrftoken
    }
});

window.onload = async () => {
    createGrid();
}

function createGrid() {
    itemGrid.jqGrid({
       
        // UI
        // styleUI: 'Bootstrap5',
        // iconSet: "Bootstrap5",

        // Data
        // datatype: 'local',
        // data: dataArray,
        
        url: '/system-manage/grid_sample',
        editurl: '/system-manage/grid_sample',
        datatype: "json",

        caption : 'Grape',
        colMenu : true,
        height: 'auto',
        responsive: true,
        autowidth: true,
        rowNum: 10,
        pager: '#pager',
        viewrecords: true,
        loadonce: true,
        rownumbers: true,
        autoResizing: { compact: true },
        colNames: ["포도이름영문","포도이름한글","포도설명"," "],
        colModel: [
            {
                name: 'grapeNameEn', label: 'grapeNameEn', editable:true, edittype:'text', 
            },
            {
                name: 'grapeNameKr', label: 'grapeNameKr', editable:true, edittype:'text', 
            },
            {
                name: 'grapeDes', label: 'grapeDes', editable:true, edittype:'text', 
            },
            {
                name: 'Actions',  width: 100, height: 120, editable: false, formatter: 'actions',
                formatoptions: {
                    keys: true,
                    editformbutton: false,
                    // Note that this mtype is used only for editing.
                    mtype: 'PUT',

                    editOptions: {
                        mtype: 'PUT',
                        editCaption: '데이터 수정',
                        bSubmit: "수정",
                        bCancel: "취소",
                        clearAfterAdd: true,
                        closeAfterAdd: true,
                        closeAfterEdit: true,
                        closeOnEscape: true,
                        recreateForm: true, // This option fixes missing buttons.
                        afterSubmit: reloadAfterSubmit,
                    },
                    
                    delOptions: {
                        mtype: 'DELETE',
                        caption: "데이터 삭제",
                        msg: "선택한 항목을 지우시겠습니까?",
                        bSubmit: "삭제",
                        bCancel: "취소",
                        closeOnEscape: true,
                        recreateForm: true, // This option fixes missing buttons.
                        afterSubmit: reloadAfterSubmit,
                    }
                },
                search: false,
            },
            
        ],
    
    }).jqGrid("filterToolbar", {
        searchOnEnter: false,
    
    }).jqGrid('navGrid','#pager', 
    // Refer to http://www.guriddo.net/documentation/guriddo/javascript/user-guide/navigating/#form-edit-navigator
    // parameter.
    
    {
        add: true,
        search: false,
        alerttext: '수정 또는 삭제할 데이터를 선택해주세요.',
        alertwidth: 300,
    },
    // prmEdit.
    // Refer to http://www.guriddo.net/documentation/guriddo/javascript/user-guide/editing/#edit-grid-row
    
    {
        mtype: 'PUT',
        editCaption: '데이터 수정',
        bSubmit: "수정",
        bCancel: "취소",
        clearAfterAdd: true,
        closeAfterAdd: true,
        closeAfterEdit: true,
        closeOnEscape: true,
        recreateForm: true, // This option fixes missing buttons.

        afterSubmit: reloadAfterSubmit,
    },
    
    // prmAdd.
    // Refer to http://www.guriddo.net/documentation/guriddo/javascript/user-guide/editing/#add-grid-row

    {
        mtype: 'POST',
        addCaption: '데이터 추가',
        bSubmit: "추가",
        bCancel: "취소",
        clearAfterAdd: true,
        closeAfterAdd: true,
        closeAfterEdit: true,
        closeOnEscape: true,
        recreateForm: true, // This option fixes missing buttons.

        afterSubmit: reloadAfterSubmit,
    },
    // prmDel.
    // Refer to http://www.guriddo.net/documentation/guriddo/javascript/user-guide/editing/#del-grid-row
    
    {
        mtype: 'DELETE',
        caption: "데이터 삭제",
        msg: "선택한 항목을 지우시겠습니까?",
        bSubmit: "삭제",
        bCancel: "취소",
        closeOnEscape: true,
        recreateForm: true, // This option fixes missing buttons.

        afterSubmit: reloadAfterSubmit,
    });

    $('#gsh_itemGrid_rn').html('<span class="ui-icon ui-icon-search"></span>');
}


function reloadGrid() {
    pageAfterReload = 1;
    $("#itemGrid").jqGrid('setGridParam',{
        datatype: 'json',
        page: pageAfterReload
    }).trigger('reloadGrid');
}
function reloadAfterSubmit (response, postdata, oper)  {
    const success = response.responseJSON.success;
    let msg = "";
    if (!success) {
        msg = response.responseJSON.message;
        return [success, msg, "_empty"];
    }
    const newID = response.responseJSON.newID;
    reloadGrid();

    return [success, msg, newID];
}
