import os
import subprocess

print("Cloning the repository...")
subprocess.run(
    ["git", "clone", "https://github.com/chandansgowda/paperswift-api.git"])

print("Changing directory to the cloned repository...")
os.chdir("paperswift-api")

print("Installing virtualenv...")
subprocess.run(["pip", "install", "virtualenv"])

print("Creating a virtual environment...")
subprocess.run(["virtualenv", "venv"])

print("Activating the virtual environment...")
if os.name == 'posix':
    activate_script = "source venv/bin/activate"
elif os.name == 'nt':
    activate_script = "venv\\Scripts\\activate.bat"
else:
    print("Unsupported operating system")
    exit()

subprocess.run(activate_script, shell=True)

api_key_value = input(
    "Enter the value for BREVO_API_KEY environment variable: ")
os.environ['BREVO_API_KEY'] = api_key_value

print("Installing requirements...")
subprocess.run(["pip", "install", "-r", "requirements.txt"])

print("Making migrations...")
subprocess.run(["python", "manage.py", "makemigrations"])

print("Applying migrations...")
subprocess.run(["python", "manage.py", "migrate"])

print("Successful!\nTo start the server -  python manage.py runserver")
