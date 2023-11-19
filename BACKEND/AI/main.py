from dotenv import load_dotenv
import os
from modules.gpt.main import gpt
def main():
    print('Starting Crumb AI...')
    load_dotenv()

    open_ai = gpt(env('OPENAI_API_KEY'))
    






def env(variable):
    return os.getenv(variable)




if __name__ == '__main__':
    main()