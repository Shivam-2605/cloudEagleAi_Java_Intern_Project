// Constants
const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// State
let currentReportData = null;
let currentRawData = null;
let activeView = "user"; // 'user' or 'repo'

// DOM Elements
const form = document.getElementById("report-form");
const orgInput = document.getElementById("org-input");
const privateCheck = document.getElementById("private-checkbox");
const errorMsg = document.getElementById("error-message");
const loading = document.getElementById("loading");
const resultsSection = document.getElementById("results-section");
const toggleBtns = document.querySelectorAll(".toggle-btn");
const exportJsonBtn = document.getElementById("export-json");

// Event Listeners
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const org = orgInput.value.trim();
    const includePrivate = privateCheck.checked;
    
    if (org) {
        await fetchReport(org, includePrivate);
    }
});

toggleBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
        // Update active class
        toggleBtns.forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        
        // Update view
        activeView = e.target.dataset.view;
        renderTable();
    });
});

exportJsonBtn.addEventListener("click", () => {
    if (!currentRawData) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentRawData, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download",`github_report_${currentRawData.organization}.json⁠`);
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
});

// Core Fetch Function
async function fetchReport(org, includePrivate) {
    // Reset UI
    errorMsg.classList.add("hidden");
    resultsSection.classList.add("hidden");
    loading.classList.remove("hidden");

    try {
        const url =`${API_BASE_URL}/report/${org}?include_private=${includePrivate}`;
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.message || "An error occurred while fetching the report.");
        }

        // Store data and render
        currentRawData = data;
        currentReportData = data.report;
        
        renderStats(data.summary);
        renderTable();
        
        resultsSection.classList.remove("hidden");
    } catch (error) {
        errorMsg.textContent = error.message;
        errorMsg.classList.remove("hidden");
    } finally {
        loading.classList.add("hidden");
    }
}

function renderStats(summary) {
    document.getElementById("stat-repos").textContent = summary.total_repositories;
    document.getElementById("stat-users").textContent = summary.total_users;
    document.getElementById("stat-entries").textContent = summary.total_access_entries;
}

function renderTable() {
    if (!currentReportData) return;

    const thead = document.getElementById("table-head");
    const tbody = document.getElementById("table-body");
    
    thead.innerHTML = "";
    tbody.innerHTML = "";

    if (activeView === "user") {
        renderUserView(thead, tbody);
    } else {
        renderRepoView(thead, tbody);
    }
}

function renderUserView(thead, tbody) {
    thead.innerHTML = `
        <tr>
            <th>User</th>
            <th>Total Repos</th>
            <th>Access List (Repository : Role)</th>
        </tr>
    `;

    const users = Object.values(currentReportData.by_user).sort((a, b) => a.login.localeCompare(b.login));
    
    users.forEach(user => {
        const tr = document.createElement("tr");
        const reposHtml = user.repositories.map(repo => `
            <span class="badge badge-${repo.role}">${repo.name} : ${repo.role}</span>
        `).join(" ");

        tr.innerHTML = `
            <td>
                <div class="user-cell">
                    <img src="${user.avatar_url}" alt="${user.login}" class="user-avatar" onerror="this.src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'">
                    <a href="${user.profile_url}" target="_blank" style="color: var(--text-primary); text-decoration: none;"><strong>${user.login}</strong></a>
                </div>
            </td>
            <td>${user.repository_count}</td>
            <td style="line-height: 2;">${reposHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderRepoView(thead, tbody) {
    thead.innerHTML = `
        <tr>
            <th>Repository</th>
            <th>Total Users</th>
            <th>Access List (User : Role)</th>
        </tr>
    `;

    const repos = Object.values(currentReportData.by_repository).sort((a, b) => a.name.localeCompare(b.name));
    
    repos.forEach(repo => {
        const tr = document.createElement("tr");
        const usersHtml = repo.users.map(user => `
            <span class="badge badge-${user.role}">${user.login} : ${user.role}</span>
        `).join(" ");

        const privateBadge = repo.private ? '<span class="badge badge-private">Private</span>' : '';

        tr.innerHTML = `
            <td>
                <strong>${repo.name}</strong>
                ${privateBadge}
            </td>
            <td>${repo.user_count}</td>
            <td style="line-height: 2;">${usersHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}