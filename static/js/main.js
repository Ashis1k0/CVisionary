document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsSection = document.getElementById('resultsSection');
    const atsScoreSection = document.getElementById('atsScoreSection');
    const jobRecommendationsSection = document.getElementById('jobRecommendationsSection');

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        try {
            loadingOverlay.classList.remove('hidden');
            const formData = new FormData();
            formData.append('resume', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                displayResults(data.parsed_data);
                if (data.improvements && data.improvements.length > 0) {
                    displayImprovements(data.improvements);
                }
                resultsSection.classList.remove('hidden');
            } else {
                throw new Error(data.error || 'Failed to process resume');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing resume: ' + error.message);
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    }

    function displayResults(data) {
        // Display personal details
        document.getElementById('name').textContent = data.name || 'N/A';
        document.getElementById('email').textContent = data.email || 'N/A';
        document.getElementById('phone').textContent = data.phone || 'N/A';

        // Display skills with improved formatting
        const skillsContainer = document.getElementById('skills');
        skillsContainer.innerHTML = '';
        if (data.skills && data.skills.length) {
            const skillsWrapper = document.createElement('div');
            skillsWrapper.className = 'skills-wrapper';
            
            // Group skills into categories (you can adjust these categories)
            const categories = {
                'Programming Languages': ['Python', 'C++', 'Java', 'JavaScript', 'PHP'],
                'Web Technologies': ['HTML', 'CSS', 'React', 'Node.js', 'Angular'],
                'Data & AI': ['Machine Learning', 'Data Analysis', 'Artificial Intelligence', 'Computer Vision'],
                'Tools & Technologies': ['Git', 'Linux', 'SQL', 'Docker', 'AWS'],
                'Other': []
            };

            // Sort skills into categories
            const categorizedSkills = {};
            data.skills.forEach(skill => {
                let found = false;
                for (const [category, keywords] of Object.entries(categories)) {
                    if (keywords.some(keyword => skill.toLowerCase().includes(keyword.toLowerCase()))) {
                        if (!categorizedSkills[category]) {
                            categorizedSkills[category] = [];
                        }
                        categorizedSkills[category].push(skill);
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    if (!categorizedSkills['Other']) {
                        categorizedSkills['Other'] = [];
                    }
                    categorizedSkills['Other'].push(skill);
                }
            });

            // Create skill sections for each category
            for (const [category, skills] of Object.entries(categorizedSkills)) {
                if (skills.length > 0) {
                    const categorySection = document.createElement('div');
                    categorySection.className = 'skills-category';
                    
                    const categoryTitle = document.createElement('h4');
                    categoryTitle.className = 'category-title';
                    categoryTitle.innerHTML = `<i class="fas fa-chevron-right"></i> ${category}`;
                    categorySection.appendChild(categoryTitle);

                    const skillsList = document.createElement('div');
                    skillsList.className = 'skills-list';
                    
                    skills.forEach(skill => {
                        const skillTag = document.createElement('span');
                        skillTag.className = 'skill-tag';
                        skillTag.textContent = skill;
                        skillsList.appendChild(skillTag);
                    });

                    categorySection.appendChild(skillsList);
                    skillsWrapper.appendChild(categorySection);
                }
            }
            
            skillsContainer.appendChild(skillsWrapper);
        } else {
            skillsContainer.textContent = 'No skills listed';
        }

        // Add CSS for the new skills styling
        const style = document.createElement('style');
        style.textContent = `
            .skills-wrapper {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
                padding: 0.5rem;
            }

            .skills-category {
                background-color: white;
                border-radius: 0.5rem;
                padding: 1rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }

            .category-title {
                font-size: 1rem;
                font-weight: 600;
                color: var(--text-color);
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .category-title i {
                color: var(--primary-color);
                font-size: 0.875rem;
            }

            .skills-list {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                padding-left: 1.5rem;
            }

            .skill-tag {
                background-color: #f0f9ff;
                color: #0369a1;
                padding: 0.375rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                font-weight: 500;
                transition: all 0.2s ease;
            }

            .skill-tag:hover {
                background-color: #e0f2fe;
                transform: translateY(-1px);
            }

            @media (max-width: 768px) {
                .skills-list {
                    padding-left: 0.75rem;
                }

                .skill-tag {
                    font-size: 0.75rem;
                    padding: 0.25rem 0.5rem;
                }
            }
        `;
        document.head.appendChild(style);

        // Display education
        const educationContainer = document.getElementById('education');
        educationContainer.innerHTML = '';
        if (data.education && data.education.length) {
            data.education.forEach(edu => {
                const eduDiv = document.createElement('div');
                eduDiv.className = 'education-item';
                eduDiv.innerHTML = `
                    <p><strong>${edu.degree || ''}</strong></p>
                    <p>${edu.institution || ''} (${edu.year || ''})</p>
                `;
                educationContainer.appendChild(eduDiv);
            });
        } else {
            educationContainer.textContent = 'No education listed';
        }

        // Display experience
        const experienceContainer = document.getElementById('experience');
        experienceContainer.innerHTML = '';
        if (data.experience && data.experience.length) {
            data.experience.forEach(exp => {
                const expDiv = document.createElement('div');
                expDiv.className = 'experience-item';
                expDiv.innerHTML = `
                    <p><strong>${exp.title || ''}</strong></p>
                    <p>${exp.company || ''} (${exp.duration || ''})</p>
                `;
                experienceContainer.appendChild(expDiv);
            });
        } else {
            experienceContainer.textContent = 'No experience listed';
        }

        // Display projects
        const projectsContainer = document.getElementById('projects');
        projectsContainer.innerHTML = '';
        if (data.projects && data.projects.length) {
            data.projects.forEach(project => {
                const projectDiv = document.createElement('div');
                projectDiv.className = 'project-item';
                projectDiv.innerHTML = `
                    <p><strong>${project.title || ''}</strong></p>
                    <p>${project.description || ''}</p>
                    <p><em>Technologies: ${project.technologies ? project.technologies.join(', ') : ''}</em></p>
                `;
                projectsContainer.appendChild(projectDiv);
            });
        } else {
            projectsContainer.textContent = 'No projects listed';
        }
    }

    function displayImprovements(improvements) {
        const improvementsList = document.getElementById('improvementsList');
        improvementsList.innerHTML = '';
        
        improvements.forEach(improvement => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i>${improvement}`;
            improvementsList.appendChild(li);
        });

        // Show the improvements section
        document.getElementById('atsScoreSection').classList.remove('hidden');
    }

    // Handle ATS Score button click
    document.getElementById('atsScoreBtn').addEventListener('click', async () => {
        try {
            const response = await fetch('/ats-score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    parsed_data: {
                        name: document.getElementById('name').textContent,
                        email: document.getElementById('email').textContent,
                        phone: document.getElementById('phone').textContent,
                        skills: Array.from(document.getElementById('skills').children).map(skill => skill.textContent),
                        education: Array.from(document.getElementById('education').children).map(edu => edu.textContent),
                        experience: Array.from(document.getElementById('experience').children).map(exp => exp.textContent)
                    }
                })
            });

            const data = await response.json();
            if (data.score !== undefined) {
                document.getElementById('atsScoreValue').textContent = Math.round(data.score);
                atsScoreSection.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error calculating ATS score');
        }
    });

    // Handle Job Recommendations button click
    document.getElementById('jobRecommendBtn').addEventListener('click', async () => {
        try {
            const loadingOverlay = document.getElementById('loadingOverlay');
            loadingOverlay.classList.remove('hidden');
            
            const skills = Array.from(document.getElementById('skills').children)
                .map(skill => skill.textContent.trim())
                .filter(skill => skill);  // Remove empty skills
                
            if (!skills.length) {
                throw new Error('No skills found in the resume');
            }

            const response = await fetch('/job-recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ skills })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to get job recommendations');
            }

            if (data.recommendations && data.recommendations.length) {
                displayJobRecommendations(data.recommendations);
                document.getElementById('jobRecommendationsSection').classList.remove('hidden');
                
                // Scroll to recommendations
                document.getElementById('jobRecommendationsSection').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            } else {
                throw new Error('No recommendations received');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message || 'Error getting job recommendations');
        } finally {
            document.getElementById('loadingOverlay').classList.add('hidden');
        }
    });

    function displayJobRecommendations(recommendations) {
        const recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = '';

        recommendations.forEach(job => {
            const jobCard = document.createElement('div');
            jobCard.className = 'analysis-card job-card';
            
            // Calculate match percentage color
            const matchColor = job.match_percentage >= 80 ? '#16a34a' : 
                             job.match_percentage >= 60 ? '#ca8a04' : 
                             '#dc2626';
            
            jobCard.innerHTML = `
                <h3>
                    <i class="fas fa-briefcase"></i>
                    ${job.title}
                    <span class="match-badge" style="background-color: ${matchColor}">
                        ${Math.round(job.match_percentage)}% Match
                    </span>
                </h3>
                <div class="card-content">
                    <p class="job-description">${job.description}</p>
                    
                    <div class="skills-section">
                        <h4><i class="fas fa-check-circle"></i> Matching Skills</h4>
                        <div class="skills-list">
                            ${job.matching_skills.map(skill => 
                                `<span class="skill-tag matching">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div class="skills-section">
                        <h4><i class="fas fa-plus-circle"></i> Recommended Skills</h4>
                        <div class="skills-list">
                            ${job.recommended_skills.map(skill => 
                                `<span class="skill-tag recommended">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            `;
            recommendationsList.appendChild(jobCard);
        });

        // Add CSS for the new styles
        const style = document.createElement('style');
        style.textContent = `
            .job-card {
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            .job-card:hover {
                transform: translateY(-4px);
                box-shadow: var(--hover-shadow);
            }
            
            .match-badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                color: white;
                font-size: 0.875rem;
                font-weight: 500;
                margin-left: 0.75rem;
            }
            
            .skills-section {
                margin-top: 1rem;
            }
            
            .skills-section h4 {
                font-size: 0.875rem;
                font-weight: 600;
                color: var(--text-color);
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .skills-list {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
            }
            
            .skill-tag {
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 500;
            }
            
            .skill-tag.matching {
                background-color: #e0f2fe;
                color: #0369a1;
            }
            
            .skill-tag.recommended {
                background-color: #fef3c7;
                color: #92400e;
            }
            
            .job-description {
                margin: 0.75rem 0;
                line-height: 1.5;
            }
        `;
        document.head.appendChild(style);
    }
});
