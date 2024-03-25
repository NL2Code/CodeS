# 100 Code Repositories for Supervised Fine-Tuning

> searched condition on GitHub: `stars:>100 language:Python created:<2023-08-01`

To adapt base models for the NL2Repo task, we perform supervised fine-tuning based on a collection of $100$ code repositories. To obtain these repositories, we first crawl Python repositories created before August 1, 2023 from GitHub. Choosing this creation date as a filtering criterion aims to prevent data leakage into our newly constructed evaluation benchmark SketchEval, thus ensuring the fairness of our experiments. After that, we further exclude repositories with less than $100$ stars to ensure high-quality training data.Based on the filtered repositories, we manually select $100$ high-quality Python ones.