
CUDA_VISIBLE_DEVICES=1,2,3,4,5 python src/train_bash.py \
    --stage sft \
    --do_predict \
    --model_name_or_path /your/model/output/path \
    --dataset /your/dataset/path \
    --template llama2 \
    --output_dir /your/model/output/path/results \
    --per_device_eval_batch_size 1 \
    --max_samples 100 \
    --predict_with_generate \
    --cutoff_len 10000 \
    --rope_scaling dynamic \
    --fp16