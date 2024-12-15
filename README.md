### EduAll Project Structure

## EduAll - Learning Path and Resource Management System

### Overview

EduAll is a web-based platform designed to help users create, manage, and track their learning journeys. It allows users to signup with Google authentication or through normal email registration. Users can enter topics they want to learn, and a personalized roadmap with recommended resources like links, books, and research materials is generated using Google Gemini. These roadmaps, progress notes, and research points are stored in Firebase for easy access and management.

### Features

- **Signup**: Allows users to sign up using Google Auth or normal email.
- **Learning Paths**: Create unlimited learning paths for various topics.
- **Roadmap Generation**: Generates a roadmap for a given topic with *resources such as links, books, and recommended materials*.
- **Progress Notes**: Users can use a Markdown editor to document their progress for each learning path.
- **AI Research Assistance**: A small chat window integrated with an AI for researching specific topics and storing research points.
- **Firebase Integration**: Stores all data related to progress and research points in the Firebase database.

### Problem Addressed

EduAll addresses the lack of a clear and structured path for individuals looking to learn new topics. By providing a systematic roadmap generation and progress tracking system, users are guided effectively from entry-level learning to advanced research, ensuring a cohesive and engaging learning experience.

### Usage

- **Signup/Login**: Choose to sign up using Google or normal email and password.
- **Create Learning Paths**: Enter a topic, and a roadmap is generated with resources.
- **Progress Tracking**: Use the Markdown editor to document progress for each topic.
- **AI Research**: Utilize the AI chat window to research and store points related to the topic.
- **Database**: All data including roadmaps, progress, and research points are stored in Firebase.

### Project Structure

- **app.py**: Main application file for the Flask server.
- **config.json**: Configuration settings.
- **gemini_call.py**: Handles API calls to Google Gemini for roadmap generation.
- **gemini_chat.py**: Manages AI-based topic research and storage.
- **__pycache__**: Contains bytecode files for Python modules.
- **requirements.txt**: Contains the necessary Python dependencies.
- **routes.py**: Defines routes and handles route-specific logic.
- **server/src**: Source code for backend operations.
- **static**: Contains static assets like CSS, JS, and images.
- **templates**: HTML templates for rendering web pages.
- **todo.md**: To-do list for future improvements.
- **work.txt**: Additional workspace documentation.

### Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, Python
- **Database**: Firebase
- **Authentication**: Google OAuth, Email
- **AI**: Google Gemini

### Contribution

Contributions are welcome! Please fork this repository, make changes, and submit a pull request.

### License

This project is licensed under the MIT License.
