// Rows with a data-href open their page, except when a button or link inside them is clicked
document.querySelectorAll(".clickable-row[data-href]").forEach((row) => {
  row.addEventListener("click", (event) => {
    if (event.target.closest("a, button, form")) return;
    window.location.href = row.dataset.href;
  });
});

// The shared delete modal takes its target URL and item name from the button that opened it
const deleteModal = document.getElementById("deleteModal");
if (deleteModal) {
  deleteModal.addEventListener("show.bs.modal", (event) => {
    const trigger = event.relatedTarget;
    deleteModal.querySelector("form").action = trigger.dataset.deleteUrl;
    deleteModal.querySelector("[data-delete-name]").textContent = trigger.dataset.deleteName;
  });
}
