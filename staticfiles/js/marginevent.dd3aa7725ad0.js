// verificamos si el usuario esta o no logueado para definir los margenes 


document.addEventListener('DOMContentLoaded', function() {
    const bodyClass = document.body.classList.contains('authenticated');
    const mainContent = document.querySelector('.main-content');
    if (bodyClass) {
        mainContent.classList.add('authenticated-main');
    } else {
        mainContent.classList.add('unauthenticated-main');
    }
});