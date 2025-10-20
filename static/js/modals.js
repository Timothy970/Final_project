document.addEventListener('DOMContentLoaded', function () {
    // Get modal elements
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const emergencyModal = document.getElementById('emergencyModal');

    // Get buttons that open modals
    const loginButtons = document.querySelectorAll('[data-action="open-login"]');
    const registerButtons = document.querySelectorAll('[data-action="open-register"]');
    const emergencyButtons = document.querySelectorAll('[data-action="open-emergency"]');

    // Get close buttons
    const closeButtons = document.querySelectorAll('.close-modal');

    // Open Login Modal
    function openLoginModal() {
        closeRegisterModal();
        loginModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    // Open Register Modal
    function openRegisterModal() {
        closeLoginModal();
        registerModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    //Open Emergency Modal
    function openEmergencyModal() {
        emergencyModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    // Close Login Modal
    function closeLoginModal() {
        loginModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Close Register Modal
    function closeRegisterModal() {
        registerModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    //close emergency modal
    function closeEmergencyModal() {
        emergencyModal.style.display = 'none';
        document.body.style.overflow = 'auto';

    }
    // Add event listeners
    loginButtons.forEach(btn => {
        btn.addEventListener('click', openLoginModal);
    });

    registerButtons.forEach(btn => {
        btn.addEventListener('click', openRegisterModal);
    });

    emergencyButtons.forEach(btn => {
        btn.addEventListener('click', openEmergencyModal)
    })
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            if (loginModal.style.display === 'block') closeLoginModal();
            if (registerModal.style.display === 'block') closeRegisterModal();
            if (emergencyModal.style.display === 'block') closeEmergencyModal();
        });
    });

    // Close when clicking outside
    window.addEventListener('click', function (event) {
        if (event.target === loginModal) closeLoginModal();
        if (event.target === registerModal) closeRegisterModal();
        if (event.target === emergencyModal) closeEmergencyModal();

    });

    // Close with Escape key
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeLoginModal();
            closeRegisterModal();
            closeEmergencyModal();
        }
    });

    // Make functions available globally if needed
    window.openLoginModal = openLoginModal;
    window.openRegisterModal = openRegisterModal;
    window.openEmergencyModal = openEmergencyModal;
    window.closeEmergencyModal = closeEmergencyModal;
    window.closeLoginModal = closeLoginModal;
    window.closeRegisterModal = closeRegisterModal;
});