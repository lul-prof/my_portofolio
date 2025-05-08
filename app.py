from flask import Flask, render_template, send_file, jsonify, request, flash
import requests
from concurrent.futures import ThreadPoolExecutor
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email configuration
app.config['SECRET_KEY'] = 'cant-hack-me' 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'israelmutua539@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pzws tkzr scdc vwvd'  

mail = Mail(app)

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(
            subject=f'Portfolio Contact from {name}',
            sender=email,
            recipients=['israelmutua539@gmail.com'],  # Replace with your email
            body=f'''
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            '''
        )
        
        
        mail.send(msg)
        
        return jsonify({'status': 'success', 'message': 'Your message has been sent successfully!'})
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to send message. Please try again later.'}), 500

def get_fallback_projects():
    return [
        {
            'name': 'Diamond Coffee Company',
            'description': 'A web application for managing a coffee shop business, including order management and inventory tracking.',
            'url': 'https://github.com/lul-prof/diamond_coffee_company',
            'language': 'Python'
        },
        {
            'name': 'Joy\'s Law Firm',
            'description': 'A professional website for a law firm with case management and client portal features.',
            'url': 'https://github.com/lul-prof/joys_law_firm',
            'language': 'PHP'
        },
        {
            'name': 'Ndanus Bakery',
            'description': 'An e-commerce platform for a bakery business with order management and delivery tracking.',
            'url': 'https://github.com/lul-prof/ndanus_bakery',
            'language': 'Python'
        },
        {
            'name': 'BFL Studios',
            'description': 'A multimedia studio management system for handling bookings and project tracking.',
            'url': 'https://github.com/lul-prof/bfl_studios',
            'language': 'JavaScript'
        },
        {
            'name': 'Medical Recommendation System',
            'description': 'An AI-powered system for medical diagnosis and treatment recommendations.',
            'url': 'https://github.com/lul-prof/medical_recommendation_system',
            'language': 'Python'
        },
        {
            'name': 'BFL Music',
            'description': 'A music streaming platform with playlist management and artist profiles.',
            'url': 'https://github.com/lul-prof/bfl_music',
            'language': 'JavaScript'
        },
        {
            'name': 'Police DB',
            'description': 'A database management system for law enforcement records and case tracking.',
            'url': 'https://github.com/lul-prof/police_db',
            'language': 'Python'
        },
        {
            'name': 'BFL Apparel',
            'description': 'An e-commerce platform for clothing and fashion accessories.',
            'url': 'https://github.com/lul-prof/bfl-apparel',
            'language': 'JavaScript'
        },
        {
            'name': 'Job Application Portal',
            'description': 'A web application for managing job postings and applications with user authentication.',
            'url': 'https://github.com/lul-prof/job-application-portal-flask',
            'language': 'Python'
        }
    ]

def fetch_repo(repo):
    try:
        url = f'https://api.github.com/repos/lul-prof/{repo}'
        response = requests.get(url)
        if response.status_code == 200:
            repo_data = response.json()
            return {
                'name': repo_data['name'],
                'description': repo_data['description'] or 'No description available',
                'url': repo_data['html_url'],
                'language': repo_data['language'] or 'Not specified'
            }
        else:
            print(f"Error fetching {repo}: Status {response.status_code}")
    except Exception as e:
        print(f"Error fetching repo {repo}: {str(e)}")
    return None

def fetch_github_repos():
    repos = [
        'diamond_coffee_company',
        'joys_law_firm',
        'ndanus_bakery',
        'bfl_studios',
        'medical_recommendation_system',
        'bfl_music',
        'police_db',
        'bfl-apparel',
        'job-application-portal-flask'
    ]
    
    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_repo, repos))
    
    # Filter out None results and return valid repos
    return [repo for repo in results if repo is not None]

@app.route('/')
def home():
    try:
        projects = fetch_github_repos()
        return render_template('index.html', projects=projects)
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        # Return empty projects list if there's an error
        return render_template('index.html', projects=get_fallback_projects())

@app.route('/download-resume')
def download_resume():
    try:
        return send_file('static/resume/Israel_Mutua_Resume.docx')
    except Exception as e:
        print(f"Error downloading resume: {str(e)}")
        return "Resume not found", 404

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', projects=get_fallback_projects()), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', projects=get_fallback_projects()), 500

if __name__ == '__main__':
    app.run(debug=True)