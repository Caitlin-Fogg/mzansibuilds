async function loadMyRequests() {
    try {
        const requests = await getMyRequests();

        const container = document.getElementById("myRequests");
        container.innerHTML = "";

        requests.forEach(req => {
            const div = document.createElement("div");

            div.innerHTML = `
                <p><b>Project Title:</b> ${req.project_title}</p>
                <p>${req.message}</p>
                <p>Status: ${req.status}</p>
                <hr/>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error(err);
    }
}

loadMyRequests();