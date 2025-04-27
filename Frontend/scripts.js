// frontend/scripts.js

const API_BASE_URL = "http://localhost:8000"; // Make sure this is correct
const API_KEY = "supersecretkey"; // Your API key

// Helper function to perform authenticated GET requests
async function fetchWithAuth(url) {
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
}

// Load available programs and display them on the dashboard
document.addEventListener("DOMContentLoaded", async () => {
    const programsList = document.getElementById("programs-list");
    try {
        const programs = await fetchWithAuth(`${API_BASE_URL}/programs/`);

        if (programs.length === 0) {
            programsList.innerHTML = "No programs available.";
            return;
        }

        programsList.innerHTML = "";
        programs.forEach(program => {
            const div = document.createElement("div");
            div.classList.add("program-item");
            div.innerHTML = `
                <h3>${program.name}</h3>
                <p>${program.description}</p>
            `;
            programsList.appendChild(div);
        });
    } catch (error) {
        console.error("Error loading programs:", error);
        programsList.innerHTML = "Error loading programs.";
    }
});

// Handle client form submission
const clientForm = document.getElementById("client-form");
if (clientForm) {
    clientForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const programId = document.getElementById("program").value;

        try {
            const response = await fetch(`${API_BASE_URL}/clients/`, {
                method: "POST",
                headers: {
                    "x-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name,
                    email,
                    program_id: parseInt(programId)
                })
            });

            const result = await response.json();
            const message = document.getElementById("response-msg");

            if (response.ok) {
                message.textContent = `Client "${result.name}" registered successfully!`;
                clientForm.reset();
            } else {
                message.textContent = `Error: ${result.detail || "Something went wrong"}`;
            }
        } catch (error) {
            console.error("Registration error:", error);
            document.getElementById("response-msg").textContent = "Failed to register client.";
        }
    });
}

// Fetch programs and populate the select dropdown
async function loadPrograms() {
    const programSelect = document.getElementById("program");
    const responseMsg = document.getElementById("response-msg");

    try {
        const response = await fetch(`${API_BASE_URL}/programs/`, {
            method: "GET",
            headers: {
                "x-api-key": API_KEY
            }
        });

        if (response.ok) {
            const programs = await response.json();
            if (programs.length === 0) {
                programSelect.innerHTML = `<option value="">No programs available</option>`;
                return;
            }

            // Clear existing options and populate the dropdown with programs
            programSelect.innerHTML = `<option value="">Select a program</option>`;
            programs.forEach(program => {
                const option = document.createElement("option");
                option.value = program.id;
                option.textContent = program.name;
                programSelect.appendChild(option);
            });
        } else {
            programSelect.innerHTML = `<option value="">Error loading programs</option>`;
            responseMsg.textContent = "Failed to load programs.";
        }
    } catch (error) {
        console.error("Error loading programs:", error);
        programSelect.innerHTML = `<option value="">Error loading programs</option>`;
        responseMsg.textContent = "Failed to load programs.";
    }
}

// Load programs when the page is ready
document.addEventListener("DOMContentLoaded", loadPrograms);

// Handle program form submission
const programForm = document.getElementById("program-form");
if (programForm) {
    programForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const description = document.getElementById("description").value.trim();

        try {
            const response = await fetch(`${API_BASE_URL}/programs/`, {
                method: "POST",
                headers: {
                    "x-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, description })
            });

            const result = await response.json();
            const message = document.getElementById("program-msg");

            if (response.ok) {
                message.textContent = ` Program "${result.name}" created successfully!`;
                programForm.reset();
            } else {
                message.textContent = ` Error: ${result.detail || "Something went wrong"}`;
            }
        } catch (error) {
            console.error("Program creation error:", error);
            document.getElementById("program-msg").textContent = " Failed to create program.";
        }
    });
}

// Handle searching and displaying clients
const searchBtn = document.getElementById("search-btn");
if (searchBtn) {
    searchBtn.addEventListener("click", async () => {
        const query = document.getElementById("search").value.trim();
        const clientsList = document.getElementById("clients-list");
        clientsList.innerHTML = "Searching...";

        try {
            const clients = await fetchWithAuth(`${API_BASE_URL}/clients/`);


            const filtered = clients.filter(client =>
                client.name.toLowerCase().includes(query.toLowerCase()) ||
                client.email.toLowerCase().includes(query.toLowerCase())
            );

            if (filtered.length === 0) {
                clientsList.innerHTML = " No matching clients found.";
                return;
            }

            clientsList.innerHTML = "";
            filtered.forEach(client => {
                const div = document.createElement("div");
                div.textContent = `${client.name} (${client.email})`;
                div.style.cursor = "pointer";
                div.addEventListener("click", () => loadClientProfile(client.id));
                clientsList.appendChild(div);
            });
        } catch (error) {
            console.error("Error searching clients:", error);
            clientsList.innerHTML = " Error searching clients.";
        }
    });
}

// Load full client profile
async function loadClientProfile(clientId) {
    const profileDiv = document.getElementById("client-profile");
    profileDiv.innerHTML = "Loading...";

    try {
        const client = await fetchWithAuth(`${API_BASE_URL}/clients/${clientId}`);

        profileDiv.innerHTML = `
            <p><strong>Name:</strong> ${client.name}</p>
            <p><strong>Email:</strong> ${client.email}</p>
            <p><strong>Enrolled Program:</strong> ${client.program ? client.program.name : "None"}</p>
            <p><strong>Program Description:</strong> ${client.program ? client.program.description : "N/A"}</p>
        `;
    } catch (error) {
        console.error("Error loading profile:", error);
        profileDiv.innerHTML = " Failed to load client profile.";
    }
}


// Load clients and programs for the enrollment page
document.addEventListener("DOMContentLoaded", async () => {
    const clientSelect = document.getElementById("client-select");
    const programsList = document.getElementById("programs-list");
    const enrollBtn = document.getElementById("enroll-btn");
    const enrollmentMsg = document.getElementById("enrollment-msg");

    // Fetch and load clients
    const clients = await fetchWithAuth(`${API_BASE_URL}/clients/`);
    clients.forEach(client => {
        const option = document.createElement("option");
        option.value = client.id;
        option.textContent = `${client.name} (${client.email})`;
        clientSelect.appendChild(option);
    });

    // Fetch and display programs
    const programs = await fetchWithAuth(`${API_BASE_URL}/programs/`);
    programs.forEach(program => {
        const div = document.createElement("div");
        div.classList.add("program-checkbox");
        div.innerHTML = `
            <input type="checkbox" id="program-${program.id}" value="${program.id}">
            <label for="program-${program.id}">${program.name}</label>
        `;
        programsList.appendChild(div);
    });

    // Enroll the client in selected programs
    enrollBtn.addEventListener("click", async () => {
        const clientId = clientSelect.value;
        const selectedPrograms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                                      .map(checkbox => checkbox.value);

        if (!clientId || selectedPrograms.length === 0) {
            enrollmentMsg.textContent = " Please select a client and at least one program.";
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/clients/${clientId}/enroll/`, {
                method: "POST",
                headers: {
                    "x-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ program_ids: selectedPrograms })
            });

            const result = await response.json();

            if (response.ok) {
                enrollmentMsg.textContent = ` Client successfully enrolled in programs!`;
            } else {
                enrollmentMsg.textContent = ` Error: ${result.detail || "Something went wrong"}`;
            }
        } catch (error) {
            console.error("Enrollment error:", error);
            enrollmentMsg.textContent = " Failed to enroll client.";
        }
    });
});
