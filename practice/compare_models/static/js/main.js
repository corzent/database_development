document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Function to handle text analysis form submission
    const analyzeForm = document.getElementById('analyze-form');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = 'Analyzing...';
            submitButton.disabled = true;

            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results-container').innerHTML = data.html;
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            });
        });
    }

    // Function to get CSRF token
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

    // Function to toggle model details
    const modelCards = document.querySelectorAll('.model-card');
    modelCards.forEach(card => {
        const detailsButton = card.querySelector('.details-button');
        if (detailsButton) {
            detailsButton.addEventListener('click', function() {
                const details = card.querySelector('.model-details');
                details.classList.toggle('d-none');
                this.textContent = details.classList.contains('d-none') ? 'Show Details' : 'Hide Details';
            });
        }
    });
}); 