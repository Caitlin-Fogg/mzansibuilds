/* Handles project detail page:
- Displaying project info
- Managing milestones, comments and collaboration requests
Includes role-based UI (owner vs non-owner)
*/

// Store current project ID and ownership state
let currentProjectId = null;
let isOwner = false;

// Store original milestone values during edit mode (for updating milestones)
const milestoneCache = {};

// Extract project id
function getProjectId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

// Check if page is in read-only mode (used for Celebration Wall)
function isReadOnly() {
    const params = new URLSearchParams(window.location.search);
    return params.get("readonly") === "true";
}

// Fetch and display project details
async function loadProject() {
    const id = getProjectId();

    try {
        // Retrieve project data from backend
        const project = await apiRequest(`/projects/${id}`);

        // Populate UI with project details
        document.getElementById("title").innerText = project.title;
        document.getElementById("description").innerText = project.description;
        document.getElementById("stage").innerText = "Stage: " + project.stage;
        document.getElementById("support").innerText = "Support: " + project.support_needed;
        document.getElementById("status").innerText = "Status: " + project.status;

        const currentUserId = getCurrentUserId();

        console.log("DEBUG currentUserId:", currentUserId);
        console.log("DEBUG project.user_id:", project.user_id);

        const readOnly = isReadOnly();

        // Show collaboration UI based on ownership and mode
        // If user is owner - show incoming requests
        // If not owner - allow sending collaboration request
        if (!readOnly) {
            if (Number(currentUserId) === Number(project.user_id)) {
                document.getElementById("collabRequestsSection").style.display = "block";
                loadCollabRequests(id);
            } else {
                document.getElementById("collabRequestSection").style.display = "block";
            }
        }

        currentProjectId = id;

        loadMilestones(id, currentUserId);
        loadCollaborators(id);

    } catch (error) {
        console.error(error);
        alert("Failed to load project");
    }
}

// Fetch and display milestones for the project
async function loadMilestones(projectId) {
    try {
        const data = await getMilestones(projectId);

        const container = document.getElementById("milestones");
        container.innerHTML = "";

        const currentUserId = getCurrentUserId();
        const ownerId = data.project_owner_id;
        const milestones = data.milestones;

        const readOnly = isReadOnly();
        // Determine ownership (controls UI permissions)
        isOwner = Number(ownerId) === Number(currentUserId) && !readOnly;

        if (milestones.length === 0) {
            container.innerHTML = "<p>No milestones</p>";
        }

        // Render each milestone
        milestones.forEach(m => {
            const div = document.createElement("div");

            div.id = `milestone-${m.id}`; 

            div.innerHTML = `
                <div>
                    <h4 class="milestone-title">${m.title}</h4>
                    <p class="milestone-desc">${m.description || ""}</p>
                    <small>Created: ${new Date(m.created_at).toLocaleString()}</small>
                </div>

                ${isOwner ? `
                    <div class="milestone-actions">
                        <span onclick="editMilestone(${m.id})" title="Edit">✏️</span>
                        <span onclick="deleteMilestoneUI(${m.id})" title="Delete">🗑️</span>
                    </div>
                ` : ""}

                <hr/>
            `;

            container.appendChild(div);
        });

        if (isOwner) {
            const addBox = document.createElement("div");

            addBox.innerHTML = `
                <h4>Add Milestone</h4>
                <input id="newMilestoneTitle" placeholder="Title" />
                <textarea id="newMilestoneDesc" placeholder="Description"></textarea>
                <button onclick="addMilestone()">Add</button>
            `;

            container.appendChild(addBox);
        }

    } catch (err) {
        console.error(err);
        alert("Failed to load milestones");
    }
}

// Add a new milestone (owner only)
async function addMilestone() {
    const title = document.getElementById("newMilestoneTitle").value;
    const description = document.getElementById("newMilestoneDesc").value;

    try {
        await createMilestone(currentProjectId, {
            title,
            description
        });

        loadMilestones(currentProjectId);
    } catch (err) {
        console.error(err);
        alert("Failed to add milestone");
    }
}

// Handles updating milestones
function editMilestone(id) {
    const container = document.getElementById(`milestone-${id}`);

    const titleEl = container.querySelector(".milestone-title");
    const descEl = container.querySelector(".milestone-desc");

    milestoneCache[id] = {
        title: titleEl.innerText,
        desc: descEl.innerText
    };

    titleEl.outerHTML = `
        <input class="edit-title" value="${milestoneCache[id].title}" />
    `;

    descEl.outerHTML = `
        <textarea class="edit-desc">${milestoneCache[id].desc}</textarea>
    `;

    container.querySelector(".milestone-actions").innerHTML = `
        <span onclick="saveMilestone(${id})">✅</span>
        <span onclick="cancelEdit(${id})">❌</span>
    `;
}

// Saving changes to milestone
async function saveMilestone(id) {
    const container = document.getElementById(`milestone-${id}`);

    const title = container.querySelector(".edit-title").value;
    const description = container.querySelector(".edit-desc").value;

    try {
        await updateMilestone(id, { title, description });

        loadMilestones(currentProjectId);

    } catch (err) {
        console.error(err);
        alert("Update failed");
    }
}

