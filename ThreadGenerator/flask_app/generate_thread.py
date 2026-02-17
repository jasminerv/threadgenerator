from classes import Persona, ThreadParams
import random
import csv
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def generate_thread(persona, thread_params):
    messages = []
    history = []  # This will store the context for subsequent messages
    start_date = datetime.strptime(thread_params.thread_start_date, '%Y-%m-%d')
    end_date = start_date + timedelta(weeks=4 * thread_params.thread_length_months)

    current_date = start_date
    while current_date <= end_date:
        num_messages_today = random.randint(1, thread_params.max_notes_per_day)
        times_today = sorted(
            [random.randint(0, 86399) for _ in range(num_messages_today)])  # Generate random seconds in a day

        for time_seconds in times_today:
            time_of_day = timedelta(seconds=time_seconds)
            message_datetime = current_date + time_of_day
            formatted_datetime = message_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if not history:  # If no history, generate the first message
                message = generate_message(persona, thread_params, formatted_datetime)
                history.append({"role": "assistant", "content": message["message"]})
            else:
                message_content = generate_new_entry(history, client, persona, thread_params)
                message = {
                    "message": message_content,
                    "date_time": formatted_datetime,
                    "name_thread": thread_params.name_thread,
                    "name_notebook": thread_params.name_notebook
                }
                history.append({"role": "assistant", "content": message["message"]})

            messages.append(message)

        current_date += timedelta(days=1)  # Move to the next day

    return messages


def clean_message(text):
    # Splits the text into sentences
    sentences = text.split(". ")
    # Removes the last sentence if it does not end with a period
    if sentences and not sentences[-1].endswith('.'):
        return ". ".join(sentences[:-1]) + "."
    return text


def generate_message(persona, thread_params, date):
    prompt = construct_prompt(persona, thread_params)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"Act as the following person: First Name: {persona.name_first} "
                           f"Last Name: {persona.name_last}\nAge: {persona.age}\nPlace of Residence: "
                           f"{persona.place_residence} Place of Birth: {persona.place_birth}\nHobbies: "
                           f"{persona.hobbies}\nPersonality type: {persona.personality_type}\nCareer: "
                           f"{persona.career}\nCareer State: {persona.career_state}\nPartnered: {persona.partnered}\n"
                           f"Partner Name: {persona.partner_name}”\n"
                           f"You are keeping an ongoing thread of messages with yourself. "
                           f"The name of the thread is {thread_params.name_thread}"
                           f"and exists within a digital notebook called {thread_params.name_notebook}. "
            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        temperature=1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
    )

    generated_content = response.choices[0].message.content
    cleaned_content = clean_message(generated_content)

    return {
        "message": cleaned_content,
        "date_time": date,
        "name_thread": thread_params.name_thread,
        "name_notebook": thread_params.name_notebook
    }


def generate_new_entry(history, client, persona, thread_params):
    context = " ".join([msg["content"] for msg in history[-10:]])
    new_prompt = f"{context} Write the next short message to yourself on the topic of {thread_params.name_thread}. " \
                 f"Imagine this is a note to self, " \
                 f"or as if you were just keeping track of your thoughts. " \
                 f"Write in the FIRST person. Do not write in the second person " \
                 f"or address yourself by name. Tone: " \
                 f"Casual. DO NOT INCLUDE formal structure, greetings, dates, subject lines,titles, etc."

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"Act as the following person: First Name: {persona.name_first} "
                           f"Last Name: {persona.name_last}"
                           f"Age: {persona.age}\nPlace of Residence: {persona.place_residence} "
                           f"Place of Birth: {persona.place_birth}"
                           f"Hobbies: {persona.hobbies}"
                           f"Personality type: {persona.personality_type}"
                           f"Career: {persona.career}"
                           f"Career State: {persona.career_state}"
                           f"Partnered: {persona.partnered}"
                           f"Partner Name: {persona.partner_name}”"
                           f"\nYou are keeping an ongoing thread of messages with yourself. "
                           f"The name of the thread is {thread_params.name_thread}"
                           f"and exists within a digital notebook called {thread_params.name_notebook}"
                           f"Write in the FIRST person.DO NOT INCLUDE formal structure, "
                           f"greetings, dates, subject lines,titles, etc. "
            },
            {
                "role": "user",
                "content": new_prompt
            }
        ],
        temperature=.3,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1,
    )

    new_message = response.choices[0].message.content
    cleaned_new_message = clean_message(new_message)

    return cleaned_new_message


def construct_prompt(persona, thread_params):
    prompt_elements = [
    ]
    prompt = " ".join(
        prompt_elements) + f"You are {persona.name_first}  keeping personal notes. Write short message to yourself" \
                           f" on " \
                           f"the following topic {thread_params.thread_description}. Imagine this is a note to self, " \
                           f"or as if you were just keeping track of your thoughts. Write in the first person." \
                           f"Do not write in the second person " \
                           f"or address yourself by name. Limit your message to 2-4 sentences. Vary sentence length. Tone: " \
                           f"Casual. DO NOT INCLUDE formal structure, greetings, dates, subject lines,titles, etc. "
    return prompt


def save_messages_to_csv(messages, persona, thread_params):
    # Create a filename based on persona and thread_params
    filename = f"{persona.name_first}_{persona.name_last}_{thread_params.name_thread}.csv"
    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Message", "Date/Time", "Thread Name", "Notebook Name"])  # Header row
        for msg in messages:
            writer.writerow([msg["message"], msg["date_time"], msg["name_thread"], msg["name_notebook"]])
    return filename
