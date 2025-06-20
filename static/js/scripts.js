document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.toggle-btn').forEach(button => {
    button.addEventListener('click', function () {
      const id = this.getAttribute('data-id');

      fetch(`/toggle/${id}`, {
        method: "POST"
      })
        .then(res => res.json())
        .then(data => {
          if (data.active) {
            this.textContent = "Active";
            this.classList.remove("inactive");
            this.classList.add("active");
          } else {
            this.textContent = "Inactive";
            this.classList.remove("active");
            this.classList.add("inactive");
          }
        })
        .catch(error => {
          console.error("Error toggling status:", error);
          alert("Something went wrong while toggling status.");
        });
    });
  });
});
