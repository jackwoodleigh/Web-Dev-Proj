document.addEventListener('DOMContentLoaded', function() {
  const deleteButtons = document.querySelectorAll('.delete-btn');
  deleteButtons.forEach(button => {
    button.addEventListener('click', function(event) {
      event.preventDefault();
      event.stopPropagation();
      
      if (this.dataset.processing === 'true') {
        return;
      }
      
      const recipeId = this.getAttribute('data-recipe-id');
      
      if (confirm('Are you sure you want to delete this recipe?')) {
        this.dataset.processing = 'true';
        
        fetch(`/recipe/${recipeId}/delete`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            const recipeCard = this.closest('.recipe-card');
            recipeCard.remove();
            
            const recipesList = document.querySelector('.recipes-list');
            if (recipesList && recipesList.children.length === 0) {
              const noContent = document.createElement('div');
              noContent.className = 'no-content';
              noContent.innerHTML = `
                <div class="empty-recipes">
                  <i class="ri-book-line"></i>
                  <h2>You haven't created any recipes yet</h2>
                  <p>Create your first recipe to see it here!</p>
                  <a href="/create-recipe" class="create-btn">Create New Recipe</a>
                </div>
              `;
              
              document.querySelector('.recipes-list').replaceWith(noContent);
            }
          } else {
            alert('Failed to delete recipe. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');
        })
        .finally(() => {
          this.dataset.processing = 'false';
        });
      }
    });
  });
}); 