# CodeS: Natural Language to Code Repository via Multi-Layer Sketch

## Video Demo of CodeS

Please see [./assets/codes_demo.mp4](./assets/codes_demo.mp4)

## Project Directory

```python
.
├── assets
├── clean_repo.py # ./repos/ -> ./cleaned_repos/
├── cleaned_repos
├── craft_train_data.py # ./output -> ./training_data
├── extract_sketch.py # ./cleaned_repos/ -> ./output
├── outputs
├── projects # two projects
├── prompt_construction_utils.py
├── repos
├── requirements.txt
├── run_step1_clean.sh # runing ./clean_repo.py
├── run_step2_extract_sketch.sh # runing ./extract_sketch.py
├── run_step3_make_data.sh # runing ./craft_train_data.py
├── scripts
├── train # *train codes model* scripts
├── training_data
└── validation # *evaluation* scripts
```

## Creating Command Data for 100 Repositories

1. Download the selected repositories to the `repos` directory and unzip them.
2. Preprocess the repositories:
```bash
bash run_step1_clean.sh
```
3. Extract command training data for `RepoSketcher`, `FileSketcher`, and `SketchFiller`:
```bash
bash run_step2_extract_sketch.sh
```
4. Compile the command data from 100 repositories:
```bash
bash run_step3_make_data.sh
```

## Training

1. Place the created command data into `./train/data` and configure `dataset_info.json` according to the structure described at https://github.com/hiyouga/LLaMA-Factory/tree/main/data.

2. Start the training process:

```bash
vim ./train/run_train_multi_gpu.sh
bash ./train/run_train_multi_gpu.sh
```

## Evaluation

1. Install `SketchBLEU`, similar to `CodeBLEU`.

2. Perform inference on `SketchEval`:
```bash
python ./codes/validation/evaluation-scripts/from_scratch_inference.py
```

3. Convert the inference results for the entire repository:
```bash
python ./codes/validation/evaluation-scripts/transfer_output_to_repo.py
```

4. Evaluate the generated repository as with `CodeBLEU`:

```bash
python ./codes/validation/evaluation-scripts/batch_eval/get_metric.py
```

## Reference
If you want to use the models, you need to cite our following paper:
```
@article{zan2024codes,
  title={CodeS: Natural Language to Code Repository via Multi-Layer Sketch},
  author={Zan, Daoguang and Yu, Ailun and Liu, Wei and Chen, Dong and Shen, Bo and Li, Wei and Yao, Yafen and Gong, Yongshun and Chen, Xiaolin and Guan, Bei and others},
  journal={arXiv preprint arXiv:2403.16443},
  year={2024}
}
```
