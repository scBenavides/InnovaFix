//Quitar backdrop al cerrar modal
document.addEventListener('shown.bs.modal', function () {
    let backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.parentNode.removeChild(backdrop);
    }
});