const btn_submit = document.getElementById("btn-submit");
const reset_form = document.getElementById("resetForm")

btn_submit.addEventListener("click", () => {
    reset_form.submit();
});