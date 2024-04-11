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

print("Installing requirements...")
subprocess.run(["pip", "install", "-r", "requirements.txt"])

print("Running the Django server...")
subprocess.run(["python", "manage.py", "runserver"])
