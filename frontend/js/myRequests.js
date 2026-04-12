async function loadMyRequests() {
    try {
        const requests = await getMyRequests();

        const container = document.getElementById("myRequests");
        container.innerHTML = "";

        requests.forEach(req => {
            const div = document.createElement("div");
            div.classList.add("request-item");

            div.innerHTML = `
                <p><b>Project Title:</b> ${req.project_title}</p>
                <p>${req.message || ""}</p>
                <p>Status: ${req.status}</p>

                ${
                    (req.status === "pending" || req.status === "rejected")
                    ? `
                        <div class="request-actions">
                            <span onclick="deleteRequest(${req.id})" title="Delete">🗑️</span>
                        </div>
                    `
                    : ""
                }

                <hr/>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error(err);
    }
}

async function deleteRequest(id) {
    if (!confirm("Delete this collaboration request?")) return;

    try {
        await deleteCollaborationRequest(id);
        loadMyRequests();
    } catch (err) {
        console.error(err);
        alert("Failed to delete request");
    }
}

loadMyRequests();