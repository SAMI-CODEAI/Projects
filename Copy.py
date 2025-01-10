import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DATABASE = 'course_recommendations.db'

# Add these routes at the top of the file, after the app initialization
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/home')
def home():
    return render_template_string(HTML_TEMPLATE)

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Career Path Advisor - Get personalized learning recommendations">
    <meta name="keywords" content="Career Path, Learning, Technology, Education, Web Development, Data Science, Cybersecurity">
    <meta name="author" content="Career Guide">
    
    <title>Career Path Advisor</title>
    
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Favicon -->
    <link rel="apple-touch-icon" sizes="180x180" href="https://cdn-icons-png.flaticon.com/512/1693/1693746.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://cdn-icons-png.flaticon.com/512/1693/1693746.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://cdn-icons-png.flaticon.com/512/1693/1693746.png">
    <link rel="shortcut icon" href="https://cdn-icons-png.flaticon.com/512/1693/1693746.png">
    
    <!-- Open Graph / Social Media Meta Tags -->
    <meta property="og:title" content="Career Path Advisor">
    <meta property="og:description" content="Get personalized learning recommendations for your tech career">
    <meta property="og:image" content="https://cdn-icons-png.flaticon.com/512/1693/1693746.png">
    <meta property="og:url" content="https://your-domain.com">
    
    <!-- Theme Color for Browser -->
    <meta name="theme-color" content="#4CAF50">
    
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
            background: rgba(76, 175, 80, 0.1);  /* Light green background */
            color: #4CAF50;  /* Green text */
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 600;
            display: inline-block;
            margin: 5px 0;
        }

        .price-tag.free {
            background: rgba(76, 175, 80, 0.2);  /* Slightly darker green background */
            color: #4CAF50;  /* Green text */
            border: 1px solid rgba(76, 175, 80, 0.3);  /* Subtle border */
            animation: pulse 2s infinite;  /* Add subtle pulse animation */
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
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

        .roadmap-container {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .roadmap-step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 30px;
            position: relative;
            padding-left: 50px;
            animation: fadeIn 0.5s ease-out forwards;
        }

        .roadmap-step:before {
            content: '';
            position: absolute;
            left: 20px;
            top: 0;
            bottom: -30px;
            width: 2px;
            background: var(--primary);
            opacity: 0.3;
        }

        .roadmap-step:last-child:before {
            display: none;
        }

        .step-number {
            position: absolute;
            left: 10px;
            top: 0;
            width: 24px;
            height: 24px;
            background: var(--primary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.8em;
        }

        .step-content {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            flex-grow: 1;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .step-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .step-title {
            font-size: 1.2em;
            font-weight: bold;
            color: var(--primary);
            margin: 0;
        }

        .step-duration {
            font-size: 0.9em;
            color: var(--secondary-text);
            background: rgba(76, 175, 80, 0.1);
            padding: 4px 12px;
            border-radius: 15px;
        }

        .step-description {
            color: var(--text);
            margin-bottom: 15px;
            line-height: 1.5;
        }

        .step-resources {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .resource-tag {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text);
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .resource-tag i {
            color: var(--primary);
        }

        .site-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        .site-icon {
            font-size: 2.5em;
            color: var(--primary);
            background: linear-gradient(45deg, var(--primary), #80e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.1);
                opacity: 0.8;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }

        .site-title {
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, var(--primary), #80e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .site-subtitle {
            font-size: 1.2em;
            color: #4CAF50;
            margin: 0;
            padding: 5px 0;
            border-radius: 0;
            background: none;
            border: none;
            opacity: 0.9;
            transition: opacity 0.3s ease;
        }

        .site-subtitle:hover {
            opacity: 1;
        }

        /* Light mode variables */
        [data-theme="light"] {
            --primary: #4CAF50;
            --background: #ffffff;
            --card-bg: #f5f5f5;
            --text: #333333;
            --secondary-text: #666666;
        }

        /* Dark mode variables (your existing colors) */
        [data-theme="dark"] {
            --primary: #4CAF50;
            --background: #0a0a0a;
            --card-bg: #1a1a1a;
            --text: #ffffff;
            --secondary-text: #a0a0a0;
        }

        /* Theme toggle button styles */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--card-bg);
            border: 1px solid var(--primary);
            color: var(--text);
            padding: 8px;  /* Reduced padding */
            width: 40px;   /* Fixed width */
            height: 40px;  /* Fixed height */
            border-radius: 50%;  /* Make it circular */
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        .theme-toggle:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }

        .theme-toggle i {
            font-size: 1.2em;
        }

        /* Hide the text, show only the icon */
        .toggle-text {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="site-header">
            <i class="fas fa-brain site-icon"></i>
            <h1 class="site-title">Career Path Advisor</h1>
            <h2 class="site-subtitle">Course Recommendations</h2>
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

    <button class="theme-toggle" onclick="toggleTheme()">
        <i class="fas fa-moon"></i>
        <span class="toggle-text">Dark Mode</span>
    </button>

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
                        <div class="roadmap-container">
                            <div class="roadmap-step">
                                <div class="step-number">✓</div>
                                <div class="step-content">
                                    <div class="step-header">
                                        <h4 class="step-title">Excellent Profile!</h4>
                                        <span class="step-duration">Ready to Go</span>
                                    </div>
                                    <p class="step-description">You have all the core skills for this specialization.</p>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    flowchart.innerHTML = `
                        <div class="roadmap-container">
                            <div class="roadmap-header">
                                <h3>Your Learning Journey</h3>
                                <p>Master these skills to advance in your career</p>
                            </div>
                            ${data.missing_skills.map((skill, index) => `
                                <div class="roadmap-step" style="animation-delay: ${index * 0.1}s">
                                    <div class="step-number">${index + 1}</div>
                                    <div class="step-content">
                                        <div class="step-header">
                                            <h4 class="step-title">${skill}</h4>
                                            <span class="step-duration">Estimated: ${getSkillDuration(skill)}</span>
                                        </div>
                                        <p class="step-description">
                                            ${getSkillDescription(skill, data.specialization)}
                                        </p>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `;
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
            const courseContainer = document.getElementById('courses');
            courseContainer.innerHTML = '';
            
            courses.forEach(course => {
                const courseCard = document.createElement('div');
                courseCard.className = 'course-card';
                
                const priceTag = course.is_paid ? 
                    `<span class="price-tag">
                        $${course.price}
                    </span>` : 
                    `<span class="price-tag free">
                        <i class="fas fa-gift"></i> Free
                    </span>`;
                
                courseCard.innerHTML = `
                    <h3>${course.name}</h3>
                    <div class="course-platform">
                        <span class="platform-tag">${course.platform}</span>
                    </div>
                    <div class="course-stats">
                        <div class="stat">
                            <i class="fas fa-star"></i> ${course.rating}/5
                        </div>
                        <div class="stat">
                            <i class="fas fa-clock"></i> ${course.duration}
                        </div>
                    </div>
                    ${priceTag}
                    <p>${course.description}</p>
                    <a href="${course.url}" target="_blank" class="course-link">
                        Learn More →
                    </a>
                `;
                
                courseContainer.appendChild(courseCard);
            });
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

        function getSkillDescription(skill, specialization) {
            const skillDescriptions = {
                // AI/ML skill descriptions
                'keras': "A powerful deep learning framework essential for building and training neural networks quickly. Used extensively in AI for rapid prototyping and research.",
                'tensorflow': "Google's flagship deep learning framework, crucial for developing and deploying large-scale machine learning models in production AI systems.",
                'pytorch': "Facebook's dynamic deep learning framework, preferred in AI research for its flexibility and debugging capabilities.",
                'deep learning': "Core technology behind modern AI, enabling machines to learn from examples and recognize complex patterns in data.",
                'machine learning': "Fundamental AI technology that allows systems to learn from data and make intelligent decisions without explicit programming.",
                'computer vision': "Essential AI field for processing and analyzing visual data, enabling applications like facial recognition and autonomous vehicles.",
                'nlp': "Natural Language Processing is key to AI applications that understand, interpret, and generate human language.",
                'neural networks': "Foundational structures in AI that mimic human brain function, crucial for deep learning applications.",
                
                // Web Development skill descriptions
                'javascript': "Core programming language for web development, essential for creating interactive and dynamic web applications.",
                'react': "Popular JavaScript library for building user interfaces, crucial for modern web application development.",
                'node.js': "Server-side JavaScript runtime, enabling full-stack JavaScript development and scalable web applications.",
                'python': "Versatile programming language used in web backends, offering extensive libraries and frameworks.",
                'django': "Robust Python web framework for building secure and maintainable web applications quickly.",
                'postgresql': "Advanced open-source database system for storing and managing application data reliably.",
                'aws': "Leading cloud platform providing essential services for modern web application deployment and scaling.",
                'docker': "Containerization technology crucial for consistent development and deployment environments.",
                
                // Cybersecurity skill descriptions
                'networking': "Fundamental knowledge for understanding and securing computer networks and communication systems.",
                'penetration testing': "Essential security skill for identifying and fixing vulnerabilities before they can be exploited.",
                'malware analysis': "Critical capability for understanding and defending against malicious software threats.",
                'cloud security': "Vital expertise for protecting cloud-based systems and data in modern infrastructure.",
                'network security': "Core competency for protecting computer networks from unauthorized access and attacks.",
                'cryptography': "Essential science of securing communication and data through encryption techniques.",
                'incident response': "Crucial skill for effectively handling and recovering from security breaches.",
                'forensics': "Important capability for investigating security incidents and collecting digital evidence.",
                
                // Data Science skill descriptions
                'statistics': "Fundamental knowledge for analyzing data and drawing meaningful conclusions.",
                'data visualization': "Essential skill for communicating insights and patterns found in complex datasets.",
                'sql': "Critical language for managing and querying structured databases in data analysis.",
                'r': "Powerful programming language specialized for statistical computing and graphics.",
                'pandas': "Essential Python library for data manipulation and analysis.",
                'numpy': "Fundamental package for scientific computing with Python.",
                'scikit-learn': "Core machine learning library for data science in Python.",
                'hadoop': "Framework for distributed storage and processing of big data.",
                'spark': "Fast and general-purpose cluster computing system for big data processing."
            };

            return skillDescriptions[skill.toLowerCase()] || 
                   `Master ${skill} to enhance your expertise in ${specialization}. This skill is crucial for professional development in this field.`;
        }

        function getSkillDuration(skill) {
            const skillDurations = {
                // AI/ML skill durations
                'keras': "2-3 weeks",
                'tensorflow': "4-6 weeks",
                'pytorch': "4-6 weeks",
                'deep learning': "12-16 weeks",
                'machine learning': "8-12 weeks",
                'computer vision': "6-8 weeks",
                'nlp': "6-8 weeks",
                'neural networks': "4-6 weeks",
                
                // Web Development skill durations
                'javascript': "6-8 weeks",
                'react': "4-6 weeks",
                'node.js': "4-6 weeks",
                'python': "6-8 weeks",
                'django': "3-4 weeks",
                'postgresql': "2-3 weeks",
                'aws': "6-8 weeks",
                'docker': "2-3 weeks",
                
                // Cybersecurity skill durations
                'networking': "4-6 weeks",
                'penetration testing': "8-12 weeks",
                'malware analysis': "6-8 weeks",
                'cloud security': "6-8 weeks",
                'network security': "6-8 weeks",
                'cryptography': "4-6 weeks",
                'incident response': "3-4 weeks",
                'forensics': "4-6 weeks",
                
                // Data Science skill durations
                'statistics': "6-8 weeks",
                'data visualization': "2-3 weeks",
                'sql': "3-4 weeks",
                'r': "4-6 weeks",
                'pandas': "2-3 weeks",
                'numpy': "2-3 weeks",
                'scikit-learn': "3-4 weeks",
                'hadoop': "4-6 weeks",
                'spark': "4-6 weeks"
            };

            return skillDurations[skill.toLowerCase()] || "4-6 weeks";
        }

        function getSkillResources(skill) {
            return [
                {
                    icon: 'fas fa-book',
                    text: 'Learning Resources'
                },
                {
                    icon: 'fas fa-laptop-code',
                    text: 'Hands-on Practice'
                },
                {
                    icon: 'fas fa-project-diagram',
                    text: 'Real Projects'
                }
            ];
        }

        // Theme toggle functionality
        function toggleTheme() {
            const body = document.body;
            const toggleBtn = document.querySelector('.theme-toggle');
            const toggleIcon = toggleBtn.querySelector('i');
            const toggleText = toggleBtn.querySelector('.toggle-text');
            
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                toggleIcon.className = 'fas fa-sun';
                toggleText.textContent = 'Light Mode';
                localStorage.setItem('theme', 'dark');
            } else {
                body.setAttribute('data-theme', 'light');
                toggleIcon.className = 'fas fa-moon';
                toggleText.textContent = 'Dark Mode';
                localStorage.setItem('theme', 'light');
            }
        }

        // Set initial theme based on user's preference
        document.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            const body = document.body;
            const toggleBtn = document.querySelector('.theme-toggle');
            const toggleIcon = toggleBtn.querySelector('i');
            const toggleText = toggleBtn.querySelector('.toggle-text');
            
            body.setAttribute('data-theme', savedTheme);
            if (savedTheme === 'light') {
                toggleIcon.className = 'fas fa-moon';
                toggleText.textContent = 'Dark Mode';
            } else {
                toggleIcon.className = 'fas fa-sun';
                toggleText.textContent = 'Light Mode';
            }
        });
    </script>
</body>
</html>
'''

def init_db():
    """Initialize database with enhanced profiles and courses."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables with proper schema
    cursor.execute('''
    DROP TABLE IF EXISTS users
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        skills TEXT NOT NULL,
        specialization TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        company TEXT NOT NULL
    )
    ''')
    
    # Expanded profiles per specialization
    sample_professionals = [
        # AI/ML Professionals
        ("Sarah Chen", 
         "python,tensorflow,pytorch,deep learning,machine learning,computer vision,nlp",
         "AI", 7, "Google Brain"),
        ("Alex Kumar",
         "python,keras,scikit-learn,deep learning,data science,reinforcement learning",
         "AI", 5, "DeepMind"),
        ("Maria Santos",
         "python,machine learning,neural networks,computer vision,data mining,statistics",
         "AI", 9, "OpenAI"),
        ("John Smith",
         "python,natural language processing,bert,transformers,machine learning,data analysis",
         "AI", 6, "Microsoft AI"),
        ("Emily Zhang",
         "python,computer vision,object detection,gan,deep learning,pytorch",
         "AI", 8, "Tesla AI"),
        
        # Web Development Professionals
        ("Michael Rodriguez", 
         "javascript,react,node.js,python,django,postgresql,aws,docker",
         "Web Development", 8, "Netflix"),
        ("Jennifer Park",
         "javascript,vue.js,php,mysql,html5,css3,typescript,graphql",
         "Web Development", 6, "Shopify"),
        ("David Wilson",
         "javascript,angular,java,spring,mongodb,kubernetes,ci/cd,aws",
         "Web Development", 10, "Amazon"),
        ("Sophie Turner",
         "javascript,react native,mobile development,redux,firebase,aws",
         "Web Development", 5, "Uber"),
        ("Carlos Garcia",
         "python,django,fastapi,postgresql,redis,docker,kubernetes",
         "Web Development", 7, "Twitter"),
        
        # Cybersecurity Professionals
        ("Emma Thompson", 
         "python,networking,penetration testing,malware analysis,cloud security",
         "Cybersecurity", 6, "Microsoft Security"),
        ("James Chen",
         "network security,cryptography,incident response,forensics,security+",
         "Cybersecurity", 8, "FireEye"),
        ("Lisa Anderson",
         "ethical hacking,osint,vulnerability assessment,threat hunting,cissp",
         "Cybersecurity", 7, "CrowdStrike"),
        ("Marcus Johnson",
         "cloud security,aws security,azure security,devsecops,security architecture",
         "Cybersecurity", 9, "Palo Alto Networks"),
        ("Sophia Patel",
         "application security,web security,penetration testing,owasp,secure coding",
         "Cybersecurity", 5, "Google Security"),
        
        # Data Science Professionals
        ("Daniel Lee",
         "python,r,statistics,machine learning,data visualization,sql",
         "Data Science", 7, "Facebook"),
        ("Rachel Green",
         "python,pandas,numpy,scikit-learn,tableau,big data",
         "Data Science", 5, "LinkedIn"),
        ("Thomas Anderson",
         "python,spark,hadoop,data engineering,etl,aws",
         "Data Science", 8, "Airbnb"),
        ("Anna Martinez",
         "r,statistics,hypothesis testing,ab testing,experimental design",
         "Data Science", 6, "Netflix"),
        ("Kevin Zhang",
         "python,deep learning,nlp,computer vision,data science,keras",
         "Data Science", 9, "Apple")
    ]
    
    # Insert professionals
    cursor.executemany(
        "INSERT INTO users (name, skills, specialization, experience_years, company) VALUES (?, ?, ?, ?, ?)",
        sample_professionals
    )
    
    # Verify the insertion
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Inserted {cursor.fetchone()[0]} professionals")
    
    # Create and populate courses table
    cursor.execute('''
    DROP TABLE IF EXISTS courses
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        skill TEXT NOT NULL,
        specialization TEXT NOT NULL,
        platform TEXT NOT NULL,
        url TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        instructor TEXT NOT NULL,
        duration TEXT NOT NULL,
        description TEXT NOT NULL,
        rating REAL NOT NULL
    )
    ''')
    
    core_courses = [
        # AI/ML Courses
        ("Deep Learning Specialization", "deep learning", "AI", "Coursera", 
         "https://www.coursera.org/specializations/deep-learning", "Advanced", "Andrew Ng", "5 months", 
         "Comprehensive deep learning curriculum covering neural networks, CNN, RNN", 4.9),
        ("Machine Learning", "machine learning", "AI", "Stanford Online", 
         "https://www.coursera.org/learn/machine-learning", "Intermediate", "Andrew Ng", "3 months", 
         "Fundamental machine learning concepts and algorithms", 4.8),
        ("Computer Vision A-Z", "computer vision", "AI", "Udemy", 
         "https://www.udemy.com/course/computer-vision-a-z/", "Advanced", "Various Experts", "4 months", 
         "Complete computer vision toolkit with practical projects", 4.7),
        ("Natural Language Processing Specialization", "nlp", "AI", "Coursera", 
         "https://www.coursera.org/specializations/natural-language-processing", "Advanced", "DeepLearning.AI", "4 months", 
         "Advanced NLP techniques and transformers", 4.8),
        
        # Web Development Courses
        ("The Complete Web Development Bootcamp", "web development", "Web Development", "Udemy", 
         "https://www.udemy.com/course/the-complete-web-development-bootcamp/", "Beginner", "Dr. Angela Yu", "6 months", 
         "Complete web development from frontend to backend", 4.8),
        ("React - The Complete Guide", "react", "Web Development", "Udemy", 
         "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "Intermediate", "Maximilian Schwarzmüller", "2 months", 
         "Modern React with Hooks and Redux", 4.9),
        ("Complete Node.js Developer", "node.js", "Web Development", "Zero To Mastery", 
         "https://academy.zerotomastery.io/p/learn-node-js", "Intermediate", "Andrei Neagoie", "3 months", 
         "Backend development with Node.js and Express", 4.8),
        ("AWS Certified Developer Associate", "aws", "Web Development", "A Cloud Guru", 
         "https://acloudguru.com/course/aws-certified-developer-associate", "Advanced", "Ryan Kroonenburg", "4 months", 
         "Cloud development and deployment with AWS", 4.7),
        
        # Cybersecurity Courses
        ("Penetration Testing Professional", "penetration testing", "Cybersecurity", "INE Security", 
         "https://ine.com/learning/paths/penetration-testing-professional", "Advanced", "Security Experts", "3 months", 
         "Hands-on penetration testing and ethical hacking", 4.9),
        ("CompTIA Security+ Certification", "network security", "Cybersecurity", "CompTIA", 
         "https://www.comptia.org/certifications/security", "Intermediate", "Various Experts", "2 months", 
         "Fundamental security concepts and implementation", 4.8),
        ("AWS Security Specialty", "cloud security", "Cybersecurity", "A Cloud Guru", 
         "https://acloudguru.com/course/aws-certified-security-specialty", "Advanced", "Cloud Experts", "3 months", 
         "Security in AWS cloud environments", 4.7),
        ("SANS SEC504: Incident Handling", "incident response", "Cybersecurity", "SANS Institute", 
         "https://www.sans.org/cyber-security-courses/hacker-techniques-incident-handling/", "Advanced", "SANS Instructors", "2 months", 
         "Advanced incident response and threat hunting", 4.9),
        
        # Data Science Courses
        ("Data Scientist Professional with Python", "data science", "Data Science", "DataCamp", 
         "https://www.datacamp.com/tracks/data-scientist-professional-with-python", "Intermediate", "Various Experts", "4 months", 
         "Comprehensive data science curriculum with real-world projects", 4.8),
        ("Applied Data Science with Python Specialization", "python", "Data Science", "Coursera", 
         "https://www.coursera.org/specializations/data-science-python", "Intermediate", "University of Michigan", "3 months", 
         "Practical data science using Python libraries", 4.7),
        ("Big Data with Apache Spark", "spark", "Data Science", "edX", 
         "https://www.edx.org/professional-certificate/berkeleyxapache-spark", "Advanced", "Berkeley Professors", "3 months", 
         "Large-scale data processing with Spark", 4.8),
        ("Statistical Learning", "statistics", "Data Science", "Stanford Online", 
         "https://online.stanford.edu/courses/sohs-ystatslearning-statistical-learning", "Advanced", "Trevor Hastie & Rob Tibshirani", "4 months", 
         "Advanced statistical methods for data science", 4.9)
    ]
    
    cursor.executemany("""
        INSERT INTO courses (
            name, skill, specialization, platform, url, difficulty, 
            instructor, duration, description, rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, core_courses)
    
    conn.commit()
    conn.close()

@app.route("/suggest", methods=["POST"])
def suggest():
    """Provide skill suggestions and profile comparisons."""
    data = request.get_json()
    user_skills = set(skill.strip().lower() for skill in data.get("skills", "").split(","))
    specialization = data.get("specialization")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Debug: Print the specialization being queried
    print(f"Querying for specialization: {specialization}")
    
    # Get all profiles for the specialization
    cursor.execute("""
        SELECT name, skills, experience_years, company 
        FROM users 
        WHERE specialization = ?
    """, (specialization,))
    
    professionals = cursor.fetchall()
    
    # Debug: Print the number of professionals found
    print(f"Found {len(professionals)} professionals")
    
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
    
    # Debug: Print the number of profile comparisons
    print(f"Generated {len(profile_comparisons)} profile comparisons")
    
    # Get course recommendations
    missing_skills = all_required_skills - user_skills
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
        "rating": course[8],
        "is_paid": False,
        "price": 49  # Simple dollar price if paid
    } for course in courses]

    # Make some courses paid
    for i, course in enumerate(course_recommendations):
        if i % 2 == 0:  # Make every other course paid
            course["is_paid"] = True

    conn.close()

    return jsonify({
        "missing_skills": list(missing_skills),
        "profile_comparisons": profile_comparisons,
        "course_recommendations": course_recommendations
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)