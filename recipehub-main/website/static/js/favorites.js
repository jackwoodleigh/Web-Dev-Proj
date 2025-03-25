
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.favorite-icon').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const recipeId = this.dataset.recipeId;
            const btn = this;
            fetch('/toggle_favorite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `recipe_id=${recipeId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const icon = btn.querySelector('i');
                    if (data.favorited) {
                        icon.classList.remove('ri-star-line');
                        icon.classList.add('ri-star-fill');
                    } else {
                        icon.classList.remove('ri-star-fill');
                        icon.classList.add('ri-star-line');
                    }
                } else {
                    console.error("Failed to toggle favorite");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
