document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Flash messages auto-dismiss
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.alert-dismissible');
        flashMessages.forEach(function(message) {
            const bsAlert = new bootstrap.Alert(message);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Star rating
    const ratingInputs = document.querySelectorAll('.rating-input');
    const ratingValue = document.getElementById('rating-value');
    
    if (ratingInputs.length > 0) {
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                if (ratingValue) {
                    ratingValue.textContent = this.value;
                }
            });
        });
    }
    
    // Search form
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.getElementById('search-input');
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
    
    // File input preview
    const licenseInput = document.getElementById('license_image');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    
    if (licenseInput && previewContainer && previewImage) {
        licenseInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.addEventListener('load', function() {
                    previewImage.src = this.result;
                    previewContainer.classList.remove('d-none');
                });
                reader.readAsDataURL(file);
            } else {
                previewContainer.classList.add('d-none');
            }
        });
    }
    
    // Toggle password visibility
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    
    if (togglePasswordBtns.length > 0) {
        togglePasswordBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const passwordField = document.querySelector(this.getAttribute('data-target'));
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);
                
                // Toggle icon
                this.querySelector('i').classList.toggle('fa-eye');
                this.querySelector('i').classList.toggle('fa-eye-slash');
            });
        });
    }
    
    // Category filter
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const url = new URL(window.location.href);
            url.searchParams.set('category', this.value);
            window.location.href = url.toString();
        });
    }
    
    // Initialize any date pickers
    const datePickers = document.querySelectorAll('.datepicker');
    if (datePickers.length > 0) {
        datePickers.forEach(picker => {
            // This would typically use a date picker library
            // For now, we'll just set the type to date
            picker.type = 'date';
        });
    }
    
    // Quantity calculation in order form
    const quantityInput = document.getElementById('quantity');
    const priceInput = document.getElementById('proposed_price');
    const totalAmountDisplay = document.getElementById('total-amount');
    const commissionDisplay = document.getElementById('commission-amount');
    const farmerPayoutDisplay = document.getElementById('farmer-payout');
    
    function updateCalculations() {
        if (quantityInput && priceInput && totalAmountDisplay) {
            const quantity = parseFloat(quantityInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            const totalAmount = quantity * price;
            const commission = totalAmount * 0.05; // 5% commission
            const farmerPayout = totalAmount - commission;
            
            totalAmountDisplay.textContent = totalAmount.toFixed(2);
            
            if (commissionDisplay && farmerPayoutDisplay) {
                commissionDisplay.textContent = commission.toFixed(2);
                farmerPayoutDisplay.textContent = farmerPayout.toFixed(2);
            }
        }
    }
    
    if (quantityInput && priceInput) {
        quantityInput.addEventListener('input', updateCalculations);
        priceInput.addEventListener('input', updateCalculations);
        
        // Initial calculation
        updateCalculations();
    }
    
    // Handle negotiation accept/reject buttons
    const acceptRejectButtons = document.querySelectorAll('.accept-reject-btn');
    
    if (acceptRejectButtons.length > 0) {
        acceptRejectButtons.forEach(button => {
            button.addEventListener('click', function() {
                const action = this.getAttribute('data-action');
                const actionInput = document.getElementById('action');
                
                if (actionInput) {
                    actionInput.value = action;
                }
                
                // Confirm dialog
                if (action === 'accept') {
                    return confirm('Are you sure you want to accept this offer?');
                } else if (action === 'reject') {
                    return confirm('Are you sure you want to reject this offer?');
                }
            });
        });
    }
    
    // Handle product status toggle
    const availabilityToggle = document.getElementById('is_available');
    if (availabilityToggle) {
        availabilityToggle.addEventListener('change', function() {
            const statusText = document.getElementById('availability-status');
            if (statusText) {
                statusText.textContent = this.checked ? 'Available' : 'Unavailable';
                statusText.className = this.checked ? 'text-success' : 'text-danger';
            }
        });
    }
});
