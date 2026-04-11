document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("completedProjects");

    try {
        const projects = await getCompletedProjects();

        if (projects.length === 0) {
            container.innerHTML = "<p>No completed projects yet</p>";
            return;
        }

        projects.forEach(project => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <small>By: ${project.username}</small>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        container.innerHTML = "<p>Failed to load Celebration Wall.</p>";
        console.error(err);
    }
});