#!/bin/bash

# setup for wandb
export WANDB_PROJECT="codes"
export WANDB_API_KEY="[placehoder]"

deepspeed --include localhost:0,1,2,3,4,5,6,7 --master_port=9901 src/train_bash.py \
    --deepspeed configs/ds_config_zero3.json \
    --stage sft \
    --model_name_or_path /your/model/path \
    --do_train True \
    --finetuning_type full \
    --template llama2 \
    --output_dir /your/model/output/path \
    --overwrite_output_dir \
    --dataset_dir data \
    --dataset codes \
    --learning_rate 5e-05 \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 8 \
    --lr_scheduler_type cosine \
    --num_train_epochs 5.0 \
    --logging_steps 2 \
    --save_steps 20 \
    --fp16 True \
    --rope_scaling linear \
    --plot_loss True \
    --report_to wandb