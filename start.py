import os
import re
import sys
import subprocess
import random
import argparse
import platform
import socket

try:
    from tzlocal import get_localzone
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "tzlocal"], check=True)
    from tzlocal import get_localzone
try:
    from dotenv import load_dotenv
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "python-dotenv"], check=True
    )
    from dotenv import load_dotenv
try:
    import win32com.client as wim
except ImportError:
    wim = None


def prompt_user(prompt, default=None):
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
    else:
        user_input = input(f"{prompt}: ").strip()
    return user_input if user_input else default


def is_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def is_tool_installed(tool):
    try:
        subprocess.run(
            [tool, "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_docker():
    system = platform.system().lower()
    if system == "linux":
        if is_tool_installed("apt-get"):
            commands = [
                "sudo apt-get update",
                "sudo apt-get install -y docker.io",
                "sudo systemctl start docker",
                "sudo systemctl enable docker",
                "sudo usermod -aG docker $USER",
            ]
        elif is_tool_installed("yum"):
            commands = [
                "sudo yum install -y docker",
                "sudo systemctl start docker",
                "sudo systemctl enable docker",
                "sudo usermod -aG docker $USER",
            ]
        else:
            print("Unsupported Linux distribution. Please install Docker manually.")
            return False
    elif system == "darwin":
        print(
            "Please install Docker Desktop for Mac from https://www.docker.com/products/docker-desktop"
        )
        return False
    elif system == "windows":
        print(
            "Please install Docker Desktop for Windows from https://www.docker.com/products/docker-desktop"
        )
        return False
    else:
        print(f"Unsupported operating system: {system}")
        return False

    for command in commands:
        subprocess.run(command, shell=True, check=True)
    return True


def install_docker_compose():
    system = platform.system().lower()
    if system == "linux":
        commands = [
            'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose',
            "sudo chmod +x /usr/local/bin/docker-compose",
        ]
        for command in commands:
            subprocess.run(command, shell=True, check=True)
        return True
    elif system in ["darwin", "windows"]:
        print(
            "Docker Compose is included in Docker Desktop. Please ensure Docker Desktop is installed."
        )
        return False
    else:
        print(f"Unsupported operating system: {system}")
        return False


def check_prerequisites():
    if not is_tool_installed("docker"):
        print("Docker is not installed.")
        install = prompt_user("Would you like to install Docker? (y/n)", "y")
        if install.lower() != "y":
            print("Docker is required to run Sophia III. Exiting.")
            sys.exit(1)
        if not install_docker():
            print("Failed to install Docker. Please install it manually and try again.")
            sys.exit(1)

    if not is_tool_installed("docker-compose"):
        print("Docker Compose is not installed.")
        install = prompt_user("Would you like to install Docker Compose? (y/n)", "y")
        if install.lower() != "y":
            print("Docker Compose is required to run Sophia III. Exiting.")
            sys.exit(1)
        if not install_docker_compose():
            print(
                "Failed to install Docker Compose. Please install it manually and try again."
            )
            sys.exit(1)


def run_shell_command(command):
    print(f"Executing: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    while True:
        try:
            output = process.stdout.readline()
        except:
            print("View the logs in docker with 'docker compose logs'")
            break
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return_code = process.poll()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command)


def get_default_env_vars():
    workspace_folder = os.path.normpath(os.path.join(os.getcwd(), "WORKSPACE"))
    machine_tz = get_localzone()
    return {
        "SOPHIA_III_API_KEY": "",
        "STREAMLIT_SOPHIA_III_URI": "http://sophia_iii:7437",
        "SOPHIA_III_URI": "http://localhost:7437",
        "SOPHIA_III_PORT": "7437",
        "SOPHIA_III_INTERACTIVE_PORT": "3437",
        "SOPHIA_III_STREAMLIT_PORT": "8501",
        "SOPHIA_III_AGENT": "Sophia III",
        "SOPHIA_III_BRANCH": "stable",
        "SOPHIA_III_FILE_UPLOAD_ENABLED": "true",
        "SOPHIA_III_VOICE_INPUT_ENABLED": "true",
        "SOPHIA_III_FOOTER_MESSAGE": "Powered by Sophia III",
        "SOPHIA_III_REQUIRE_API_KEY": "false",
        "SOPHIA_III_RLHF": "true",
        "SOPHIA_III_SHOW_SELECTION": "conversation,agent",
        "SOPHIA_III_SHOW_AGENT_BAR": "true",
        "SOPHIA_III_SHOW_APP_BAR": "true",
        "SOPHIA_III_CONVERSATION_MODE": "select",
        "SOPHIA_III_SHOW_OVERRIDE_SWITCHES": "tts,websearch,analyze-user-input",
        "ALLOWED_DOMAINS": "*",
        "APP_DESCRIPTION": "A chat powered by Sophia III.",
        "APP_NAME": "Sophia III Chat",
        "APP_URI": "http://localhost:3437",
        "STREAMLIT_APP_URI": "http://localhost:8501",
        "AUTH_WEB": "http://localhost:3437/user",
        "CREATE_AGENT_ON_REGISTER": "true",
        "CREATE_SOPHIA_III_AGENT": "true",
        "DISABLED_PROVIDERS": "",
        "DISABLED_EXTENSIONS": "",
        "WORKING_DIRECTORY": workspace_folder.replace("\\", "/"),
        "TZ": machine_tz,
        "INTERACTIVE_MODE": "chat",
        "THEME_NAME": "doom",
        "ALLOW_EMAIL_SIGN_IN": "true",
        "DATABASE_TYPE": "sqlite",
        "DATABASE_NAME": "models/sophia_iii",
        "LOG_LEVEL": "INFO",
        "LOG_FORMAT": "%(asctime)s | %(levelname)s | %(message)s",
        "UVICORN_WORKERS": "10",
        "SOPHIA_III_AUTO_UPDATE": "true",
        "EZLOCALAI_URI": f"http://{get_local_ip()}:8091/v1/",
        "DEFAULT_MODEL": "QuantFactory/dolphin-2.9.2-qwen2-7b-GGUF",
        "VISION_MODEL": "deepseek-ai/deepseek-vl-1.3b-chat",
        "LLM_MAX_TOKENS": "32768",
        "WHISPER_MODEL": "base.en",
        "GPU_LAYERS": "0",
        "WITH_STREAMLIT": "true",
        "WITH_EZLOCALAI": "false",
        "REGISTRATION_DISABLED": "false",
        "SOPHIA_III_ALLOW_MESSAGE_EDITING": "true",
        "SOPHIA_III_ALLOW_MESSAGE_DELETION": "true",
        "SOPHIA_III_SHOW_CHAT_THEME_TOGGLES": "",
        "LOG_VERBOSITY_SERVER": "3",
        "AOL_CLIENT_ID": "",
        "AOL_CLIENT_SECRET": "",
        "APPLE_CLIENT_ID": "",
        "APPLE_CLIENT_SECRET": "",
        "AUTODESK_CLIENT_ID": "",
        "AUTODESK_CLIENT_SECRET": "",
        "AWS_CLIENT_ID": "",
        "AWS_CLIENT_SECRET": "",
        "AWS_REGION": "",
        "AWS_USER_POOL_ID": "",
        "GITHUB_CLIENT_ID": "",
        "GITHUB_CLIENT_SECRET": "",
        "GOOGLE_CLIENT_ID": "",
        "GOOGLE_CLIENT_SECRET": "",
        "MICROSOFT_CLIENT_ID": "",
        "MICROSOFT_CLIENT_SECRET": "",
    }


def set_environment(env_updates=None):
    load_dotenv()
    env_vars = get_default_env_vars()
    # Update with existing environment variables
    for key in env_vars.keys():
        env_value = os.getenv(key)
        if env_value is not None:
            env_vars[key] = env_value
    # Apply updates
    if env_updates:
        for key, value in env_updates.items():
            if key in env_vars:
                env_vars[key] = value
    # Ensure SOPHIA_III_API_KEY is set
    if env_vars["SOPHIA_III_API_KEY"] == "":
        env_vars["SOPHIA_III_API_KEY"] = "".join(
            random.choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
            for i in range(64)
        )
    # Write to .env file
    env_file_content = "\n".join(
        [f'{key}="{value}"' for key, value in env_vars.items()]
    )
    with open(".env", "w") as file:
        file.write(env_file_content)
    if str(env_vars["WITH_EZLOCALAI"]).lower() == "true":
        print("Starting ezLocalai, this can take several minutes...")
        start_ezlocalai()
    dockerfile = "docker-compose.yml"
    if env_vars["SOPHIA_III_BRANCH"] != "stable":
        dockerfile = "docker-compose-dev.yml"
