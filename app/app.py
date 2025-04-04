from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from email.message import EmailMessage
import smtplib
import config
from models import db, Submission  # Import db and Submission model

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # Allow requests from React frontend

db.init_app(app)  # Initialize the database
migrate = Migrate(app, db)  # Initialize Flask-Migrate

@app.route('/')
def hello_world():
    return "Hello, Flask!"

# Route to handle the email submission and save to DB
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Get data from the request
        data = request.get_json()
        name = data['name']
        email = data['email']
        message_content = data['message']

        # Create a new submission and store it in the database
        submission = Submission(name=name, email=email, message=message_content)
        db.session.add(submission)
        db.session.commit()

        # Create the email message
        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage: {message_content}")
        msg['Subject'] = 'Contact Form Message'
        msg['From'] = config.EMAIL_ADDRESS
        msg['To'] = config.EMAIL_ADDRESS  # Send email to yourself

        # Send email using Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'success': True, 'message': 'Email sent and submission saved successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# Route to get all submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = Submission.query.all()  # Get all submissions
        submissions_data = [submission.to_dict() for submission in submissions]  # Convert to dictionary
        return jsonify({'success': True, 'submissions': submissions_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/submissions/<int:id>', methods=['GET'])
def get_submission(id):
    try:
        submission = Submission.query.get_or_404(id)  # Get submission by ID or return 404
        return jsonify({'success': True, 'submission': submission.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to delete a specific submission by ID
@app.route('/submissions/<int:id>', methods=['DELETE'])
def delete_submission(id):
    try:
        submission = Submission.query.get_or_404(id)  # Get submission by ID or return 404
        db.session.delete(submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Submission deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to update an entire submission (PUT)
@app.route('/submissions/<int:id>', methods=['PUT'])
def update_submission(id):
    try:
        # Get the submission by ID
        submission = Submission.query.get_or_404(id)

        # Get new data from the request
        data = request.get_json()
        submission.name = data.get('name', submission.name)  # Update name if provided
        submission.email = data.get('email', submission.email)  # Update email if provided
        submission.message = data.get('message', submission.message)  # Update message if provided

        # Commit the changes to the database
        db.session.commit()

        # Send email with updated submission details
        send_email_to_self(submission)

        return jsonify({'success': True, 'message': 'Submission updated successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to update a specific field of a submission (PATCH)
@app.route('/submissions/<int:id>', methods=['PATCH'])
def partial_update_submission(id):
    try:
        # Get the submission by ID
        submission = Submission.query.get_or_404(id)

        # Get partial data from the request
        data = request.get_json()

        # Update only the fields provided in the request
        if 'name' in data:
            submission.name = data['name']
        if 'email' in data:
            submission.email = data['email']
        if 'message' in data:
            submission.message = data['message']

        # Commit the changes to the database
        db.session.commit()

        # Send email with updated submission details
        send_email_to_self(submission)

        return jsonify({'success': True, 'message': 'Submission updated successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def send_email_to_self(submission):
    """Function to send email with the updated submission details."""
    msg = EmailMessage()
    msg.set_content(f"Name: {submission.name}\nEmail: {submission.email}\n\nMessage: {submission.message}")
    msg['Subject'] = 'Updated Contact Form Message'
    msg['From'] = config.EMAIL_ADDRESS
    msg['To'] = config.EMAIL_ADDRESS  # Send email to yourself

    # Send email using Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)
