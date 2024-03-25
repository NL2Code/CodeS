export CUDA_VISIBLE_DEVICES=0

python src/web_demo.py \
    --model_name_or_path /dev/shm/codes7b/full/2024-01-16-00-00-01/checkpoint-100 \
    --template llama2 \
    --cutoff_len 10000 \
    --rope_scaling dynamic