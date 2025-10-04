// realsearch.js - Fixed version with proper search hide



function confirmDelete(clientId) {
    if (confirm('Are you sure you want to delete this client? This action cannot be undone.')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/client/${clientId}/delete/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);
        
        document.body.appendChild(form);
        form.submit();
    }  // <-- This closing bracket was missing
}

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - initializing realsearch.js');
    
    // Initialize search if elements exist
    const searchInput = document.getElementById('search-input');
    const clientsContainer = document.getElementById('clients-container');
    const searchLoading = document.getElementById('search-loading');
    const regularClientsSection = document.getElementById('regular-clients-section');
    const searchResultsContainer = document.getElementById('search-results-container');

    if (searchInput && clientsContainer) {
        console.log('Initializing search functionality');
        let searchTimeout;

        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            
            clearTimeout(searchTimeout);
            
            // IMMEDIATELY handle empty input - HIDE search results
            if (query === '') {
                if (searchResultsContainer) searchResultsContainer.classList.add('hidden');
                if (regularClientsSection) regularClientsSection.classList.remove('hidden');
                if (searchLoading) searchLoading.classList.add('hidden');
                return; // STOP here, don't proceed to search
            }
            
            if (searchLoading) searchLoading.classList.remove('hidden');

            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });

        function performSearch(query) {
            const url = `/dashboard/?q=${encodeURIComponent(query)}`;
            
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                clientsContainer.innerHTML = data.clients_html;
                
                // Only show search results if we still have a query (user didn't clear it during fetch)
                if (searchInput.value.trim() !== '') {
                    if (searchResultsContainer) searchResultsContainer.classList.remove('hidden');
                    if (regularClientsSection) regularClientsSection.classList.add('hidden');
                }
            })
            .catch(error => {
                console.error('Search error:', error);
            })
            .finally(() => {
                if (searchLoading) searchLoading.classList.add('hidden');
            });
        }
        
        // Initialize sections on page load - HIDE search results by default
        if (searchResultsContainer) searchResultsContainer.classList.add('hidden');
        if (regularClientsSection) regularClientsSection.classList.remove('hidden');
    }

    // ... rest of your existing code (referral modal, completeReferral, etc.)
    // Initialize referral modal if elements exist
    const referralForm = document.getElementById('referralForm');
    const modal = document.getElementById('referralModal');

    if (referralForm && modal) {
        console.log('Initializing referral modal');
        
        referralForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Referring...';
            submitBtn.disabled = true;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeReferralModal();
                    showNotification(data.message, 'success');
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showNotification(data.error || 'Error referring client', 'error');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error referring client', 'error');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
        
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeReferralModal();
            }
        });
    }

    // Initialize auto-refresh for doctors
    if (document.body.classList.contains('doctor-dashboard')) {
        console.log('Initializing auto-refresh for doctor');
        initializeAutoRefresh();
    }
});

// Modal control functions
function openReferralModal(clientId) {
    const modal = document.getElementById('referralModal');
    const clientIdField = document.getElementById('clientId');
    
    if (modal && clientIdField) {
        clientIdField.value = clientId;
        modal.classList.remove('hidden');
    }
}

function closeReferralModal() {
    const modal = document.getElementById('referralModal');
    const referralForm = document.getElementById('referralForm');
    
    if (modal) modal.classList.add('hidden');
    if (referralForm) referralForm.reset();
}

// Complete Referral Function - FIXED URL
function completeReferral(clientId) {
    if (!confirm('Are you sure you want to mark this referral as completed?')) {
        return;
    }
    
    // FIXED: Use the EXACT URL from your urls.py
    const url = `/client/${clientId}/complete-referral/`;
    console.log('Making request to:', url);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showNotification(data.message || 'Referral completed successfully!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification(data.error || 'Error completing referral', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error: ' + error.message, 'error');
    });
}

// Auto-refresh function
function initializeAutoRefresh() {
    function refreshNotifications() {
        fetch('/check-notifications/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            const pendingElement = document.getElementById('pending-referrals');
            if (pendingElement) {
                pendingElement.textContent = data.pending_referrals;
            }
            
            const navBadges = document.querySelectorAll('.navbar-notification-badge');
            navBadges.forEach(badge => {
                if (badge) {
                    badge.textContent = data.pending_referrals;
                    if (data.pending_referrals > 0) {
                        badge.classList.remove('hidden');
                    } else {
                        badge.classList.add('hidden');
                    }
                }
            });
        })
        .catch(error => console.error('Notification refresh error:', error));
    }
    
    setInterval(refreshNotifications, 5000);
    refreshNotifications();
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Notification function
function showNotification(message, type) {
    const existingNotifications = document.querySelectorAll('.fixed-notification');
    existingNotifications.forEach(notif => notif.remove());
    
    const notification = document.createElement('div');
    notification.className = `fixed-notification fixed top-4 right-4 p-4 rounded-lg shadow-lg text-white z-50 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    }`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

