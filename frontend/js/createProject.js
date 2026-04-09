function ensureLoggedIn() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html";
    }
}

document.getElementById("projectForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    ensureLoggedIn();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const stage = document.getElementById("stage").value;
    const support = document.getElementById("support").value;

    const projectData = {title: title, description: description, stage: stage, support_needed: support, status: "active"};

    try {
        await apiRequest("/projects/", "POST", projectData);

        alert("Project created!");
        window.location.href = "index.html";

    } catch (error) {
        console.error(error);
        alert("Failed to create project");
    }
});