document.addEventListener("DOMContentLoaded", () => {
    const listContainer = document.getElementById("list-container");

    // Fetch lists from the server
    fetch("/lists/")
        .then(response => response.json())
        .then(data => {
            data.forEach(list => {
                const listItem = document.createElement("div");
                listItem.className = "list-item";
                listItem.innerHTML = `
                    <h3>${list.name}</h3>
                    <p>${list.description}</p>
                `;
                listContainer.appendChild(listItem);
            });
        })
        .catch(err => console.error("Error fetching lists:", err));
});
