from desktop_env.desktop_env import DesktopEnv

example = {
    "id": "94d95f96-9699-4208-98ba-3c3119edf9c2",
    "instruction": "I want to install Spotify on my current system. Could you please help me?",
    "config": [
        {
            "type": "execute",
            "parameters": {
                "command": [
                    "python",
                    "-c",
                    "import pyautogui; import time; pyautogui.click(960, 540); time.sleep(0.5);"
                ]
            }
        }
    ],
    "evaluator": {
        "func": "check_include_exclude",
        "result": {
            "type": "vm_command_line",
            "command": "which spotify"
        },
        "expected": {
            "type": "rule",
            "rules": {
                "include": ["spotify"],
                "exclude": ["not found"]
            }
        }
    }
}

env = DesktopEnv(action_space="pyautogui")

obs = env.reset(task_config=example)
obs, reward, done, info = env.step("pyautogui.rightClick()")

# import base64
# from openai import OpenAI


# instruction = "search for today's weather"
# screenshot_path = "/Volumes/T7 Shield/project/osworld-c/code/OSWorld/results/test_small/clean/pyautogui/screenshot/qwen-vl-max/chrome/7b6c7e24-c58a-49fc-a5bb-d57b80e5b4c3/step_1_20250601@170456.png"
# client = OpenAI(
#     base_url="http://8.130.84.63:55382/v1",
#     api_key="empty",
# )

# ## Below is the prompt for mobile
# prompt = r"""You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task. 

# ## Output Format
# ```\nThought: ...
# Action: ...\n```

# ## Action Space

# click(start_box='<|box_start|>(x1,y1)<|box_end|>')
# left_double(start_box='<|box_start|>(x1,y1)<|box_end|>')
# right_single(start_box='<|box_start|>(x1,y1)<|box_end|>')
# drag(start_box='<|box_start|>(x1,y1)<|box_end|>', end_box='<|box_start|>(x3,y3)<|box_end|>')
# hotkey(key='')
# type(content='') #If you want to submit your input, use \"\
# \" at the end of `content`.
# scroll(start_box='<|box_start|>(x1,y1)<|box_end|>', direction='down or up or right or left')
# wait() #Sleep for 5s and take a screenshot to check for any changes.
# finished()
# call_user() # Submit the task and call the user when the task is unsolvable, or when you need the user's help.


# ## Note
# - Use Chinese in `Thought` part.
# - Summarize your next action (with its target element) in one sentence in `Thought` part.

# ## User Instruction
# """

# with open(screenshot_path, "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
# response = client.chat.completions.create(
#     model="ui-tars",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": prompt + instruction},
#                 {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_string}"}},
#             ],
#         },
#     ],
#     frequency_penalty=1,
#     max_tokens=128,
#     timeout=6000
# )
# print(response.choices[0].message.content)