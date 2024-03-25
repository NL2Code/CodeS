# SnakeAI

This project contains the program scripts for the classic game "Snake" and an artificial intelligence agent that can play the game automatically. The intelligent agent is trained using deep reinforcement learning and includes two versions: an agent based on a Multi-Layer Perceptron (MLP) and an agent based on a Convolution Neural Network (CNN), with the latter having a higher average game score.

### Training Models

If you need to retrain the models, you can run `train_cnn.py` or `train_mlp.py` in the `main/` folder.

```bash
cd [parent folder of the project]/snake-ai/main
python train_cnn.py
python train_mlp.py
```
