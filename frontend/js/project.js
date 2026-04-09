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

loadProject();
loadComments();