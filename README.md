<p align="center">
  <img src="assets/demo_logo.png" alt="Banner">
</p>

<div align="center">
  <h1><a href="" target="_blank">AgentHijack: Benchmarking Computer Use Agent Robustness to Common Environment Corruptions</a></h1>
  <span style="color:red"> <strong><i>We are currently organizing and presenting the code for AgentHijack. If you have any questions about the code, feel free to create an issue. 
  If you are interested in our work, please star ⭐ our project, Thx 💕.</i></strong></span>
</div>

<div align="center">

[![Paper](https://img.shields.io/badge/Paper-arXiv:2506.00618-red)]()
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Datasets-yellow)]()
<img src="https://img.shields.io/badge/License-Apache_2.0-green.svg" alt="License">
<img src="https://visitor-badge.laobi.icu/badge?page_id=super-jw.AgentHijack"/>
<img src="https://img.shields.io/github/stars/super-jw/AgentHijack?style=flat-square&logo=github" alt="Stars">
<img src="https://img.shields.io/github/issues/super-jw/AgentHijack?color=red" alt="Issues">
<img src="https://img.shields.io/github/issues-closed/super-jw/AgentHijack?color=success" alt="Closed Issues">
</div>


## 📢 Updates
- 2026-01-23: We release the code of AgentHijack. Check it out!
- 2026-01-23: We release the AgentHijack in [arxiv]()!

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
### AgentHijack Agent
Download the AgentHijack-Agent from [huggingface](), then deploy it to run evaluation experiment.
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
@misc{OSWorld,
      title={OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments}, 
      author={Tianbao Xie and Danyang Zhang and Jixuan Chen and Xiaochuan Li and Siheng Zhao and Ruisheng Cao and Toh Jing Hua and Zhoujun Cheng and Dongchan Shin and Fangyu Lei and Yitao Liu and Yiheng Xu and Shuyan Zhou and Silvio Savarese and Caiming Xiong and Victor Zhong and Tao Yu},
      year={2024},
      eprint={2404.07972},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

## ❤️ Acknowledgement
Parts of the codes are borrowed from [OSWorld](https://github.com/xlang-ai/OSWorld) and [PopupAttack](https://github.com/SALT-NLP/PopupAttack), we express our great thanks to them for the wonderful works.