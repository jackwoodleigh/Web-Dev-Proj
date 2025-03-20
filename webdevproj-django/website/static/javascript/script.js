document.addEventListener("DOMContentLoaded", () => {
    // Homepage search functionality
    const searchBtn = document.getElementById("searchBtn");
    if (searchBtn) {
      searchBtn.addEventListener("click", () => {
        const query = document.getElementById("searchInput").value;
        // Redirect to a search results page with the query as a URL parameter
        window.location.href = `search.html?query=${encodeURIComponent(query)}`;
      });
    }
  
    // Example: Add filtering functionality on the recipe listing page
    const applyFiltersBtn = document.getElementById("applyFilters");
    if (applyFiltersBtn) {
      applyFiltersBtn.addEventListener("click", () => {
        // Retrieve filter values (this example uses only the values; you can integrate with your data source)
        const cookingTime = document.getElementById("cookingTime").value;
        const difficulty = document.getElementById("difficulty").value;
        console.log("Filters applied:", { cookingTime, difficulty });
        // Here you would filter the displayed recipe cards based on selected criteria
      });
    }
  });
  