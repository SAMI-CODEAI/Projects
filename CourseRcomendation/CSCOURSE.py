import sqlite3
import json
from flask import Flask, request, jsonify, render_template_string
import random

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
    </script>
</body>
</html>
'''

def init_db():
    """Initialize the database with sample data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT,
            specialization TEXT,
            experience_years INTEGER,
            company TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill TEXT NOT NULL,
            platform TEXT,
            url TEXT,
            difficulty TEXT
        )
    """)
    
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_professionals = [
            ("Sarah Chen", "Python,TensorFlow,NumPy,Keras,Deep Learning", "AI", 5, "Google AI"),
            ("John Smith", "Python,React,JavaScript,HTML,CSS,Node.js", "Web Development", 7, "Microsoft"),
            ("Maria Garcia", "Python,Cryptography,Networking,Kali Linux", "Cybersecurity", 4, "Security Corp"),
            ("David Kim", "Python,SQL,Tableau,R,Machine Learning", "Data Science", 6, "Amazon"),
        ]
        cursor.executemany(
            "INSERT INTO users (name, skills, specialization, experience_years, company) VALUES (?, ?, ?, ?, ?)",
            sample_professionals
        )
        
        sample_courses = [
            ("Deep Learning Specialization", "Deep Learning", "Coursera", "https://coursera.org/deep-learning", "Intermediate"),
            ("Web Development Bootcamp", "HTML,CSS,JavaScript", "Udemy", "https://udemy.com/web-dev", "Beginner"),
            ("Ethical Hacking", "Cybersecurity", "edX", "https://edx.org/ethical-hacking", "Advanced"),
            ("Data Science Fundamentals", "Python,SQL", "DataCamp", "https://datacamp.com/data-science", "Beginner"),
        ]
        cursor.executemany(
            "INSERT INTO courses (name, skill, platform, url, difficulty) VALUES (?, ?, ?, ?, ?)",
            sample_courses
        )
    
    # Create free courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS free_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            platform TEXT NOT NULL,
            specialization TEXT NOT NULL,
            topic TEXT NOT NULL,
            skill_level TEXT,
            instructor TEXT,
            url TEXT NOT NULL,
            duration TEXT,
            language TEXT,
            description TEXT,
            rating FLOAT,
            type TEXT
        )
    """)
    
    # Sample free courses data
    cursor.execute("SELECT COUNT(*) FROM free_courses")
    if cursor.fetchone()[0] == 0:
        free_courses = [
            # AI/Machine Learning Courses
            ("Neural Networks from Scratch", "YouTube", "AI", "Deep Learning",
             "Advanced", "Sentdex",
             "https://www.youtube.com/playlist?list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3",
             "15 hours", "English",
             "Build neural networks from scratch with Python",
             4.8, "Video Series"),
             
            ("TensorFlow 2.0 Complete Course", "freeCodeCamp", "AI", "Deep Learning",
             "Intermediate", "Tim Ruscica",
             "https://www.youtube.com/watch?v=tPYj3fFJGjk",
             "7 hours", "English",
             "Comprehensive TensorFlow tutorial",
             4.9, "Video Course"),

            # Web Development Courses
            ("Full Stack Web Development Course", "freeCodeCamp", "Web Development", "Full Stack",
             "Beginner", "freeCodeCamp",
             "https://www.freecodecamp.org/learn/",
             "300 hours", "English",
             "Complete web development curriculum with certification",
             4.9, "Interactive Course"),
             
            ("React JS Course 2024", "YouTube", "Web Development", "Frontend",
             "Intermediate", "JavaScript Mastery",
             "https://www.youtube.com/watch?v=b9eMGE7QtTk",
             "12 hours", "English",
             "Modern React with projects and best practices",
             4.8, "Video Course"),

            # Cybersecurity Courses
            ("Complete Ethical Hacking Course", "freeCodeCamp", "Cybersecurity", "Ethical Hacking",
             "Intermediate", "Heath Adams",
             "https://www.youtube.com/watch?v=3Kq1MIfTWCE",
             "15 hours", "English",
             "Practical ethical hacking and penetration testing",
             4.7, "Video Course"),
             
            ("Network Security Course", "Cybrary", "Cybersecurity", "Network Security",
             "Beginner", "Cybrary",
             "https://www.cybrary.it/course/network-security/",
             "20 hours", "English",
             "Network security fundamentals and best practices",
             4.6, "Interactive Course"),

            # Data Science Courses
            ("Data Science for Beginners", "Microsoft", "Data Science", "Python",
             "Beginner", "Microsoft Learn",
             "https://github.com/microsoft/Data-Science-For-Beginners",
             "Self-paced", "English",
             "Complete data science curriculum by Microsoft",
             4.9, "Interactive Course"),
             
            ("Complete SQL Mastery", "YouTube", "Data Science", "SQL",
             "Intermediate", "Tech With Tim",
             "https://www.youtube.com/watch?v=HXV3zeQKqGY",
             "4 hours", "English",
             "SQL fundamentals to advanced concepts",
             4.7, "Video Course"),

            # Additional AI Courses
            ("Practical Machine Learning", "MIT OpenCourseWare", "AI", "Machine Learning",
             "Advanced", "MIT",
             "https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/",
             "12 weeks", "English",
             "MIT's introduction to machine learning",
             4.9, "University Course"),

            # Additional Web Development
            ("Node.js Tutorial", "YouTube", "Web Development", "Backend",
             "Intermediate", "Net Ninja",
             "https://www.youtube.com/playlist?list=PL4cUxeGkcC9jsz4LDYc6kv3ymONOKxwBU",
             "10 hours", "English",
             "Complete Node.js guide with Express",
             4.8, "Video Series"),

            # Additional Cybersecurity
            ("Web Security Academy", "PortSwigger", "Cybersecurity", "Web Security",
             "All Levels", "PortSwigger",
             "https://portswigger.net/web-security",
             "Self-paced", "English",
             "Free, hands-on web security training",
             4.9, "Interactive Labs"),

            # Additional Data Science
            ("Statistics for Data Science", "YouTube", "Data Science", "Statistics",
             "Beginner", "StatQuest",
             "https://www.youtube.com/c/joshstarmer",
             "20+ hours", "English",
             "Statistical concepts explained simply",
             4.9, "Video Series")
        ]
        
        cursor.executemany("""
            INSERT INTO free_courses (
                title, platform, specialization, topic, skill_level, instructor,
                url, duration, language, description, rating, type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, free_courses)
    
    conn.commit()
    conn.close()

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
    
    # Get professionals in the same specialization
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
        placeholders = ','.join('?' * len(missing_skills))
        cursor.execute(f"SELECT name, skill, platform, url, difficulty FROM courses WHERE skill IN ({placeholders})",
                      tuple(missing_skills))
        courses = cursor.fetchall()
    else:
        courses = []
    
    course_recommendations = [
        {
            "name": course[0],
            "skill": course[1],
            "platform": course[2],
            "url": course[3],
            "difficulty": course[4]
        }
        for course in courses
    ]
    
    conn.close()

    return jsonify({
        "missing_skills": list(missing_skills),
        "profile_comparisons": profile_comparisons,
        "course_recommendations": course_recommendations
    })

@app.route('/suggest', methods=['POST'])
def suggest_courses():
    data = request.get_json()
    specialization = data.get('specialization', '')
    
    # Get paid courses
    cursor.execute("""
        SELECT name, description, price, duration, instructor, platform, rating
        FROM courses 
        WHERE specialization = ?
        ORDER BY rating DESC
        LIMIT 3
    """, (specialization,))
    paid_courses = cursor.fetchall()
    
    # Get free courses
    cursor.execute("""
        SELECT title, description, duration, instructor, platform, rating, url, skill_level
        FROM free_courses 
        WHERE specialization = ?
        ORDER BY rating DESC
        LIMIT 3
    """, (specialization,))
    free_courses = cursor.fetchall()
    
    # Format the response
    response = {
        'paid_courses': [
            {
                'name': course[0],
                'description': course[1],
                'price': course[2],
                'duration': course[3],
                'instructor': course[4],
                'platform': course[5],
                'rating': course[6]
            } for course in paid_courses
        ],
        'free_courses': [
            {
                'name': course[0],
                'description': course[1],
                'duration': course[2],
                'instructor': course[3],
                'platform': course[4],
                'rating': course[5],
                'url': course[6],
                'skill_level': course[7]
            } for course in free_courses
        ]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
