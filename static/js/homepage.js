/* NavBar */ 
document.addEventListener('DOMContentLoaded', function() {
    var navbar = document.getElementById('nav');
    var subNavbar = document.querySelector(".contentNav")
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            navbar.classList.remove('nav-absolute');
            subNavbar.classList.remove('barsubNavContent')
            navbar.classList.add('nav-fixed');
        } else {
            navbar.classList.remove('nav-fixed');
            navbar.classList.add('nav-absolute');
            subNavbar.classList.add('barsubNavContent')
        }
    });
    
    // Initial state
    if (window.scrollY > 0) {
        navbar.classList.add('nav-fixed');
    } else {
        navbar.classList.add('nav-absolute');
    }
});
