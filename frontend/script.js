async function getRecommendations() {
    const query = document.getElementById("queryInput").value.trim();
    if (!query) {
        alert("Please enter a query.");
        return;
    }

    const loading = document.getElementById("loading");
    const table = document.getElementById("resultsTable");
    const tbody = table.querySelector("tbody");

    loading.classList.remove("hidden");
    table.classList.add("hidden");
    tbody.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        data.forEach(item => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.assessment_name}</td>
                <td>${item.test_type.join(", ")}</td>
                <td>${item.duration || "N/A"}</td>
                <td>${item.remote_testing}</td>
                <td><a href="${item.assessment_url}" target="_blank">View</a></td>
            `;

            tbody.appendChild(row);
        });

        table.classList.remove("hidden");

    } catch (error) {
        alert("Error fetching recommendations.");
        console.error(error);
    } finally {
        loading.classList.add("hidden");
    }
}
