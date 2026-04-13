/*
Centralised API file for handling all backend requests, ensures:
- Consistent request structure
- Automatic token handling (authentication)
- Reusable functions for different features
*/

// Base URL for backend API
const BASE_URL = "http://127.0.0.1:8000";

// Retrieve JWT token from local storage
// Used to authenticate API requests
function getToken() {
    return localStorage.getItem("token");
}

// Generic API reuqest handler
// Handles GET, POST, PUT, DELETE methods, request body, authentication token and error handling
async function apiRequest(endpoint, method = "GET", data = null) {
    // Configure request options
    const options = {
        method: method,headers: {
            "Content-Type": "application/json",
        }
    };

    // Attach JWT token if available
    const token = getToken();
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    // Convert request data to JSON format
    if (data) {
        options.body = JSON.stringify(data);
    }

    // Send HTTP request to backend
    const response = await fetch(BASE_URL + endpoint, options);

    // Handle API errors
    if (!response.ok) {
        const text = await response.text();
        console.error("API ERROR:", response.status, text);
        throw new Error(`API request failed: ${response.status}`);
    }

    // Handle empty response (e.g., DELETE returns 204 No Content)
    if (response.status === 204) {
        return null;
    }

    return response.json();
}

// Project APIs
// Fetch projects belonging to the logged in user
function getMyProjects() {
    return apiRequest("/projects/me");
}

// Update a specific project
function updateProject(projectId, data) {
    return apiRequest(`/projects/${projectId}`, "PUT", data);
}

// Delete a project by ID
function deleteProject(projectId) {
    return apiRequest(`/projects/${projectId}`, "DELETE");
}

// Collaboration APIs
// Send collaboration request to a project
function requestCollaboration(projectId, message) {
    return apiRequest(`/projects/${projectId}/collaborate`, "POST", {
        message: message
    });
}

// Get all requests for a project (owner view)
function getProjectRequests(projectId) {
    return apiRequest(`/projects/${projectId}/requests`);
}

// Get requests made by current user
function getMyRequests() {
    return apiRequest(`/requests/me`);
}

// Accept a collaboration request (owner action)
function acceptRequest(requestId) {
    return apiRequest(`/requests/${requestId}/accept`, "PUT");
}

// Reject a collaboration request (owner action)
function rejectRequest(requestId) {
    return apiRequest(`/requests/${requestId}/reject`, "PUT");
}

// Delete a request (requester action)
function deleteCollaborationRequest(requestId) {
    return apiRequest(`/requests/${requestId}`, "DELETE");
}

// Celebration Wall API
// Fetch completed projects for display
function getCompletedProjects() {
    return apiRequest("/projects/completed");
}

// Milestone APIs
// Fetch milestones for a specific project
function getMilestones(projectId) {
    return apiRequest(`/projects/${projectId}/milestones`);
}

// Create a new milestone
function createMilestone(projectId, data) {
    return apiRequest(`/projects/${projectId}/milestones`, "POST", data);
}

// Update an existing milestone
function updateMilestone(milestoneId, data) {
    return apiRequest(`/milestones/${milestoneId}`, "PUT", data);
}

// Delete a milestone
function deleteMilestone(milestoneId) {
    return apiRequest(`/milestones/${milestoneId}`, "DELETE");
}


// Logout functionality - removes token from storage and redirects user to homepage
document.getElementById("logoutBtn")?.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "home-page.html";
});