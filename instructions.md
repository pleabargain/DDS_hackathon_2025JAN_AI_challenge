instructions
you are a python developer
you are tasked with creating a python script that will analyze the day1form.md and create a new file called day1form.json
the purpose of the script is to help the user create a details plan for creating a project
create a pyhton script that will analyze the day1form.md and create a new file called day1form.json
analyze the day1form.md and create a new file called day1form.json
populate the json file with the data from the day1form.md
each field is a key in the json file
each key is a string
each string will be formed into a question and answer pair
example: Project Title:
becomes: "Project Title": "What is the title of your project?"
user enters the answer in the format of a string
the answer will be stored in the json file as a string
the question will be stored in the json file as a string
the question and answer pair will be stored in the json file as a key and value pair
the json file will be stored in the same directory as the day1form.md file
the json file will be named day1form.json
for each answer, the answer will be passed to ollama for processing
the ollama engine will return an idea for the answer
user will be asked to review the idea and if they are satisfied with the idea, they will enter y or n
if the user is not satisfied with the idea, they will be asked to enter a new answer
the process will repeat until the user is satisfied with the idea
the json file will be stored in the same directory as the day1form.md file
the json file will be named day1form.json

