document.addEventListener("DOMContentLoaded", () => {
  const tagInput = document.getElementById("tag-input");
  const tagsArea = document.getElementById("tags-area");
  const hiddenTags = document.getElementById("hidden-tags"); 
  let tags = [];
  
  if (hiddenTags.value) {
    tags = hiddenTags.value.split(',');
    renderTags();
  }
  
  tagInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();  
      if (tagInput.value.trim() !== "") {
        const newTag = tagInput.value.trim();
        if (!tags.includes(newTag)) {
          tags.push(newTag);
          renderTags();
        }
        tagInput.value = "";
      }
    }
  });

  function renderTags() {
    tagsArea.innerHTML = "";
    tags.forEach((tag, index) => {
      const tagElement = document.createElement("div");
      tagElement.classList.add("tag");
      tagElement.textContent = tag;

      const removeBtn = document.createElement("button");
      removeBtn.classList.add("remove-btn");
      removeBtn.textContent = "x";

      removeBtn.addEventListener("click", () => {
        removeTag(index);
      });
      tagElement.appendChild(removeBtn);
      tagsArea.appendChild(tagElement);
    });
    hiddenTags.value = tags.join(',');
  }

  function removeTag(index) {
    tags.splice(index, 1);
    renderTags();
  }
  
  const imageInput = document.getElementById("image");
  const imagePreview = document.getElementById("image-preview");
  
  imageInput.addEventListener("change", function() {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      
      reader.onload = function(e) {
        imagePreview.innerHTML = "";
        const img = document.createElement("img");
        img.src = e.target.result;
        imagePreview.appendChild(img);
      };
      
      reader.readAsDataURL(this.files[0]);
    }
  });
}); 