from config import (
    deepseek_api,
    chatgpt_api,
    path_to_instruct_json,
    path_to_process,
    path_to_input_data,
    path_to_output
)
from chats_process import process_all_chats


def main():
    model = deepseek_api

    process_all_chats(model=model,
                      path_to_input=path_to_input_data,
                      path_to_process=path_to_process,
                      path_to_instruct=path_to_instruct_json,
                      path_to_output=path_to_output
    )

if __name__ == "__main__":
    main()
