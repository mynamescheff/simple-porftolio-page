const projectsContainer = document.getElementById('projects');

// Function to fetch projects data from the backend and display them
async function fetchAndDisplayProjects() {
    try {
        const response = await fetch('asd'); // Replace  with your backend URL
        const data = await response.json();

        // Clear existing projects
        projectsContainer.innerHTML = '';

        // Loop through the data and create project elements
        data.forEach(project => {
            const projectElement = document.createElement('div');
            projectElement.classList.add('project');

            const projectName = document.createElement('h2');
            projectName.textContent = project.name;

            const projectDescription = document.createElement('p');
            projectDescription.textContent = project.description;

            const technologiesUsed = document.createElement('p');
            technologiesUsed.textContent = `Technologies used: ${project.technologies}`;

            const projectLinks = document.createElement('p');
            projectLinks.innerHTML = `
                <a href="${project.project_link}" target="_blank">View Project</a>
                | 
                <a href="${project.repository_link}" target="_blank">GitHub Repository</a>
            `;

            projectElement.appendChild(projectName);
            projectElement.appendChild(projectDescription);
            projectElement.appendChild(technologiesUsed);
            projectElement.appendChild(projectLinks);

            projectsContainer.appendChild(projectElement);
        });
    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}

// Call the function to fetch and display projects when the page loads
window.addEventListener('load', fetchAndDisplayProjects);