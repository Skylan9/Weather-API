import os
import subprocess

def check_wsl_installed():
    """Check if WSL is installed on the system."""
    try:
        result = subprocess.run(["wsl", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def start_redis_server():
    """Start the Redis server using WSL and Ubuntu."""
    try:
        # Command to start Redis server inside Ubuntu
        command = "wsl -d Ubuntu redis-server"

        # Start Redis server
        print("Starting Redis server...")
        process = subprocess.Popen(command, shell=True)
        print("Redis server started successfully! Press Ctrl+C to stop.")

        # Wait for the process to complete (keep it running)
        process.wait()

    except KeyboardInterrupt:
        print("\nStopping Redis server...")
        process.terminate()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if not check_wsl_installed():
        print("WSL is not installed on this system. Please install WSL and Ubuntu before running this script.")
    else:
        start_redis_server()
