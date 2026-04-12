const BASE_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("token");
}

async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method: method,headers: {
            "Content-Type": "application/json",
        }
    };

    const token = getToken();
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(BASE_URL + endpoint, options);

    if (!response.ok) {
        const text = await response.text();
        console.error("API ERROR:", response.status, text);
        throw new Error(`API request failed: ${response.status}`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

// Project APIs
function getMyProjects() {
    return apiRequest("/projects/me");
}

function updateProject(projectId, data) {
    return apiRequest(`/projects/${projectId}`, "PUT", data);
}

function deleteProject(projectId) {
    return apiRequest(`/projects/${projectId}`, "DELETE");
}

// Collaboration APIs
function requestCollaboration(projectId, message) {
    return apiRequest(`/projects/${projectId}/collaborate`, "POST", {
        message: message
    });
}

function getProjectRequests(projectId) {
    return apiRequest(`/projects/${projectId}/requests`);
}

function getMyRequests() {
    return apiRequest(`/requests/me`);
}

function acceptRequest(requestId) {
    return apiRequest(`/requests/${requestId}/accept`, "PUT");
}

function rejectRequest(requestId) {
    return apiRequest(`/requests/${requestId}/reject`, "PUT");
}

// Celebration Wall API
function getCompletedProjects() {
    return apiRequest("/projects/completed");
}

// Milestone APIs
function getMilestones(projectId) {
    return apiRequest(`/projects/${projectId}/milestones`);
}

function createMilestone(projectId, data) {
    return apiRequest(`/projects/${projectId}/milestones`, "POST", data);
}

function updateMilestone(milestoneId, data) {
    return apiRequest(`/milestones/${milestoneId}`, "PUT", data);
}

function deleteMilestone(milestoneId) {
    return apiRequest(`/milestones/${milestoneId}`, "DELETE");
}