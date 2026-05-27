<p align="center">
  <img src="assets/logo.png" alt="AgentHijack Logo" width="200">
</p>

<div align="center">
  <h1><a href="https://agenthijack.github.io/" target="_blank">AgentHijack: Benchmarking Computer Use Agent Robustness to Common Environment Corruptions</a></h1>
  <span style="color:red"> <strong><i>We are currently organizing and presenting the code for AgentHijack. If you have any questions about the code, feel free to create an issue. 
  If you are interested in our work, please star ⭐ our project, Thx 💕.</i></strong></span>
</div>

<div align="center">

[![Paper](https://img.shields.io/badge/Paper-ICML_2026-red)](https://openreview.net/pdf?id=0H5Im3Xvuf)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Model-yellow)](https://huggingface.co/TMLR-Group-HF/AgentHijack-Agent)
![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=tmlr-group.AgentHijack)
![Stars](https://img.shields.io/github/stars/tmlr-group/AgentHijack?style=flat-square&logo=github)
![Issues](https://img.shields.io/github/issues/tmlr-group/AgentHijack?color=red)
![Closed Issues](https://img.shields.io/github/issues-closed/tmlr-group/AgentHijack?color=success)
</div>


## 📢 Updates
- 2026-05-25: We release the code of [DA-GRPO](https://github.com/super-jw/DA-GRPO). Now you can use it to train your own agents!
- 2026-05-17: We release the code of AgentHijack. Check it out!
- 2026-05-01: AgentHijack is accepted to [ICML 2026](https://agenthijack.github.io/)!

## 💾 Installation
This repository is built on [OSWorld](https://github.com/xlang-ai/OSWorld/tree/main), ref to it for installation. We recommend using VMware/Docker to run experiments, as these have been verified by us.

## 🧪 Experiments
### Open-Source and Closed-Source Multimodal Large Language Models
If you wish to run the baseline agent used in our paper, you can execute the following command, using GPT-4o under pop_ups as an example:

```bash
python run.py --path_to_vm vmware_vm_data/Ubuntu0/Ubuntu0.vmx --headless --observation_type screenshot --model openai/chatgpt-4o-latest --noise_type pop_ups --result_dir ./results
```
The results, which include screenshots, actions and summaries of the agent's task completion, will be saved in the `./results` directory in this case. You can then run the following command to obtain the result:
```bash
python show_result.py
```
For convenience, we utilize [OpenRouter](https://openrouter.ai) to integrate the APIs of different LLMs, write your api_key or change it to other interface in [mm_agents/agent.py](mm_agents/agent.py).
```python
Client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="", # put your api_key here
        )
```
### State-of-the-Art GUI Agents
We provide the deployment code in `/vllm_server`, deploy corresponding agents before running experiments. For UI-TARS-7B-DPO/UI-TARS-1.7-7B models, we recommend use 1×A100 GPU. For UI-TARS-72B-DPO, 4×A100 GPUs are needed for inference.
```bash
nohup bash vllm_server/ui-tars-1.5-7b.sh > server.log &
```
After successful deployment, run the following command to obtain the result:
```bash
python run_uitars.py --path_to_vm vmware_vm_data/Ubuntu0/Ubuntu0.vmx --headless --observation_type screenshot --model ui-tars --noise_type pop_ups --result_dir ./results
```
You can also use `run_multienv_uitars.py` for parallel execution.

> **⚠️ Note:** The `network_error` corruption is **only supported on VMware**. Its implementation drops traffic on the VMware NIC `ens160` (see `agent_network_error` in `noise.py`), which does not exist in the Docker (QEMU) guest, so disconnection has no effect under Docker. **Please use VMware for `network_error` evaluation.**
```bash
python run_multienv_uitars.py --path_to_vm "" --headless --observation_type screenshot --model ui-tars --noise_type pop_ups --num_envs 4 --result_dir ./results
```
### AgentHijack Agent
Download the AgentHijack-Agent from [huggingface](https://huggingface.co/TMLR-Group-HF/AgentHijack-Agent), then deploy it to run evaluation experiment.
```bash
nohup bash vllm_server/agenthijack-agent.sh > server.log &
```
```bash
python run_agenthijack_agent.py --path_to_vm vmware_vm_data/Ubuntu0/Ubuntu0.vmx --headless --observation_type screenshot --model ui-tars --noise_type pop_ups --result_dir ./results
```

## ⚙️ Corruption Setups
To support flexible setups for different corruptions, we offer configurable parameters in YAML file `/vllm_server/default.yaml`. Please ref to our paper for detailed explanations of these parameters.

## 📄 Citation
If you find this environment useful, please consider citing our work:
```
@inproceedings{sun2026agenthijack,
  title     = {AgentHijack: Benchmarking Computer Use Agent Robustness to Common Environment Corruptions},
  author    = {Jingwei Sun and Jianing Zhu and Yuanyi Li and Tongliang Liu and Xia Hu and Bo Han},
  booktitle = {Forty-third International Conference on Machine Learning},
  year      = {2026},
  url       = {https://openreview.net/forum?id=0H5Im3Xvuf}
}
```

## ❤️ Acknowledgement
Parts of the codes are borrowed from [OSWorld](https://github.com/xlang-ai/OSWorld) and [PopupAttack](https://github.com/SALT-NLP/PopupAttack), we express our great thanks to them for the wonderful works.