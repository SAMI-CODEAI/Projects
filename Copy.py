import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DATABASE = 'course_recommendations.db'

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Career Path Advisor</title>
    <style>
        :root {
            --primary: #4CAF50;
            --background: #0a0a0a;
            --card-bg: #1a1a1a;
            --text: #ffffff;
            --secondary-text: #a0a0a0;
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Inter', -apple-system, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h2 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, var(--primary), #80e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .form-container {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }
        
        .form-container:hover {
            transform: translateY(-5px);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--secondary-text);
            font-size: 0.9em;
        }
        
        input, select {
            width: 100%;
            padding: 12px;
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text);
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        
        button {
            background: linear-gradient(45deg, var(--primary), #45a049);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
        }
        
        .results-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .step {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .step:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }
        
        .step h4 {
            color: var(--primary);
            margin-top: 0;
            font-size: 1.2em;
        }
        
        .skill-tag {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(76, 175, 80, 0.1);
            border-radius: 15px;
            margin: 4px;
            font-size: 0.9em;
            color: var(--primary);
        }
        
        .progress-bar {
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: var(--primary);
            transition: width 1s ease-in-out;
        }
        
        .section-title {
            margin: 40px 0 20px;
            font-size: 1.5em;
            color: var(--primary);
            border-bottom: 2px solid rgba(76, 175, 80, 0.2);
            padding-bottom: 10px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        select {
            background-color: var(--card-bg);
            color: var(--text);
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            width: 100%;
            font-size: 1em;
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%23ffffff' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 1rem center;
        }

        select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }

        .profile-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .profile-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .profile-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(45deg, var(--primary), #45a049);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.2em;
            color: white;
        }

        .profile-info {
            flex-grow: 1;
        }

        .profile-name {
            font-size: 1.2em;
            font-weight: bold;
            margin: 0;
            color: var(--text);
        }

        .profile-company {
            color: var(--primary);
            font-size: 0.9em;
        }

        .profile-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }

        .stat-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.2em;
            font-weight: bold;
            color: var(--primary);
        }

        .stat-label {
            font-size: 0.8em;
            color: var(--secondary-text);
        }

        .skills-section {
            margin-top: 15px;
        }

        .skills-title {
            font-size: 0.9em;
            color: var(--secondary-text);
            margin-bottom: 10px;
        }

        .match-indicator {
            display: flex;
            align-items: center;
            margin: 15px 0;
        }

        .match-label {
            min-width: 100px;
            color: var(--secondary-text);
        }

        .match-bar {
            flex-grow: 1;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin: 0 15px;
        }

        .match-value {
            color: var(--primary);
            font-weight: bold;
        }

        .course-platform {
            margin: 10px 0;
        }

        .platform-tag, .cert-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-right: 8px;
        }

        .platform-tag {
            background: rgba(76, 175, 80, 0.1);
            color: var(--primary);
        }

        .cert-tag {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
        }

        .course-stats {
            display: flex;
            gap: 15px;
            margin: 15px 0;
        }

        .stat {
            font-size: 0.9em;
            color: var(--secondary-text);
        }

        .difficulty-tag {
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }

        .difficulty-tag.beginner {
            background: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
        }

        .difficulty-tag.intermediate {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
        }

        .difficulty-tag.advanced {
            background: rgba(244, 67, 54, 0.1);
            color: #f44336
        }

        .section-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .tab-btn {
            padding: 10px 20px;
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .tab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
        }

        .section {
            display: none;
        }

        .section.active {
            display: block;
        }

        .course-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }

        .course-card:hover {
            transform: translateY(-5px);
        }

        .platform-tag {
            background: rgba(76, 175, 80, 0.1);
            color: var(--primary);
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }

        .price-tag {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }

        .course-link {
            display: inline-block;
            margin-top: 15px;
            color: var(--primary);
            text-decoration: none;
            transition: transform 0.3s ease;
        }

        .course-link:hover {
            transform: translateX(5px);
        }

        .match-bar {
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
            flex-grow: 1;
            margin: 0 10px;
        }

        .progress-fill {
            height: 100%;
            background: var(--primary);
            transition: width 1s ease-in-out;
        }

        .section-header {
            width: 100%;
            margin: 20px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
            color: #333;
        }

        .course-link {
            display: inline-block;
            padding: 8px 15px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 10px;
        }

        .course-link:hover {
            background-color: #45a049;
        }

        .course-description {
            margin-top: 10px;
            font-style: italic;
            color: #666;
        }

        .learning-resources-section {
            margin: 30px 0;
        }

        .resource-filters {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .filter-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            background: var(--card-bg);
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .filter-btn.active {
            background: var(--primary);
            color: white;
        }

        .resources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .resource-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.3s ease;
        }

        .resource-card:hover {
            transform: translateY(-5px);
        }

        .resource-platform {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            margin-bottom: 10px;
        }

        .resource-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .resource-meta {
            display: flex;
            gap: 15px;
            margin-bottom: 10px;
        }

        .meta-item {
            font-size: 0.9em;
            color: var(--secondary-text);
        }

        .resource-topics {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 10px;
        }

        .topic-tag {
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }

        .resource-link {
            display: inline-block;
            margin-top: 15px;
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.3s ease;
        }

        .resource-link:hover {
            background: var(--primary-dark);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Career Path Advisor</h2>
            <p>Analyze your skills and get personalized recommendations</p>
        </div>
        
        <div class="form-container">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" required placeholder="Enter your name">
            </div>
            
            <div class="form-group">
                <label for="skills">Skills</label>
                <input type="text" id="skills" required placeholder="e.g., Python, JavaScript, React">
            </div>
            
            <div class="form-group">
                <label for="specialization">Specialization</label>
                <select id="specialization" required>
                    <option value="">Select your specialization</option>
                    <option value="AI">Artificial Intelligence</option>
                    <option value="Web Development">Web Development</option>
                    <option value="Cybersecurity">Cybersecurity</option>
                    <option value="Data Science">Data Science</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="experience">Years of Experience</label>
                <input type="number" id="experience" required min="0" max="50">
            </div>
            
            <button onclick="submitForm()">Analyze Profile</button>
        </div>

        <div id="results" style="display: none;">
            <div class="section-title">Your Learning Roadmap</div>
            <div id="flowchart" class="results-container"></div>
            
            <div class="section-title">Profile Comparisons</div>
            <div id="comparisons" class="results-container"></div>
            
            <div class="section-title">Recommended Courses</div>
            <div id="courses" class="results-container"></div>
        </div>
    </div>

    <script>
        function submitForm() {
            const formData = {
                name: document.getElementById("name").value,
                skills: document.getElementById("skills").value,
                specialization: document.getElementById("specialization").value,
                experience: document.getElementById("experience").value
            };

            document.getElementById("results").style.display = "none";

            fetch('/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("results").style.display = "block";
                
                const flowchart = document.getElementById("flowchart");
                const comparisons = document.getElementById("comparisons");
                const courses = document.getElementById("courses");
                
                flowchart.innerHTML = "";
                comparisons.innerHTML = "";
                courses.innerHTML = "";

                // Display missing skills
                if (data.missing_skills.length === 0) {
                    flowchart.innerHTML = `
                        <div class="step fade-in">
                            <h4>Excellent Profile!</h4>
                            <p>You have all the core skills for this specialization.</p>
                        </div>
                    `;
                } else {
                    data.missing_skills.forEach((skill, index) => {
                        const step = document.createElement("div");
                        step.className = "step fade-in";
                        step.style.animationDelay = `${index * 0.1}s`;
                        step.innerHTML = `
                            <h4>${skill}</h4>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 0%"></div>
                            </div>
                        `;
                        flowchart.appendChild(step);
                        
                        // Animate progress bar
                        setTimeout(() => {
                            step.querySelector('.progress-fill').style.width = '100%';
                        }, 100);
                    });
                }

                // Display profile comparisons
                data.profile_comparisons.forEach((profile, index) => {
                    const profileDiv = document.createElement("div");
                    profileDiv.className = "profile-card fade-in";
                    profileDiv.style.animationDelay = `${index * 0.1}s`;
                    
                    const initials = profile.name.split(' ').map(n => n[0]).join('');
                    
                    profileDiv.innerHTML = `
                        <div class="profile-header">
                            <div class="profile-avatar">${initials}</div>
                            <div class="profile-info">
                                <h4 class="profile-name">${profile.name}</h4>
                                <div class="profile-company">${profile.company}</div>
                            </div>
                        </div>
                        
                        <div class="profile-stats">
                            <div class="stat-item">
                                <div class="stat-value">${profile.experience_years}+</div>
                                <div class="stat-label">Years Experience</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${profile.similarity_score}%</div>
                                <div class="stat-label">Profile Match</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${profile.common_skills.length}</div>
                                <div class="stat-label">Shared Skills</div>
                            </div>
                        </div>

                        <div class="match-indicator">
                            <span class="match-label">Profile Match</span>
                            <div class="match-bar">
                                <div class="progress-fill" style="width: ${profile.similarity_score}%"></div>
                            </div>
                            <span class="match-value">${profile.similarity_score}%</span>
                        </div>

                        <div class="skills-section">
                            <div class="skills-title">Shared Skills</div>
                            <div class="skills">
                                ${profile.common_skills.map(skill => 
                                    `<span class="skill-tag">${skill}</span>`
                                ).join('')}
                            </div>
                        </div>

                        <div class="skills-section">
                            <div class="skills-title">Skills to Acquire</div>
                            <div class="skills">
                                ${profile.missing_skills.map(skill => 
                                    `<span class="skill-tag" style="background: rgba(255, 87, 87, 0.1); color: #ff5757;">
                                        ${skill}
                                    </span>`
                                ).join('')}
                            </div>
                        </div>
                    `;
                    comparisons.appendChild(profileDiv);
                });

                // Display course recommendations
                data.course_recommendations.forEach((course, index) => {
                    const courseDiv = document.createElement("div");
                    courseDiv.className = "step fade-in";
                    courseDiv.style.animationDelay = `${index * 0.1}s`;
                    courseDiv.innerHTML = `
                        <h4>${course.name}</h4>
                        <div class="course-platform">
                            <span class="platform-tag">${course.platform}</span>
                            ${course.certification ? '<span class="cert-tag">Certification</span>' : ''}
                        </div>
                        <div class="course-stats">
                            <div class="stat">
                                <i class="fas fa-star"></i>
                                ${course.rating} (${(course.reviews_count/1000).toFixed(1)}k reviews)
                            </div>
                            <div class="stat">
                                <i class="fas fa-clock"></i>
                                ${course.duration_weeks} weeks
                            </div>
                            <div class="stat">
                                <i class="fas fa-tag"></i>
                                ${course.is_paid ? '$' + course.price : 'Free'}
                            </div>
                        </div>
                        <div class="skill-tags">
                            <span class="skill-tag">${course.skill}</span>
                            <span class="difficulty-tag ${course.difficulty.toLowerCase()}">${course.difficulty}</span>
                        </div>
                        <p class="course-description">${course.description}</p>
                        <div class="prerequisites">
                            <strong>Prerequisites:</strong> ${course.prerequisites}
                        </div>
                        <a href="${course.url}" target="_blank" class="course-link">
                            Learn More →
                        </a>
                    `;
                    courses.appendChild(courseDiv);
                });
            })
            .catch(error => console.error('Error:', error));
        }

        function createFlowchart(learningPath) {
            const container = document.getElementById('flowchart');
            container.innerHTML = `
                <div id="network-container" style="height: 600px; background: var(--card-bg); border-radius: 12px;"></div>
                <div id="node-details" class="node-details"></div>
            `;

            // Create nodes and edges
            const nodes = new vis.DataSet();
            const edges = new vis.DataSet();

            learningPath.forEach(path => {
                // Add node
                nodes.add({
                    id: path.id,
                    label: path.topic,
                    level: Math.floor(path.order),
                    color: {
                        background: path.difficulty === 'Beginner' ? '#4CAF50' :
                                   path.difficulty === 'Intermediate' ? '#FFA726' : '#F44336',
                        border: '#ffffff',
                        highlight: {
                            background: '#81C784',
                            border: '#ffffff'
                        }
                    },
                    font: { color: '#ffffff' }
                });

                // Add edge if there's a parent
                if (path.parent) {
                    const parentNode = learningPath.find(p => p.topic === path.parent);
                    if (parentNode) {
                        edges.add({
                            from: parentNode.id,
                            to: path.id,
                            arrows: 'to',
                            color: { color: '#ffffff', opacity: 0.6 }
                        });
                    }
                }
            });

            // Network configuration
            const options = {
                layout: {
                    hierarchical: {
                        direction: 'LR',
                        sortMethod: 'directed',
                        levelSeparation: 200,
                        nodeSpacing: 150
                    }
                },
                nodes: {
                    shape: 'box',
                    margin: 10,
                    widthConstraint: {
                        minimum: 120,
                        maximum: 120
                    }
                },
                edges: {
                    smooth: {
                        type: 'cubicBezier',
                        forceDirection: 'horizontal'
                    }
                },
                physics: false,
                interaction: {
                    hover: true,
                    tooltipDelay: 200
                }
            };

            // Create network
            const network = new vis.Network(
                document.getElementById('network-container'),
                { nodes, edges },
                options
            );

            // Handle node clicks
            network.on('click', function(params) {
                if (params.nodes.length) {
                    const nodeId = params.nodes[0];
                    const pathData = learningPath.find(p => p.id === nodeId);
                    showNodeDetails(pathData);
                }
            });
        }

        function showNodeDetails(pathData) {
            const detailsContainer = document.getElementById('node-details');
            detailsContainer.innerHTML = `
                <div class="topic-card fade-in">
                    <h3>${pathData.topic}</h3>
                    <div class="difficulty-tag ${pathData.difficulty.toLowerCase()}">
                        ${pathData.difficulty}
                    </div>
                    <p class="description">${pathData.description}</p>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Estimated Time</span>
                            <span class="stat-value">${pathData.hours} hours</span>
                        </div>
                    </div>
                    <div class="resources">
                        <h4>Learning Resources</h4>
                        <div class="resource-list">
                            ${pathData.resources.map(resource => `
                                <div class="resource-item">
                                    <span class="resource-icon">📚</span>
                                    ${resource}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }

        function displayCourses(courses) {
            const courseContainer = document.getElementById('courseContainer');
            courseContainer.innerHTML = ''; // Clear previous results
            
            // Add section header for paid courses
            if (courses.paid_courses && courses.paid_courses.length > 0) {
                const paidHeader = document.createElement('h3');
                paidHeader.textContent = 'Premium Courses';
                paidHeader.className = 'section-header';
                courseContainer.appendChild(paidHeader);
                
                // Display paid courses
                courses.paid_courses.forEach(course => {
                    const courseCard = createCourseCard(course, true);
                    courseContainer.appendChild(courseCard);
                });
            }
            
            // Add section header for free courses
            if (courses.free_courses && courses.free_courses.length > 0) {
                const freeHeader = document.createElement('h3');
                freeHeader.textContent = 'Free Learning Resources';
                freeHeader.className = 'section-header';
                courseContainer.appendChild(freeHeader);
                
                // Display free courses
                courses.free_courses.forEach(course => {
                    const courseCard = createCourseCard(course, false);
                    courseContainer.appendChild(courseCard);
                });
            }
        }

        function createCourseCard(course, isPaid) {
            const card = document.createElement('div');
            card.className = 'course-card';
            
            const title = course.name || course.title;
            const rating = course.rating ? `${course.rating}/5` : 'Not rated';
            
            card.innerHTML = `
                <h3>${title}</h3>
                <p><strong>Instructor:</strong> ${course.instructor}</p>
                <p><strong>Platform:</strong> ${course.platform}</p>
                <p><strong>Duration:</strong> ${course.duration}</p>
                <p><strong>Rating:</strong> ${rating}</p>
                ${isPaid ? `<p><strong>Price:</strong> $${course.price}</p>` : 
                           `<p><strong>Skill Level:</strong> ${course.skill_level}</p>
                            <p><a href="${course.url}" target="_blank" class="course-link">Access Course</a></p>`}
                <p class="course-description">${course.description}</p>
            `;
            
            return card;
        }

        function renderLearningResources(resources) {
            const container = document.getElementById('resources-container');
            container.innerHTML = resources.map(resource => `
                <div class="resource-card" data-type="${resource.type.toLowerCase()}">
                    <div class="resource-platform" style="background: ${getPlatformColor(resource.platform)}">
                        ${resource.platform}
                    </div>
                    <div class="resource-title">${resource.title}</div>
                    <div class="resource-meta">
                        <span class="meta-item">⭐ ${resource.rating}</span>
                        <span class="meta-item">⏱️ ${resource.duration}</span>
                        <span class="meta-item">${resource.difficulty}</span>
                    </div>
                    <div class="resource-description">${resource.description}</div>
                    <div class="resource-topics">
                        ${resource.topics.map(topic => 
                            `<span class="topic-tag">${topic}</span>`
                        ).join('')}
                    </div>
                    <a href="${resource.url}" target="_blank" class="resource-link">
                        Start Learning
                    </a>
                </div>
            `).join('');
        }

        function getPlatformColor(platform) {
            const colors = {
                'Coursera': '#2196F3',
                'YouTube': '#FF0000',
                'Google': '#4CAF50',
                'DataCamp': '#03A9F4',
                'freeCodeCamp': '#FF9800'
            };
            return colors[platform] || '#9C27B0';
        }

        // Add filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                
                // Update active button
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Filter resources
                document.querySelectorAll('.resource-card').forEach(card => {
                    if (filter === 'all' || 
                        (filter === 'free' && card.dataset.free === 'true') ||
                        card.dataset.type.includes(filter)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>
'''

def init_db():
    """Initialize database with enhanced profiles and courses."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables (existing structure)
    
    # Enhanced professional profiles with diverse backgrounds
    sample_professionals = [
        # AI/ML Expert
        ("Sarah Chen", 
         "python,tensorflow,pytorch,deep learning,machine learning,computer vision,nlp,data science,aws",
         "AI", 7, "Google Brain",
         "Led AI research team, Published in top conferences, Developed production ML systems",
         "Deep Learning, Computer Vision, NLP",
         "Google AI Professional, Stanford ML Specialization, AWS ML Certification"),
        
        # Full Stack Developer
        ("Michael Rodriguez", 
         "javascript,react,node.js,python,django,postgresql,aws,docker,kubernetes,typescript",
         "Web Development", 8, "Netflix",
         "Led frontend architecture, Built scalable microservices, Mentored junior developers",
         "Frontend Architecture, Cloud Infrastructure, DevOps",
         "AWS Solutions Architect, MongoDB Professional, Kubernetes Admin"),
        
        # Cybersecurity Expert
        ("Emma Thompson", 
         "python,networking,penetration testing,malware analysis,cloud security,incident response",
         "Cybersecurity", 6, "Microsoft Security",
         "Security research, Vulnerability assessment, Threat detection systems",
         "Threat Analysis, Network Security, Cloud Security",
         "CISSP, CEH, OSCP, AWS Security Specialist"),
    ]
    
    # Enhanced courses with detailed information
    core_courses = [
        # AI/ML Courses
        ("Deep Learning Specialization", "deep learning", "AI", "Coursera", 
         "https://coursera.org/deep-learning", "Advanced", "Andrew Ng", "5 months", 
         "Comprehensive deep learning curriculum covering neural networks, CNN, RNN, and more", 4.9),
        
        ("Computer Vision Nanodegree", "computer vision", "AI", "Udacity", 
         "https://udacity.com/cv", "Advanced", "Industry Experts", "4 months", 
         "Learn to build computer vision systems with deep learning", 4.8),
        
        ("Natural Language Processing", "nlp", "AI", "Stanford Online", 
         "https://stanford.edu/nlp", "Advanced", "Christopher Manning", "3 months", 
         "Advanced NLP concepts and implementations", 4.9),
        
        # Web Development Courses
        ("Full Stack Web Development", "web development", "Web Development", "freeCodeCamp", 
         "https://freecodecamp.org", "Beginner", "Community", "6 months", 
         "Complete web development from frontend to backend", 4.8),
        
        ("React and Redux Masterclass", "react", "Web Development", "Udemy", 
         "https://udemy.com/react-redux", "Intermediate", "Stephen Grider", "2 months", 
         "Modern React development with Redux and Hooks", 4.7),
        
        ("Cloud Native Development", "kubernetes", "Web Development", "Linux Foundation", 
         "https://linuxfoundation.org/cloud", "Advanced", "Industry Experts", "4 months", 
         "Learn cloud-native development with Kubernetes", 4.8),
        
        # Cybersecurity Courses
        ("Ethical Hacking", "penetration testing", "Cybersecurity", "Offensive Security", 
         "https://offensive-security.com", "Advanced", "Security Experts", "3 months", 
         "Hands-on penetration testing and ethical hacking", 4.9),
        
        ("Cloud Security", "cloud security", "Cybersecurity", "Cloud Security Alliance", 
         "https://cloudsecurityalliance.org", "Intermediate", "Industry Experts", "2 months", 
         "Comprehensive cloud security and compliance", 4.7),
        
        ("Incident Response", "incident response", "Cybersecurity", "SANS Institute", 
         "https://sans.org/ir", "Advanced", "SANS Instructors", "3 months", 
         "Advanced incident response and threat hunting", 4.8)
    ]
    
    # Enhanced skill details with comprehensive information
    skill_details = [
        # AI/ML Skills
        ("deep learning", "AI", 
         "Advanced neural network architectures and applications",
         "Machine Learning, Python, Mathematics",
         "Advanced", 160,
         "1. Neural Networks Fundamentals\n2. CNN Architectures\n3. RNN and LSTM\n4. Transformers\n5. GANs",
         "Research papers, PyTorch tutorials, Deep Learning courses",
         "Essential for AI research and advanced ML applications"),
        
        ("computer vision", "AI",
         "Image and video processing using deep learning",
         "Deep Learning, Python, Linear Algebra",
         "Advanced", 140,
         "1. Image Processing\n2. Object Detection\n3. Segmentation\n4. Face Recognition\n5. Video Analysis",
         "OpenCV, PyTorch Vision, Research papers",
         "Critical for autonomous systems and visual AI applications"),
        
        # Web Development Skills
        ("react", "Web Development",
         "Modern frontend development with React ecosystem",
         "JavaScript, HTML, CSS",
         "Intermediate", 120,
         "1. Components and Props\n2. State Management\n3. Hooks\n4. Performance\n5. Testing",
         "React docs, Redux toolkit, Testing libraries",
         "Essential for modern web development"),
        
        ("kubernetes", "Web Development",
         "Container orchestration and cloud-native development",
         "Docker, Linux, Networking",
         "Advanced", 160,
         "1. Container Basics\n2. Cluster Management\n3. Deployments\n4. Services\n5. Security",
         "Kubernetes docs, Cloud tutorials, Practice projects",
         "Critical for scalable cloud applications"),
        
        # Cybersecurity Skills
        ("penetration testing", "Cybersecurity",
         "Systematic security testing and vulnerability assessment",
         "Networking, Linux, Programming",
         "Advanced", 180,
         "1. Reconnaissance\n2. Vulnerability Assessment\n3. Exploitation\n4. Post-Exploitation\n5. Reporting",
         "CTF challenges, Lab practice, Security tools",
         "Essential for security assessment and hardening"),
        
        ("incident response", "Cybersecurity",
         "Handling and analyzing security incidents",
         "Network Security, Forensics, System Administration",
         "Advanced", 140,
         "1. Incident Detection\n2. Triage\n3. Analysis\n4. Containment\n5. Recovery",
         "SANS resources, Practice scenarios, Tool mastery",
         "Critical for security operations and threat response")
    ]
    
    # Insert data into tables
    cursor.executemany(
        "INSERT INTO users (name, skills, specialization, experience_years, company) VALUES (?, ?, ?, ?, ?)",
        [(p[0], p[1], p[2], p[3], p[4]) for p in sample_professionals]
    )
    
    cursor.executemany("""
        INSERT INTO courses (
            name, skill, specialization, platform, url, difficulty, 
            instructor, duration, description, rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, core_courses)
    
    cursor.executemany("""
        INSERT INTO skill_details (
            skill, specialization, description, prerequisites, difficulty,
            estimated_hours, learning_path, resources, career_impact
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, skill_details)
    
    conn.commit()
    conn.close()

# Add route to get learning resources
@app.route("/learning_resources", methods=["POST"])
def get_learning_resources():
    data = request.get_json()
    skill = data.get("skill", "").lower()
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, type, platform, url, duration, difficulty, rating,
               description, instructor, is_free, topics
        FROM learning_resources
        WHERE skill = ?
        ORDER BY rating DESC
    """, (skill,))
    
    resources = [{
        "title": row[0],
        "type": row[1],
        "platform": row[2],
        "url": row[3],
        "duration": row[4],
        "difficulty": row[5],
        "rating": row[6],
        "description": row[7],
        "instructor": row[8],
        "is_free": row[9],
        "topics": row[10].split(", ")
    } for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        "skill": skill,
        "resources": resources
    })

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/suggest", methods=["POST"])
def suggest():
    """Provide skill suggestions and profile comparisons."""
    data = request.get_json()
    user_skills = set(skill.strip().lower() for skill in data.get("skills", "").split(","))
    specialization = data.get("specialization")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get relevant professionals
    cursor.execute("SELECT name, skills, experience_years, company FROM users WHERE specialization = ?", (specialization,))
    professionals = cursor.fetchall()
    
    profile_comparisons = []
    all_required_skills = set()
    
    for prof in professionals:
        prof_skills = set(skill.strip().lower() for skill in prof[1].split(","))
        all_required_skills.update(prof_skills)
        common_skills = user_skills.intersection(prof_skills)
        similarity_score = len(common_skills) / len(prof_skills) * 100
        
        profile_comparisons.append({
            "name": prof[0],
            "common_skills": list(common_skills),
            "missing_skills": list(prof_skills - user_skills),
            "similarity_score": round(similarity_score, 1),
            "experience_years": prof[2],
            "company": prof[3]
        })
    
    # Get course recommendations
    missing_skills = all_required_skills - user_skills
    if missing_skills:
        cursor.execute("""
            SELECT name, skill, platform, url, difficulty, instructor, duration, description, rating
            FROM courses 
            WHERE specialization = ? 
            ORDER BY rating DESC
            LIMIT 3
        """, (specialization,))
        
        courses = cursor.fetchall()
        course_recommendations = [{
            "name": course[0],
            "skill": course[1],
            "platform": course[2],
            "url": course[3],
            "difficulty": course[4],
            "instructor": course[5],
            "duration": course[6],
            "description": course[7],
            "rating": course[8]
        } for course in courses]
    else:
        course_recommendations = []
    
    conn.close()

    return jsonify({
        "missing_skills": list(missing_skills),
        "profile_comparisons": profile_comparisons,
        "course_recommendations": course_recommendations
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
