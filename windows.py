import os
import subprocess
import sys

def run_command(command, shell=False):
    """Utility to run a command and print its output."""
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Decode and print stdout and stderr
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode(), file=sys.stderr)
    
    if process.returncode != 0:
        print(f"Error running command: {stderr.decode()}")
        sys.exit(1)
    return stdout.decode()

def upgrade_pip():
    """Upgrade pip inside the virtual environment."""
    try:
        run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except Exception as e:
        print(f"Error upgrading pip: {e}")
        sys.exit(1)

def start_admin_terminal(command):
    """Open a new terminal with administrative privileges to run a command."""
    subprocess.run([
        "powershell",
        "-Command",
        "Start-Process",
        "powershell.exe",
        "-ArgumentList", f"'-NoExit', '-Command', '{command}'",
        "-Verb", "RunAs"
    ], check=True)

# Define paths
home_dir = os.path.expanduser("~")
scraper_app_dir = os.path.join(home_dir, "Downloads", "Scraper_App")
scraper_app_main_dir = os.path.join(home_dir, "Downloads", "Scraper_App-main")

# Ensure Scraper_App directory exists
if not os.path.exists(scraper_app_dir):
    if os.path.exists(scraper_app_main_dir):
        os.rename(scraper_app_main_dir, scraper_app_dir)
        print("Renamed Scraper_App-main to Scraper_App")
    else:
        print("Error: Scraper_App folder does not exist!")
        sys.exit(1)

# Change to the Scraper_App directory
os.chdir(scraper_app_dir)

# Create virtual environment
print("Creating virtual environment...")
run_command(["python", "-m", "venv", "env"])

# Activate the virtual environment
activate_script = os.path.join(scraper_app_dir, "env", "Scripts", "activate")
run_command([activate_script], shell=True)

# Upgrade pip
print("Upgrading pip...")
upgrade_pip()

# Install dependencies
print("Installing dependencies from req.txt...")
run_command(["pip", "install", "-r", "req.txt"])

# Start the backend server in a new terminal with administrative privileges
print("Starting the backend server in a new terminal...")
subprocess.run([
    "powershell",
    "-Command",
    "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
], check=True)

backend_command = "cd backend; .\\env\\Scripts\\Activate.ps1; python first.py"
start_admin_terminal(backend_command)

# Start the frontend server in a new terminal with administrative privileges
print("Starting the frontend server in a new terminal...")
frontend_dir = os.path.join(scraper_app_dir, "frontend")
frontend_command = f'cd ~/Downloads/Scraper_App/frontend/; npm i --legacy-peer-deps; npm start'
start_admin_terminal(frontend_command)

print("Frontend and backend servers are now running.")