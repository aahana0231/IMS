// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirmation for delete actions
    document.querySelectorAll('.delete-confirm').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Stock quantity validation
    var stockForm = document.getElementById('stockForm');
    if (stockForm) {
        stockForm.addEventListener('submit', function(e) {
            var quantityInput = document.getElementById('quantity');
            var quantity = parseInt(quantityInput.value);
            
            if (isNaN(quantity) || quantity <= 0) {
                e.preventDefault();
                alert('Please enter a valid quantity (greater than 0).');
                return false;
            }
            
            // For stock removal, check against max available
            var actionType = document.getElementById('actionType').value;
            if (actionType === 'remove') {
                var maxAvailable = parseInt(document.getElementById('maxAvailable').value);
                if (quantity > maxAvailable) {
                    e.preventDefault();
                    alert('Cannot remove more than available quantity (' + maxAvailable + ').');
                    return false;
                }
            }
            
            return true;
        });
    }

    // Search input focus
    var searchInput = document.querySelector('input[name="term"]');
    if (searchInput) {
        // Focus search on Ctrl+F or Cmd+F
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Threshold adjustment in low stock page
    var thresholdInput = document.getElementById('thresholdInput');
    var thresholdForm = document.getElementById('thresholdForm');
    
    if (thresholdInput && thresholdForm) {
        thresholdInput.addEventListener('change', function() {
            thresholdForm.submit();
        });
    }
}); 