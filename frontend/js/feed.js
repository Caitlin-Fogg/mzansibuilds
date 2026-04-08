async function loadProjects() {
    try {
        const projects = await apiRequest("/projects/active");

        const container = document.getElementById("projects");
        container.innerHTML = "";

        projects.forEach(project => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description || ""}</p>
                <p>Status: ${project.status}</p>
                <hr/>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error(error);
        alert("Failed to load projects");
    }
}

loadProjects();