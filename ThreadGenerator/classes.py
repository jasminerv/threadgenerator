class Persona:
    def __init__(self, name_first: str, name_last: str, age: int, place_residence: str, place_birth: str, hobbies: str,
                 personality_type: str, career: str, career_state: str, partnered: bool, partner_name: str = None):
        self.name_first = name_first
        self.name_last = name_last
        self.age = age
        self.place_residence = place_residence
        self.place_birth = place_birth
        self.hobbies = hobbies
        self.personality_type = personality_type
        self.career = career
        self.career_state = career_state
        self.partnered = partnered
        self.partner_name = partner_name if partnered else None

    def __str__(self):
        return f"Persona(name_first={self.name_first}, name_last={self.name_last}, age={self.age}, place_residence={self.place_residence}, place_birth={self.place_birth}, hobbies={self.hobbies}, personality_type={self.personality_type}, career={self.career}, career_state={self.career_state}, partnered={self.partnered}, partner_name={self.partner_name})"


class ThreadParams:
    def __init__(self, name_thread: str, name_notebook: str, max_notes_per_day: int, thread_description: str, thread_length_months: int, thread_start_date: str):
        self.name_thread = name_thread
        self.name_notebook = name_notebook
        self.max_notes_per_day = max_notes_per_day
        self.thread_description = thread_description
        self.thread_length_months = thread_length_months
        self.thread_start_date = thread_start_date

    def __str__(self):
        return f"Thread(name_thread={self.name_thread}, name_notebook={self.name_notebook}, max_notes_per_day={self.max_notes_per_day}, story_arc={self.story_arc}, length_months_thread={self.thread_length_months}) "

