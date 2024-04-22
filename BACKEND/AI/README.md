# CrumbAI - Python Backend

## Getting Started

This project is a video editing tool that uses AI to analyze and edit videos. It uses OpenAI's GPT-4 model for content analysis, Redis for job queue management, and MySQL for data storage, and Local File Storage for storing videos, FFMPEG for video editing, and more. The project is designed to run on a Linux server with at least 8GB of RAM and a powerful CPU. This is because the face detection process is very resource-intensive.


## Prerequisites

Before you begin, ensure you have the following installed:
  
  - [OpenAI API Key](https://platform.openai.com/api-keys)
    - You do need credits, but the usage is low. At least €1.
  - [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/): This is used for job queue management.
    - If you install it on another machine, you need to allow remote connections. [Guide](https://stackoverflow.com/a/19091231)
  - Linux server: The server should have at least 8GB of RAM and a powerful CPU.
    - A Debian-based OS is recommended.
  - [MySQL Server](https://dev.mysql.com/doc/refman/8.3/en/linux-installation.html): This is used for data storage. It should be the same one that the NextJS backend uses.
  - [Hugging Face API key](https://huggingface.co/settings/tokens): This is used for speech recognition. It's not needed, but it would improve the output.
  - [Anaconda](https://docs.anaconda.com/free/anaconda/install/linux/): This is used for python package management.
  - [FFMPEG](https://itsfoss.com/ffmpeg/): This is used for video processing. You can install it from the FFMPEG website.
  - [Gameplay Videos](): 

## Installation

1. Clone the repository to your local machine.
2. Navigate to the AI folder.
3. Create a new Anaconda environment and activate it:
   <pre>conda create --name myenv conda activate myenv</pre> 
4. Install the required Python:
   <pre>pip install -r requirements.txt</pre> 
5. Rename ``.env.template`` file to ``.env`` and fill it it with your secrets.


## Deployment (Development Environment)

To deploy the application, you need to run both the web.py and main.py scripts. You can do this by opening two terminal windows, navigating to the project directory in each, and running the scripts:

Terminal 1:
```
python web.py
```

Terminal 2:
```
python main.py
```


