let currentProjectId = null;
let isOwner = false;

function getProjectId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function isReadOnly() {
    const params = new URLSearchParams(window.location.search);
    return params.get("readonly") === "true";
}

async function loadProject() {
    const id = getProjectId();

    try {
        const project = await apiRequest(`/projects/${id}`);

        document.getElementById("title").innerText = project.title;
        document.getElementById("description").innerText = project.description;
        document.getElementById("stage").innerText = "Stage: " + project.stage;
        document.getElementById("support").innerText = "Support: " + project.support_needed;
        document.getElementById("status").innerText = "Status: " + project.status;

        const currentUserId = getCurrentUserId();

        console.log("DEBUG currentUserId:", currentUserId);
        console.log("DEBUG project.user_id:", project.user_id);

        const readOnly = isReadOnly();

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

    } catch (error) {
        console.error(error);
        alert("Failed to load project");
    }
}

async function loadMilestones(projectId) {
    try {
        const data = await getMilestones(projectId);

        const container = document.getElementById("milestones");
        container.innerHTML = "";

        const currentUserId = getCurrentUserId();
        const ownerId = data.project_owner_id;
        const milestones = data.milestones;

        const readOnly = isReadOnly();
        isOwner = Number(ownerId) === Number(currentUserId) && !readOnly;

        milestones.forEach(m => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h4 ${isOwner ? 'contenteditable="true"' : ''} id="title-${m.id}">
                    ${m.title}
                </h4>

                <p ${isOwner ? 'contenteditable="true"' : ''} id="desc-${m.id}">
                    ${m.description || ""}
                </p>

                <small>Created: ${new Date(m.created_at).toLocaleString()}</small>

                ${isOwner ? `
                    <div>
                        <button onclick="saveMilestone(${m.id})">Save</button>
                        <button onclick="deleteMilestoneUI(${m.id})">Delete</button>
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

async function saveMilestone(id) {
    const title = document.getElementById(`title-${id}`).innerText;
    const description = document.getElementById(`desc-${id}`).innerText;

    try {
        await updateMilestone(id, {
            title,
            description
        });

        loadMilestones(currentProjectId);
    } catch (err) {
        console.error(err);
        alert("Failed to update milestone");
    }
}

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

async function loadComments() {
    const id = getProjectId();

    try {
        const comments = await apiRequest(`/projects/${id}/comments`);

        const container = document.getElementById("comments");
        container.innerHTML = "";

        comments.forEach(comment => {
            const div = document.createElement("div");

            div.innerHTML = `
                <p>${comment.content}</p>
                <small>By: ${comment.username}</small>
                <hr/>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error(error);
    }
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = atob(base64Url);
    return JSON.parse(base64);
}

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

document.getElementById("commentForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = getProjectId();
    const text = document.getElementById("commentText").value;

    try {
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

document.getElementById("collabForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = getProjectId();
    const message = document.getElementById("collabMessage").value;

    try {
        await requestCollaboration(id, message);
        alert("Request sent!");
        document.getElementById("collabMessage").value = "";
    } catch (err) {
        console.error(err);
        alert("Failed to send request");
    }
});

async function loadCollabRequests(projectId) {
    try {
        const requests = await getProjectRequests(projectId);

        const container = document.getElementById("collabRequests");
        container.innerHTML = "";

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

async function handleAccept(id) {
    await acceptRequest(id);
    loadCollabRequests(getProjectId());
}

async function handleReject(id) {
    await rejectRequest(id);
    loadCollabRequests(getProjectId());
}

loadProject();
loadComments();