# CrumbAI - Python Backend

## Getting Started

This project is a video editing tool that uses AI to analyze and edit videos. It employs OpenAI's GPT-4 model for content analysis, Redis for job queue management, MySQL for data storage, local file storage for storing videos, FFMPEG for video editing, and more. The project is designed to run on a Linux OS with at least 8GB of RAM and a powerful CPU due to the resource-intensive nature of the face detection process and Redis' requirement for a Linux OS.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Linux OS or Linux Server:**
  - The system should have at least 8GB of RAM and a powerful CPU.
  - A Debian-based OS is recommended.

- **OpenAI API Key** ([Obtain here](https://platform.openai.com/api-keys)):
  - Required for content analysis. You will need credits; minimal usage cost is around €1.

- **Redis** ([Installation guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)):
  - Used for job queue management. If installed on a different machine, remote connections must be enabled. ([Remote setup guide](https://stackoverflow.com/a/19091231))

- **MySQL Server** ([Installation guide](https://dev.mysql.com/doc/refman/8.3/en/linux-installation.html)):
  - Used for data storage. Only necessary if not already installed during Front-End setup.

- **Hugging Face API Key** ([Get free token](https://huggingface.co/settings/tokens)):
  - Used for speech recognition to enhance output quality.

- **Anaconda** ([Installation guide](https://docs.anaconda.com/free/anaconda/install/linux/)):
  - Manages Python virtual environments.

- **FFMPEG** ([Installation guide](https://itsfoss.com/ffmpeg/)):
  - Essential for video processing.

- **Gameplay Videos** ([Download here](https://atlantictu-my.sharepoint.com/:f:/g/personal/g00380007_atu_ie/EtTw7Fkr2cBPp9--8FJKkI4BDo6iChzpnxlDzgiWfKmjcw?e=SxVlhr)):
  - Necessary for the gameplay module. Files are hosted externally due to their size.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository:**
```
git clone https://github.com/HamzDevelopment/CrumbAI.git
```

2. **Navigate to the Project Directory:**
```
cd CrumbAI/BACKEND/AI/
```


3. **Set Up the Anaconda Environment:**
```
conda create --name myenv python=3.12
conda activate myenv
```

4. **Install Required Dependencies:**
```
pip install -r requirements.txt
```

5. **Configure Environment Variables:**
- Rename the `.env.template` file to `.env` and fill it with your secrets:
  ```
  mv .env.template .env
  ```

6. **Prepare Gameplay Footage:**
- Place all downloaded gameplay videos into `modules/gameplay/footage`.

## Deployment (Development Environment)

To run the application in a development environment, follow these steps:

1. **Open Two Terminal Windows:**
- Activate the Anaconda environment in both:
  ```
  conda activate myenv
  ```

2. **Run the Web Server:**
```
python web.py
```

3. **Run the Main Application Script:**
```
python main.py
```

These steps will enable local development and testing of new features or bug fixes.

## API Endpoints

[Documentation](https://github.com/HamzDevelopment/CrumbAI/blob/main/BACKEND/AI/api-endpoints.md)
