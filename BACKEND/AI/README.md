# CrumbAI - Python Backend

## Getting Started

This project is a video editing tool that uses AI to analyze and edit videos. It uses OpenAI's GPT-4 model for content analysis, Redis for job queue management, MySQL for data storage, Local File Storage for storing videos, FFMPEG for video editing, and more. The project is designed to run on a Linux server with at least 8GB of RAM and a powerful CPU. This is because the face detection process is very resource-intensive, and Redis requires a Linux OS.


## Prerequisites

Before you begin, ensure you have the following installed:

  - Linux server: The server should have at least 8GB of RAM and a powerful CPU.
    - A Debian-based OS is recommended.
    - **Further prerequisites would need to be installed on a Linux OS not Windows OS.**
      
  - [OpenAI API Key](https://platform.openai.com/api-keys): This is used for content analysis.
    - You do need credits, but the usage is low. At least €1. Follow the linked link to get the API key.
      
  - [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/): This is used for job queue management. Follow the linked guide to install Redis on your system.
    - If you install it on another machine, you need to allow remote connections. [Guide](https://stackoverflow.com/a/19091231
      
  - [MySQL Server](https://dev.mysql.com/doc/refman/8.3/en/linux-installation.html): This is used for data storage. It should be the same one that the NextJS backend uses. Follow the linked guide to install MySQL on your system, you do not need to do         this if you installed it during the Front-End Installation.
    
  - [Hugging Face API key](https://huggingface.co/settings/tokens): This is used for speech recognition. It's not needed, but it would improve the output. Follow the linked guide to acquire a free token.
    
  - [Anaconda](https://docs.anaconda.com/free/anaconda/install/linux/): This is used for python's virtual environment. Follow the linked guide to install it on your system.
    
  - [FFMPEG](https://itsfoss.com/ffmpeg/): This is used for video processing. Follow the linked guide to install FFMPEG on your device. Follow the linked guide to install it on your system.
    
  - [Gameplay Videos](https://atlantictu-my.sharepoint.com/:f:/g/personal/g00380007_atu_ie/EtTw7Fkr2cBPp9--8FJKkI4BDo6iChzpnxlDzgiWfKmjcw?e=SxVlhr): Needed for the gameplay module, files are too big for GitHub so they were uploaded elsewhere. Simply       follow the link and download the files.  

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository:**
   - Clone the repository to your local machine using the following command (If you have not already):
     ```
     git clone [[URL of the Repository]](https://github.com/HamzDevelopment/CrumbAI.git)
     ```

2. **Navigate to the Project Directory:**
   - Change into the directory where the AI components of the project are located:
     ```
     cd CrumbAI/BACKEND/AI/
     ```

3. **Set Up the Anaconda Environment:**
   - Create a new Anaconda environment and activate it using:
     ```bash
     conda create --name myenv python=3.8
     conda activate myenv
     ```
   - Ensure you replace `myenv` with your desired environment name and specify the Python version if necessary.

4. **Install Required Dependencies:**
   - Install all the necessary Python libraries specified in `requirements.txt`:
     ```
     pip install -r requirements.txt
     ```

5. **Configure Environment Variables:**
   - Rename the `.env.template` file to `.env`.
   - Within Linux:
     ```
     mv .env.template .env
     ```
   - Open the `.env` file in a text editor and fill it with your secrets and configurations.

6. **Prepare Gameplay Footage:**
   - Place all the downloaded gameplay videos into the `modules/gameplay/footage` directory inside the `BACKEND/AI` directory, to ensure they can be accessed by the application.

## Deployment (Development Environment)

To run the application in a development environment, you need to launch both the web server and the main application script. Follow these steps to deploy:

1. **Open Two Terminal Windows:**
   - Ensure that your Anaconda environment is activated in both terminals:
     ```
     conda activate myenv
     ```

2. **Run the Web Server:**
   - In the first terminal, navigate to the project directory and start the web server by running:
     ```
     python web.py
     ```

3. **Run the Main Application Script:**
   - In the second terminal, navigate to the project directory and execute the main script:
     ```
     python main.py
     ```

This setup will allow you to run and test the application locally, facilitating the development and testing of new features or debugging current issues.


## API Endpoints

[Documenation](https://github.com/HamzDevelopment/CrumbAI/blob/main/BACKEND/AI/api-endpoints.md)


