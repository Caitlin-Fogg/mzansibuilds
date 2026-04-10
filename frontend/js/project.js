function getProjectId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
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

    } catch (error) {
        console.error(error);
        alert("Failed to load project");
    }

    const currentUserId = getCurrentUserId();

    if (Number(currentUserId) === Number(project.user_id)) {
        // Owner
        document.getElementById("collabRequestsSection").style.display = "block";
        loadCollabRequests(id);
    } else {
        // Not owner
        document.getElementById("collabRequestSection").style.display = "block";
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
    if (!token) return null;

    const decoded = parseJwt(token);
    return decoded.user_id; 
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