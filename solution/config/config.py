from os import path, getenv
from dotenv import load_dotenv
from solution.processing import AIModelAPI


CURRENT_FILE = path.abspath(__file__)
CURRENT_DIR = path.dirname(CURRENT_FILE)
PARENT_DIR = path.dirname(CURRENT_DIR)
ROOT_DIR = path.dirname(PARENT_DIR)


path_to_process = path.join(ROOT_DIR, 'to_process')
path_to_input_data = path.join(ROOT_DIR, 'input_data')
path_to_instruct_json = path.join(ROOT_DIR, 'solution', 'config', 'prompt_data.json')
path_to_output = path.join(ROOT_DIR, 'solutions.json')

load_dotenv()

chatgpt_api = AIModelAPI(getenv("API_GPT"), "https://api.openai.com/v1", "gpt-4-turbo") #gpt-4o-mini
deepseek_api = AIModelAPI(getenv("API_DS"), "https://api.deepseek.com", "deepseek-chat")
