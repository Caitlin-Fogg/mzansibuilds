// Handles display of completed projects (Celebration Wall)
// Fetches data from backend and renders it dynamically


document.addEventListener("DOMContentLoaded", async () => {
    // Get container element for displaying projects
    const container = document.getElementById("completedProjects");

    try {
        // Fetch completed projects from backend
        const projects = await getCompletedProjects();

        // Show message if no completed projects exist
        if (projects.length === 0) {
            container.innerHTML = "<p>No completed projects yet</p>";
            return;
        }

        // Rendering projects
        projects.forEach(project => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <small>By: ${project.username}</small>
            `;

            div.style.cursor = "pointer";

            div.addEventListener("click", () => {
            window.location.href = `project.html?id=${project.id}&readonly=true`;
            });

            container.appendChild(div);
    });

    } catch (err) {
        container.innerHTML = "<p>Failed to load Celebration Wall.</p>";
        console.error(err);
    }
});