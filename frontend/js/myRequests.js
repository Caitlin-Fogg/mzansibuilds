// Handles display of collaboration requests made by the current user
// Allows users to view status and delete pending/rejected requests

// Fetch and display user's collaboration requests
async function loadMyRequests() {
    try {
        const requests = await getMyRequests();

        const container = document.getElementById("myRequests");
        container.innerHTML = "";

        if (requests.length === 0) {
            container.innerHTML = "<p>No requests have been made yet</p>";
            return;
        }

        // Render requests
        requests.forEach(req => {
            const div = document.createElement("div");
            div.classList.add("request-item");

            div.innerHTML = `
                <p><b>Project Title:</b> ${req.project_title}</p>
                <p>${req.message || ""}</p>
                <p>Status: ${req.status}</p>

                ${
                    // Show delete option only for pending or rejected requests
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

// Delete a collaboration request
async function deleteRequest(id) {
    if (!confirm("Delete this collaboration request?")) return;

    try {
        // Call API to delete request
        await deleteCollaborationRequest(id);
        // Reload
        loadMyRequests();
    } catch (err) {
        console.error(err);
        alert("Failed to delete request");
    }
}

loadMyRequests();