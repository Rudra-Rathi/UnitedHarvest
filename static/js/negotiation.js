document.addEventListener('DOMContentLoaded', function() {
    // Handle price calculation
    const quantityInput = document.getElementById('quantity');
    const priceInput = document.getElementById('proposed_price');
    const originalPriceDisplay = document.getElementById('original-price');
    const totalPriceDisplay = document.getElementById('total-price');
    const commissionDisplay = document.getElementById('commission');
    const farmerPayoutDisplay = document.getElementById('farmer-payout');
    const savingsDisplay = document.getElementById('price-savings');
    
    // Function to update price calculations
    function updatePriceCalculations() {
        if (!quantityInput || !priceInput) return;
        
        const quantity = parseFloat(quantityInput.value) || 0;
        const proposedPrice = parseFloat(priceInput.value) || 0;
        const originalPrice = originalPriceDisplay ? parseFloat(originalPriceDisplay.getAttribute('data-original-price')) || 0 : 0;
        
        // Calculate totals
        const totalProposed = quantity * proposedPrice;
        const totalOriginal = quantity * originalPrice;
        const commission = totalProposed * 0.05; // 5% commission
        const farmerPayout = totalProposed - commission;
        const savings = totalOriginal - totalProposed;
        
        // Update displays
        if (totalPriceDisplay) {
            totalPriceDisplay.textContent = '₹' + totalProposed.toFixed(2);
        }
        
        if (commissionDisplay) {
            commissionDisplay.textContent = '₹' + commission.toFixed(2);
        }
        
        if (farmerPayoutDisplay) {
            farmerPayoutDisplay.textContent = '₹' + farmerPayout.toFixed(2);
        }
        
        if (savingsDisplay && originalPrice > 0) {
            savingsDisplay.textContent = '₹' + savings.toFixed(2);
            
            if (savings > 0) {
                savingsDisplay.classList.remove('text-danger');
                savingsDisplay.classList.add('text-success');
            } else if (savings < 0) {
                savingsDisplay.classList.remove('text-success');
                savingsDisplay.classList.add('text-danger');
            } else {
                savingsDisplay.classList.remove('text-success', 'text-danger');
            }
        }
    }
    
    // Add event listeners
    if (quantityInput) {
        quantityInput.addEventListener('input', updatePriceCalculations);
    }
    
    if (priceInput) {
        priceInput.addEventListener('input', updatePriceCalculations);
    }
    
    // Initial calculation
    updatePriceCalculations();
    
    // Handle negotiation counter offer form
    const counterOfferBtn = document.getElementById('counter-offer-btn');
    const acceptBtn = document.getElementById('accept-offer-btn');
    const rejectBtn = document.getElementById('reject-offer-btn');
    const negotiationForm = document.getElementById('negotiation-form');
    
    if (counterOfferBtn) {
        counterOfferBtn.addEventListener('click', function() {
            if (negotiationForm) {
                negotiationForm.classList.toggle('d-none');
                
                // Focus on price input
                if (priceInput && !negotiationForm.classList.contains('d-none')) {
                    priceInput.focus();
                }
            }
        });
    }
    
    // Handle accept/reject confirmation
    if (acceptBtn) {
        acceptBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to accept this offer?')) {
                e.preventDefault();
            }
        });
    }
    
    if (rejectBtn) {
        rejectBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to reject this offer?')) {
                e.preventDefault();
            }
        });
    }
    
    // Validate negotiation form
    if (negotiationForm) {
        negotiationForm.addEventListener('submit', function(e) {
            if (!priceInput || !priceInput.value || parseFloat(priceInput.value) <= 0) {
                e.preventDefault();
                alert('Please enter a valid price.');
                return false;
            }
            
            return confirm('Are you sure you want to send this counter offer?');
        });
    }
    
    // Handle negotiation history expansion
    const viewHistoryBtn = document.getElementById('view-history-btn');
    const negotiationHistory = document.getElementById('negotiation-history');
    
    if (viewHistoryBtn && negotiationHistory) {
        viewHistoryBtn.addEventListener('click', function() {
            negotiationHistory.classList.toggle('d-none');
            this.textContent = negotiationHistory.classList.contains('d-none') ? 
                'View Negotiation History' : 'Hide Negotiation History';
        });
    }
});
