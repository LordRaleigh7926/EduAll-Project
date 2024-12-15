from flask import render_template, request, redirect, url_for, session, flash, jsonify
from firebase_admin import firestore
import uuid
from gemini_chat import get_chat_response
from gemini_call import get_response_initial
import hashlib
import markdown

def consistent_hash(email):
    return hashlib.sha256(email.encode()).hexdigest()


def configure_routes(app, auth, firebase_admin_auth, db):



    @app.route('/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                # Log the user in
                user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = user['idToken']
                session['email'] = str(consistent_hash(email))
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
            except:
                flash('Login failed. Please check your credentials.')
                return redirect(url_for('signup', login="Failed Login"))
        login_status = request.args.get('login')
        return render_template('signup.html', login=login_status)







    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                user = auth.create_user_with_email_and_password(email, password)
                flash('Account created successfully!')
                return redirect(url_for('signup', login="true"))
            except:
                flash('Signup failed. Please try again.')
                return redirect(url_for('signup',login="signup failed"))

        login_status = request.args.get('login')
        return render_template('signup.html', login=login_status)





    @app.route("/")
    def index():
        try:
            logged_in = session['logged_in']
            return render_template("index.html", logged_in=logged_in)
        except:
            return render_template("index.html", logged_in=False)
            


    @app.route("/about")
    def about():
        return render_template("about.html")
    




    
# Route to handle Google Sign-In/Sign-Up
    @app.route('/google-login', methods=['POST'])
    def google_login():
        id_token = request.json.get('idToken')
        try:
            # Verify the ID token using Firebase Admin SDK
            decoded_token = firebase_admin_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')

            # Store user session
            session['user'] = uid
            session['email'] = str(consistent_hash(email))
            session['logged_in'] = True

            return jsonify({"success": True}), 200
        
        except Exception as e:
            print(f"Error verifying ID token: {e}")
            return jsonify({"success": False, "error": str(e)}), 400







    # Dashboard Route
    @app.route('/dashboard')
    def dashboard():
        if 'user' in session:
            # Get the user's email (assuming email is stored in session)
            user_id = session['email']
            
            # Reference to the user's topics subcollection
            topics_ref = db.collection('users').document(user_id).collection('topics').order_by('timestamp', direction=firestore.Query.DESCENDING)
            
            # Retrieve all the documents in the 'topics' subcollection
            topics = topics_ref.stream()

            # Extract data from each topic document
            topic_list = []
            for topic in topics:
                topic_data = topic.to_dict()
                topic_list.append({

                    'topic_id': topic.id,  # Include the topic ID for the link
                    'topic_title': topic_data.get('topic_title', 'No Title'),
                    'roadmap': topic_data.get('roadmap', 'No Roadmap'),
                    'books': topic_data.get('books', 'No Books'),
                    'links': topic_data.get('links', 'No Links'),
                    'quote1': topic_data.get('quote1', 'No Quote1'),
                    'quote2': topic_data.get('quote2', 'No Quote2'),
                    'timestamp': topic_data.get('timestamp')  # Optional: Format the timestamp as needed
                })
    
            return render_template("dashboard.html", topics=topic_list, user_id=user_id)
        else:
            return redirect(url_for('signup'))




    # Logout Route
    @app.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('logged_in', False)
        flash('You have been logged out.')
        return redirect(url_for('index'))
    




    # Route to handle the form submission
    @app.route('/submit', methods=['POST'])
    def submit():
        topic = request.form.get('inputText')
        sub_topics= request.form.get('inputSubTopics')
        time_constraint= request.form.get('inputTime')
        user_id = session['email']

        # Generate a unique topic ID for each topic (you can modify this as needed)
        topic_id = str(uuid.uuid4())

        # Create the user's subcollection (if not already present) and add the topic
        user_ref = db.collection('users').document(user_id)
        topics_ref = user_ref.collection('topics').document(topic_id)

        print(time_constraint)

        roadmap, books, links, quote1, quote2 = get_response_initial(topic, time_constraint, sub_topics)

        # Add the topic to the user's subcollection
        topics_ref.set({
            'topic_title': topic.capitalize(),
            'roadmap': roadmap,
            'links': markdown.markdown(links),
            'books': markdown.markdown(books),
            'quote1': markdown.markdown(quote1),
            'quote2': markdown.markdown(quote2),
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return redirect(url_for("dashboard"))
        
    
    @app.route('/topic/<user_id>/<topic_id>', methods=['GET'])
    def topic_detail(topic_id, user_id):

        if request.method == 'GET':
            session['topic_id'] = topic_id

        if 'chat_history' not in session:
            session[f'chat_history_{topic_id}'] = [] 
        # Get the user's email (assuming email is stored in session)
        user_id = session['email']
        
        # Reference to the specific topic document for that user
        topic_ref = db.collection('users').document(user_id).collection('topics').document(topic_id)
        
        # Retrieve the topic document
        topic = topic_ref.get()

        # For GET requests, render the editor page with existing document content
        try:
            doc = topic_ref.get()
            content = doc.to_dict()['content'] if doc.exists else ""
        except Exception as e:
            content = ""

        try:
            doc = topic_ref.get()
            progress = doc.to_dict()['progress'] if doc.exists else ""
        except Exception as e:
            progress = ""

        
        if topic.exists:
            topic_data = topic.to_dict()
            return render_template('topic_details.html', content=content, topic=topic_data, topic_id=topic_id, user_id=user_id, progress=progress)
        else:
            return 'Topic not found', 404

        

    @app.route('/topic/del', methods=['POST'])
    def del_topic():
        user_id = request.form.get('user_id')
        topic_id = request.form.get('topic_id')

        if not user_id or not topic_id:
            return "Missing user_id or topic_id", 400

        # Constructing Firestore reference
        topic_ref = db.collection('users').document(user_id).collection('topics').document(topic_id)

        try:
            topic_ref.delete()
            print("Document successfully deleted!")
        except Exception as e:
            print(f"An error occurred: {e}")

        return redirect(url_for("dashboard"))
    

    # Handle chat messages
    @app.route('/get_response', methods=['POST'])
    def get_response():
        topic_id=session.get('topic_id')
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please type a message.'})
        
        # Retrieve chat history from the session
        chat_history = session.get(f'chat_history_{topic_id}', [])
        
        # Format the input for Gemini
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        combined_input = f"{context}\nuser: {user_message}"
        
        # Get response from Gemini
        try:
            gemini_response = get_chat_response(combined_input)
            gemini_response = markdown.markdown(gemini_response)
        except Exception as e:
            return jsonify({'response': f"Error: {str(e)}"})

        # Update chat history
        chat_history.append({'role': 'user', 'content': user_message})
        chat_history.append({'role': 'assistant', 'content': gemini_response})
        session['chat_history'] = chat_history
        
        return jsonify({'response': gemini_response})
    
    

    @app.route('/topic/<user_id>/<topic_id>/editRoadmap', methods=['POST'])
    def topic_detail_save_roadmap(user_id, topic_id):

        new_field_name = "roadmap"
        content = request.json.get('content')  # Markdown content
        topic_id = session['topic_id']
        user_id = session['email']
        topic_ref = db.collection('users').document(user_id).collection('topics').document(topic_id)


        try:
            topic_ref.update({new_field_name: content})
            return jsonify({'status': 'success', 'message': f'Roadmap saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'status': 'error', 'message': str(e)}), 500


    @app.route('/topic/<user_id>/<topic_id>/editProg', methods=['POST'])
    def topic_detail_save_progress(user_id, topic_id):
        
        new_field_name = "progress"
        content = request.json.get('content')  # Progress Content
        
        # Reference to the specific topic document for that user
        topic_ref = db.collection('users').document(user_id).collection('topics').document(topic_id)
        
        try:
            topic_ref.update({new_field_name: content})
            return jsonify({'status': 'success', 'message': f'Content saved under field "{new_field_name}"'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        

        

    @app.route('/topic/<user_id>/<topic_id>/editNotes', methods=['POST'])
    def topic_detail_save_notes(user_id, topic_id):
        
        new_field_name = "content"
        content = request.json.get('content')  # Progress Content
        
        # Reference to the specific topic document for that user
        topic_ref = db.collection('users').document(user_id).collection('topics').document(topic_id)

        try:
            topic_ref.update({new_field_name: content})
            return jsonify({'status': 'success', 'message': f'Editor content saved under field "{new_field_name}"'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        