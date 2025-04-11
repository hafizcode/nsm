const searchInput = document.getElementById("searchInput");
const filterButtons = document.querySelectorAll(".filter-btn");
const items = document.querySelectorAll(".item");

let currentFilter = "all";

searchInput.addEventListener("input", filterList);
filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        filterButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.getAttribute("data-filter");
        filterList();
    });
});

function filterList() {
    const searchTerm = searchInput.value.toLowerCase();

    items.forEach((item) => {
        const text = item.textContent.toLowerCase();
        const labels = item.getAttribute("data-labels");

        const matchesSearch = text.includes(searchTerm);
        const matchesFilter =
            currentFilter === "all" || labels.includes(currentFilter);

        if (matchesSearch && matchesFilter) {
            item.style.display = "";
        } else {
            item.style.display = "none";
        }
    });
}
