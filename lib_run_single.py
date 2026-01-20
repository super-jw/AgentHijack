import datetime
import json
import logging
import os
import yaml
import base64
import time
from wrapt_timeout_decorator import *
from perturb_utils import scale_actions
from noise import perturb_agents
logger = logging.getLogger("desktopenv.experiment")


def run_single_example(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    agent.reset(runtime_logger)
    if agent.noise_type not in ["verification", "network_error"]:
        env.reset(task_config=example)
    elif agent.noise_type == "network_error":
        env.reset_step1(task_config=example)
        perturb_agents(agent.noise_type, agent.noise_config, None, agent.platform, env, -1, instruction, example)
        env.reset_step2(task_config=example)
    elif agent.noise_type == "verification":
        env.reset(task_config=example)
        perturb_agents(agent.noise_type, agent.noise_config, None, agent.platform, env, -1, instruction, example)
    time.sleep(10) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            step_idx,
            instruction,
            obs,
            env=env,
            example=example
        )
        if agent.noise_type != "clean":
            # with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_pre.png"),
            #             "wb") as _f:
            #         # screenshot before action
            #         _f.write(obs['screenshot'])
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_agent_observe.png"),
                        "wb") as _f:
                    # screenshot before action, transform from byte string
                    _f.write(base64.b64decode(agent.observations[-1]["screenshot"]))
        for action in actions:
            # update the action according to the resolution
            if agent.noise_type == 'resolution':
                with open(file=agent.noise_config) as f:
                    cfg = yaml.load(f, Loader=yaml.FullLoader)['noise'][agent.noise_type]
                logger.info("Before scale: Step %d: %s", step_idx + 1, action)
                action = scale_actions(action, 1/cfg['scale'])
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            if agent.noise_type == "clean":
                with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                        "wb") as _f:
                    _f.write(obs['screenshot'])
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "summary": agent.history_summary[-1] if len(agent.history_summary)>0 else "None",
                    "action": response+action,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }, ensure_ascii=False))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))


def setup_logger(example, example_result_dir):
    runtime_logger = logging.getLogger(f"desktopenv.example.{example['id']}")
    runtime_logger.setLevel(logging.DEBUG)
    runtime_logger.addHandler(logging.FileHandler(os.path.join(example_result_dir, "runtime.log")))
    return runtime_logger
