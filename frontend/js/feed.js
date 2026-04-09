async function loadProjects() {
    try {
        console.log("Loading projects...");

        const projects = await apiRequest("/projects/active");

        console.log("SUCCESS:", projects);

        const container = document.getElementById("projects");
        container.innerHTML = "";

        projects.forEach(project => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description || ""}</p>
                <p>Status: ${project.status}</p>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error("ACTUAL ERROR:", error);
        alert("Failed to load projects");
    }
}

loadProjects();