window.addEventListener('scroll', function() {
    var isAuthenticated = "{{ user.is_authenticated }}" === "True";

    if (isAuthenticated) {
        var scrollPosition = window.scrollY;
        var footerPosition = document.querySelector('footer').offsetTop;
        var navbar = document.querySelector('.navbar');

        if (scrollPosition > footerPosition - window.innerHeight) {
            navbar.classList.add('transparent-navbar');
        } else {
            navbar.classList.remove('transparent-navbar');
        }
    }
});
