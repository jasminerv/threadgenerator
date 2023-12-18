from flask import Flask, render_template, request, session, send_from_directory, jsonify
import os
import json
from classes import Persona, ThreadParams  # Import your classes
from generate_thread import generate_thread, save_messages_to_csv
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
app = Flask(__name__)

# Set the Flask app's secret key from the environment variable
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/download_thread')
def download_thread():
    filename = session.get('generated_filename')
    if filename:
        return send_from_directory(app.root_path, filename, as_attachment=True)
    else:
        return "No thread generated", 404


@app.route('/generate_thread', methods=['GET', 'POST'])
def generate_thread_page():
    if request.method == 'POST':
        selected_persona_name = request.form['selected_persona']
        selected_thread_params_name = request.form['selected_thread_params']

        personas = load_personas_from_file()
        thread_params = load_thread_params_from_file()

        selected_persona_dict = next(
            (p for p in personas if f"{p['name_first']} {p['name_last']}" == selected_persona_name), None)
        selected_thread_params_dict = next(
            (tp for tp in thread_params if tp['name_thread'] == selected_thread_params_name), None)

        if not selected_persona_dict or not selected_thread_params_dict:
            error_message = "Selected persona or thread parameters not found. Please try again."
            return render_template('error_page.html', error_message=error_message)

        selected_persona = Persona(**selected_persona_dict)
        selected_thread_params = ThreadParams(**selected_thread_params_dict)

        messages = generate_thread(selected_persona, selected_thread_params)
        filename = save_messages_to_csv(messages, selected_persona, selected_thread_params)
        session['generated_filename'] = filename  # Store filename in session

        return render_template('thread_generated.html')  # Render a new template

    personas = load_personas_from_file()
    thread_params = load_thread_params_from_file()
    return render_template('generate_thread.html', personas=personas, thread_params=thread_params)


def load_personas_from_file():
    try:
        with open('personas.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def load_thread_params_from_file():
    try:
        with open('thread_params.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_persona_to_file(persona):
    try:
        with open('personas.json', 'r') as file:
            personas = json.load(file)
    except FileNotFoundError:
        personas = []

    personas.append(persona.__dict__)

    with open('personas.json', 'w') as file:
        json.dump(personas, file, indent=4)


def save_thread_params_to_file(thread_param):
    try:
        with open('thread_params.json', 'r') as file:
            thread_params = json.load(file)
    except FileNotFoundError:
        thread_params = []

    thread_params.append(thread_param.__dict__)

    with open('thread_params.json', 'w') as file:
        json.dump(thread_params, file, indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_persona', methods=['GET', 'POST'])
def create_persona():
    if request.method == 'POST':
        persona = Persona(
            request.form['name_first'],
            request.form['name_last'],
            int(request.form['age']),
            request.form['place_residence'],
            request.form['place_birth'],
            request.form['hobbies'],
            request.form['personality_type'],
            request.form['career'],
            request.form['career_state'],
            request.form.get('partnered') == 'on',
            request.form['partner_name']
        )
        save_persona_to_file(persona)
        return render_template('submission_success.html', message="Persona created successfully.")
    return render_template('create_persona.html')


@app.route('/create_thread_params', methods=['GET', 'POST'])
def create_thread_params():
    if request.method == 'POST':
        thread_params = ThreadParams(
            request.form['name_thread_params'],
            request.form['name_notebook'],
            int(request.form['max_notes_per_day']),
            request.form['thread_description'],
            int(request.form['thread_length_months']),
            request.form['thread_start_date']
        )
        save_thread_params_to_file(thread_params)
        return render_template('submission_success.html', message="Thread Parameters created successfully.")
    return render_template('create_thread_params.html')


@app.route('/view_personas')
def view_personas():
    personas = load_personas_from_file()
    return render_template('view_personas.html', personas=personas)


@app.route('/view_thread_params')
def view_thread_params():
    thread_params = load_thread_params_from_file()
    return render_template('view_thread_params.html', thread_params=thread_params)


if __name__ == '__main__':
    app.run(debug=True)
