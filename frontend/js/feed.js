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
                <h3>
                    <a href="project.html?id=${project.id}">
                        ${project.title}
                    </a>
                </h3>
                <p>${project.description || ""}</p>
                <p>Status: ${project.status}</p>
                <small>By: ${project.username}</small>
            `;

            div.style.cursor = "pointer";
            div.addEventListener("click", (e) => {
                // Only trigger if not clicking the link itself
                if (e.target.tagName !== "A") {
                    window.location.href = `project.html?id=${project.id}`;
                }
            });

            container.appendChild(div);
        });

    } catch (error) {
        console.error("ACTUAL ERROR:", error);
        alert("Failed to load projects");
    }
}

loadProjects();

