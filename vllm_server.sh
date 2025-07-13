# UI-TARS-72B-DPO
CUDA_VISIBLE_DEVICES=0,1,2,3 python -m vllm.entrypoints.openai.api_server --served-model-name ui-tars --model /cpfs04/shared/AI4Good/models/UI-TARS/UI-TARS-72B-DPO --port 55382 --tensor-parallel-size 4 --gpu-memory-utilization 0.85 --limit-mm-per-prompt "image=5" -
-disable-custom-all-reduce
# UI-TARS-7B-DPO
CUDA_VISIBLE_DEVICES=0,1,2,3 python -m vllm.entrypoints.openai.api_server --served-model-name ui-tars --model /cpfs04/shared/AI4Good/models/UI-TARS/UI-TARS-7B-DPO --port 55382 --tensor-parallel-size 1 --gpu-memory-utilization 0.85 --limit-mm-per-prompt "image=5" -
-disable-custom-all-reduce
# Qwen2.5-VL-72B-Instruct
CUDA_VISIBLE_DEVICES=0,1,2,3 python -m vllm.entrypoints.openai.api_server --served-model-name qwen-vl --model /cpfs04/shared/AI4Good/models/Qwen/Qwen2.5-VL-72B-Instruct --port 55382 --tensor-parallel-size 4 --gpu-memory-utilization 0.85 --limit-mm-per-prompt "image=5" -
-disable-custom-all-reduce