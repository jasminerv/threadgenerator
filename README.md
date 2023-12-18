# threadgenerator
Generate a thread of synthetic messages from the perspective of a specific persona writing every day for a selected number of months.

This program outputs a CSV of messages that are a cohesive thread on a specific topic in chronological order.

When configuring a new set of thread parameters, you will be prompted to select number of max notes a day, this number will be used to 
determine how many notes will be generated on a certain day for the persona (between one and the max number chosen)

Each row contains its message, a date/time, thread name, and notebook name. 
## Requirements
```
flask
openai
python-dotenv

```
## Set Up 
1. Clone this repo
2. If you do not have an IDE, download PyCharm: https://www.jetbrains.com/pycharm/download/?section=mac
3. Set up a virtual environment 
4. Download requirements 
5. Add a .env file to the root file (ThreadGenerator) and add your OpenAI API key and a secret key for flask

_Example .env file:_

```
OPENAI_API_KEY = YOUR_OPENAI_KEY_HERE
SECRET_KEY = LITERALLY_ANYTHING_HERE_BUT_TRY_AND_MAKE_IT_SECRET
```

## Using the Thread Generator
1. Navigate to app.py in the flask_app directory
2. Run app.py
3. Create a new persona and thread parameters, or take a look at the existing ones
4. To generate a new thread, go to "Generate New Thread"
