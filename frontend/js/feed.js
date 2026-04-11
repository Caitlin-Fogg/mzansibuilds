// Function to check if users are logged in
// To view the live feed, a user must be logged in. If they are not, they will be redirected to the home page
function checkAuth() {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "home-page.html";
    }
}

checkAuth();

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

document.getElementById("logoutBtn")?.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "home-page.html";
});

loadProjects();

