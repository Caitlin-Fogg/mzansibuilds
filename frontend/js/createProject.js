// Handles creation of new projects
// Ensures user is authenticated before allowing submission

// Check if user is logged in before allowing access
function ensureLoggedIn() {
    const token = localStorage.getItem("token");
    // Redirects user to login page if no token found
    if (!token) {
        window.location.href = "login.html";
    }
}

// Handle project creation form submission
document.getElementById("projectForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    ensureLoggedIn();

    // Retrieve user input values from form fields
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const stage = document.getElementById("stage").value;
    const support = document.getElementById("support").value;

    // Construct project object to send to backend
    // Status defaults to "active" for new projects
    const projectData = {title: title, description: description, stage: stage, support_needed: support, status: "active"};

    try {
        // Send POST request to backend to create project
        await apiRequest("/projects/", "POST", projectData);

        alert("Project created!");
        window.location.href = "index.html";

    } catch (error) {
        console.error(error);
        alert("Failed to create project");
    }
});