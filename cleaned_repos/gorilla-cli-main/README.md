# Gorilla CLI

Gorilla CLI powers your command-line interactions with a user-centric tool. Simply state your objective, and Gorilla CLI will generate potential commands for execution. Gorilla today supports ~1500 APIs, including Kubernetes, AWS, GCP,  Azure, GitHub, Conda, Curl, Sed, and many more. No more recalling intricate CLI arguments! 🦍

Developed by UC Berkeley as a research prototype, Gorilla-CLI prioritizes user control and confidentiality:
 - Commands are executed solely with your explicit approval.
 - While we utilize queries and error logs (stderr) for model enhancement, we NEVER collect output data (stdout).

## Usage

Some examples

```bash
$ gorilla list all my GCP instances
» gcloud compute instances list --format="table(name,zone,status)"
  gcloud compute instances list --format table
  gcloud compute instances list --format="table(name, zone, machineType, status)"
```
```bash
$ gorilla get the image ids of all pods running in all namespaces in kubernetes
» kubectl get pods --all-namespaces -o jsonpath="{..imageID}"
  kubectl get pods --all --namespaces
  kubectl get pod -A -o jsonpath='{range .items[*]}{"\n"}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
```


## How It Works

Gorilla-CLI fuses the capabilities of various Language Learning Models (LLMs) like Gorilla LLM, OpenAI's GPT-4, Claude v1, and others to present a user-friendly command-line interface. For each user query, we gather responses from all contributing LLMs, filter, sort, and present you with the most relevant options. 

### Arguments

```
usage: go_cli.py [-h] [-p] [command_args ...]

Gorilla CLI Help Doc

positional arguments:
  command_args   Prompt to be inputted to Gorilla

optional arguments:
  -h, --help     show this help message and exit
  -p, --history  Display command history
```

The history feature lets the user go back to previous commands they've executed to re-execute in a similar fashion to terminal history.