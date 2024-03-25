def get_repo_sketch_prompt(readme_content):
    instruction = f"""Below is a detailed README.md of repository. Please write a repository sketch in the form of a tree, including all folders, files, as well as imports information if necessary.

---
README.md
---
{readme_content}

---
Repository Sketch
---
"""
    return instruction

def get_file_sketch_prompt(readme_content, repo_sketch_content, path):
    instruction = f"""Below is a detailed README.md of repository, repository sketch, as well as a file path. Please write a corresponding file sketch.

---
README.md
---
{readme_content}

---
Repository Sketch
---
Here is a practicable repository sketch.

```
{repo_sketch_content}
```

---
File Path
---
{path}

---
File Sketch
---
"""
    return instruction

def get_function_body_prompt(readme_summary, repo_sketch_content, relevant_file_sketch_content, function_header_content):
    instruction = f"""Below is a detailed README.md of repository, repository sketch, as well as some relevant file sketches. Please fill the function body for the given function header.

---
README.md
---
{readme_summary}

---
Repository Sketch
---
Here is a practicable repository sketch.

```
{repo_sketch_content}
```

{relevant_file_sketch_content}

---
Function Complement
---
{function_header_content}
"""
    return instruction

def get_relervant_file_sketch_content(idx, this_relevant_path, this_python_file_sketch):
    instruction = f"""---
Relevant File Sketch/{idx}
---
Here is the file sketch of `{this_relevant_path}`.

```python
{this_python_file_sketch}
```

"""
    return instruction

def get_current_file_sketch_content(idx, path, current_python_content):
    instruction = f"""---
Current File Sketch/{idx}
---
Here is the file sketch of `{path}`.

```python
{current_python_content}
```

"""
    return instruction