// Hamburger menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const hamburgerIcon = mobileMenuButton.querySelector('i');

    mobileMenuButton.addEventListener('click', function() {
        // Toggle mobile menu visibility
        mobileMenu.classList.toggle('hidden');
        
        // Toggle hamburger icon between bars and times
        if (mobileMenu.classList.contains('hidden')) {
            hamburgerIcon.className = 'fas fa-bars text-xl';
        } else {
            hamburgerIcon.className = 'fas fa-times text-xl';
        }
    });

    // Close mobile menu when clicking on a link
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
            hamburgerIcon.className = 'fas fa-bars text-xl';
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = event.target.closest('nav');
        const isMobileMenuButton = event.target.closest('#mobile-menu-button');
        
        if (!isClickInsideNav && !mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
            hamburgerIcon.className = 'fas fa-bars text-xl';
        }
    });

    // Close mobile menu on window resize (if resizing to desktop)
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) { // lg breakpoint
            mobileMenu.classList.add('hidden');
            hamburgerIcon.className = 'fas fa-bars text-xl';
        }
    });
});