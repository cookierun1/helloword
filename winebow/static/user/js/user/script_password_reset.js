const btn_submit = document.getElementById("btn-submit");
const form = document.getElementById("emailForm")
btn_submit.addEventListener("click", () => {
    btn_submit.disabled=true;
    form.submit();
});