// Cancelling update
function cancelEdit(id) {
    const container = document.getElementById(`milestone-${id}`);

    const original = milestoneCache[id];

    container.querySelector(".edit-title").outerHTML =
        `<h4 class="milestone-title">${original.title}</h4>`;

    container.querySelector(".edit-desc").outerHTML =
        `<p class="milestone-desc">${original.desc}</p>`;

    container.querySelector(".milestone-actions").innerHTML = `
        <span onclick="editMilestone(${id})">✏️</span>
        <span onclick="deleteMilestoneUI(${id})">🗑️</span>
    `;
}

// Delete milestone
async function deleteMilestoneUI(id) {
    if (!confirm("Delete this milestone?")) return;

    try {
        await deleteMilestone(id);
        loadMilestones(currentProjectId);
    } catch (err) {
        console.error(err);
        alert("Failed to delete milestone");
    }
}

// Load comments for the project
async function loadComments() {
    const id = getProjectId();

    try {
        // Fetch comments from backend
        const comments = await apiRequest(`/projects/${id}/comments`);

        const container = document.getElementById("comments");
        container.innerHTML = "";

        if (comments.length === 0) {
            container.innerHTML = "<p>No comments</p>";
            return;
        }

        // Render comments with username
        // Show delete option only for comment owner
        comments.forEach(comment => {
            const div = document.createElement("div");

            div.innerHTML = `
                <p>${comment.content}</p>
                <small>By: ${comment.username}</small>

                ${comment.user_id === getCurrentUserId() ? `
                    <div class="comment-actions">
                        <span onclick="deleteComment(${comment.id})" title="Delete">🗑️</span>
                    </div>
                ` : ""}

                <hr/>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error(error);
    }
}

// Delete a comment (only allowed for owner)
async function deleteComment(id) {
    if (!confirm("Delete this comment?")) return;

    try {
        await apiRequest(`/comments/${id}`, "DELETE");
        loadComments();
    } catch (err) {
        console.error(err);
        alert("Failed to delete comment");
    }
}

// Decode JWT token to extract user information
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = atob(base64Url);
    return JSON.parse(base64);
}

// Get current user ID from stored JWT token
// Used to determine ownership and control UI behaviour
function getCurrentUserId() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.warn("No token found");
        return null;
    }

    try {
        const decoded = parseJwt(token);
        console.log("Decoded JWT:", decoded);
        return decoded.user_id || decoded.sub;
    } catch (e) {
        console.error("JWT decode failed:", e);
        return null;
    }
}

// Handle new comment submission
document.getElementById("commentForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = getProjectId();
    const text = document.getElementById("commentText").value;

    try {
        // Send comment to backend
        await apiRequest(`/projects/${id}/comments`, "POST", {
            content: text
        });

        document.getElementById("commentText").value = "";
        loadComments();

    } catch (error) {
        console.error(error);
        alert("Failed to post comment");
    }
});

// Handle collaboration request submission
document.getElementById("collabForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = getProjectId();
    const message = document.getElementById("collabMessage").value;

    try {
        // Send request with optional message
        await requestCollaboration(id, message);
        alert("Request sent!");
        document.getElementById("collabMessage").value = "";
    } catch (err) {
        console.error(err);
        alert("Failed to send request");
    }
});

// Load collaboration requests for project (owner only)
async function loadCollabRequests(projectId) {
    try {
        const requests = await getProjectRequests(projectId);

        const container = document.getElementById("collabRequests");
        container.innerHTML = "";

        if (requests.length === 0) {
            container.innerHTML = "<p>No requests yet</p>";
            return;
        }

        requests.forEach(req => {
            const div = document.createElement("div");

            div.innerHTML = `
                <p><b>${req.username}</b></p>
                <p>${req.message}</p>
                <p>Status: ${req.status}</p>
                ${
                    req.status === "pending" ? `
                    <button onclick="handleAccept(${req.id})">Accept</button>
                    <button onclick="handleReject(${req.id})">Reject</button>
                    ` : ""
                }
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error(err);
    }
}

// Get collaborators for a project
async function loadCollaborators(projectId) {
    try {
        const collaborators = await getCollaborators(projectId);

        const container = document.getElementById("collaborators");
        container.innerHTML = "";

        if (collaborators.length === 0) {
            container.innerHTML = "<p>No collaborators</p>";
            return;
        }

        collaborators.forEach(c => {
            const div = document.createElement("div");
            div.innerHTML = `
                <p>👤 ${c.username}</p>
            `;
            container.appendChild(div);
        });

    } catch (err) {
        console.error(err);
    }
}

// Accept collaboration request
async function handleAccept(id) {
    await acceptRequest(id);
    loadCollabRequests(getProjectId());
}

// Reject collaboration request
async function handleReject(id) {
    await rejectRequest(id);
    loadCollabRequests(getProjectId());
}

loadProject();
loadComments();