# 19 Repositories for Evaluation

To collect the evaluation repositories, we follow three steps: crawling, filtering, and grouping.
Firstly, we extensively crawl open-source repositories via GitHub API.
From GitHub, we request around 300 most-starred repositories with Python as the main language from August 2023 onwards.

Secondly, we refine the crawled repository set by filtering out repositories based on their type, quality, and topic.
- for types, we rule out those framework- or library-oriented repositories, mainly focusing on standalone projects.
- for quality, we select those repositories with a well-organized README and well-constructed source code.
For each repository, we require that its README document contains a meta description and a detailed feature description. The descriptions are necessary to declare the goal of a repository. we also check the validity of the source code by manually running the repository or reading the code.
- for topics, we try our best to cover diverse areas of repositories (e.g. AI, cyber security, shell tools, etc.).

Thirdly, we group the selected repositories into different difficulty levels based on the scale of a repository.
The repositories are grouped into three levels:
repositories of Hard level should contain > 10 Python files or > 2500 Python code lines;
Repositories of Medium level should contain > 5 Python files or > 500 Python code lines;
Other repositories are classified as Easy level.