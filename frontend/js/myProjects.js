// Handles display and management of the current user's projects
// Includes update and delete functionality

// Ensure only authenticated users can access this page
function checkAuth() {
    const token = localStorage.getItem("token");
    if (!token) window.location.href = "home-page.html";
}
checkAuth();

// Fetch and display projects created by the current user
async function loadMyProjects() {
    try {
        const projects = await getMyProjects();

        const container = document.getElementById("projects");
        container.innerHTML = "";

        projects.forEach(p => {
            const div = document.createElement("div");
            div.className = "card";

            div.innerHTML = `
                <h2>${p.title}</h2>
                <p><b>Description:</b> ${p.description || ""}</p>
                <p><b>Stage:</b> ${p.stage}</p>
                <p><b>Support Needed:</b> ${p.support_needed}</p>
                <p><b>Status:</b> ${p.status}</p>
                <small>Created: ${new Date(p.created_at).toLocaleString()}</small>

                <hr>

                <h3>Update Project</h3>
                <form onsubmit="handleUpdate(event, ${p.id})">
                    <input type="text" id="title-${p.id}" placeholder="Title" />
                    <textarea id="desc-${p.id}" placeholder="Description"></textarea>

                    <input type="text" id="support-${p.id}" placeholder="Support Needed" />

                    <select id="stage-${p.id}">
                        <option value="">Select Stage</option>
                        <option value="idea">Idea</option>
                        <option value="planning">Planning</option>
                        <option value="development">Development</option>
                        <option value="completed">Completed</option>
                    </select>

                    <select id="status-${p.id}">
                        <option value="">Select Status</option>
                        <option value="active">Active</option>
                        <option value="completed">Completed</option>
                    </select>

                    <button type="submit">Update</button>
                </form>

                <h3>Delete Project</h3>
                <button onclick="handleDelete(${p.id})">Delete</button>

                <hr>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error(err);
        alert("Failed to load projects");
    }
}

// Handle project update submission
async function handleUpdate(event, id) {
    event.preventDefault();

    // Build update using only changed fields
    const data = {};

    const title = document.getElementById(`title-${id}`).value;
    const description = document.getElementById(`desc-${id}`).value;
    const stage = document.getElementById(`stage-${id}`).value;
    const support = document.getElementById(`support-${id}`).value;
    const status = document.getElementById(`status-${id}`).value;

    if (title) data.title = title;
    if (description) data.description = description;
    if (stage) data.stage = stage;
    if (support) data.support_needed = support;
    if (status) data.status = status;

    try {
        // Send update request to backend
        await updateProject(id, data);
        alert("Project updated!");
        // Reload
        loadMyProjects();
    } catch (err) {
        console.error(err);
        alert("Update failed");
    }
}

// Handle project deletion
async function handleDelete(id) {
    if (!confirm("Are you sure you want to delete this project?")) return;

    try {
        // Call API to delete project
        await deleteProject(id);
        alert("Project deleted");
        // Reload
        loadMyProjects();
    } catch (err) {
        console.error(err);
        alert("Delete failed");
    }
}

document.getElementById("logoutBtn")?.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "home-page.html";
});

loadMyProjects();