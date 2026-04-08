async function loadCompleted() {
    const projects = await apiRequest("/projects/completed");

    const container = document.getElementById("completed");

    projects.forEach(p => {
        const div = document.createElement("div");
        div.innerHTML = `<h3>${p.title}</h3>`;
        container.appendChild(div);
    });
}

loadCompleted();