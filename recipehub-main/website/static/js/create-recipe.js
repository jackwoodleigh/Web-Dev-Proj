document.addEventListener("DOMContentLoaded", () => {
    const tagInput = document.getElementById("tag-input");
    const tagsArea = document.getElementById("tags-area");
    let tags = [];
  
    tagInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();  // prevent the form from submitting
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
  });
  