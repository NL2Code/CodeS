# easier-docker

## Repository Introduction
This is based on [docker-py](https://github.com/docker/docker-py?tab=readme-ov-file) which makes it easier to run your program in docker.
Configure your container image information more easily in python, allowing the container in docker to execute the configured program you want to execute.

## Usage
💡 Please check config parameters in [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/containers.html)

### Use examples in code
```bash
python example.py
```
```python
# example.py
import os

from easierdocker import EasierDocker

if __name__ == '__main__':
    host_script = os.path.dirname(os.path.abspath(__file__))
    container_script = '/path/to/container'
    config = {
        'image': 'python:3.9',
        'name': 'python_test',
        'volumes': {
            f'{host_script}': {'bind': container_script, 'mode': 'rw'}
        },
        'detach': True,
        'command': ["sh", "-c", f'cd {container_script} &&'
                                'python docker_example.py'],
    }
    easier_docker = EasierDocker(config)
    easier_docker.start()
    """
    >>> 2023-12-29 15:17:31,901 - INFO - easier-docker ==> Network id: [13c5a6cb0137], name: [host]
    >>> 2023-12-29 15:17:31,901 - INFO - easier-docker ==> Network id: [27d6b39aeef6], name: [none]
    >>> 2023-12-29 15:17:31,901 - INFO - easier-docker ==> Network id: [2c9ae2fbfe9d], name: [bridge]
    >>> 2023-12-29 15:17:31,901 - INFO - easier-docker ==> Network: [bridge] is found locally...
    >>> 2023-12-29 15:17:31,901 - INFO - easier-docker ==> Find docker image: [python:3.9] locally...
    >>> 2023-12-29 15:17:31,906 - INFO - easier-docker ==> Image: [python:3.9] is found locally
    >>> 2023-12-29 15:17:31,906 - INFO - easier-docker ==> Find docker container: [python_test] locally...
    >>> 2023-12-29 15:17:31,910 - INFO - easier-docker ==> ContainerNotFound: [python_test], it will be created
    >>> 2023-12-29 15:17:34,217 - INFO - easier-docker ==> Container name: [python_test] is running
    >>> 2023-12-29 15:17:34,217 - INFO - easier-docker ==> Container id: [fd7fad6e9995] is running
    >>> 2023-12-29 15:17:34,217 - INFO - easier-docker ==> Container ip address: [172.17.0.2]
    >>> 2023-12-29 15:17:34,217 - INFO - easier-docker ==> Successfully container is running and be created at 2023-12-29T07:17:31.912747785Z
    """
```
The content of docker_example.py is
```python
# docker_example.py
def main():
    import logging
    import time
    for i in range(1, 101):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'sleep 30s, times:{i}')
        time.sleep(30)


if __name__ == '__main__':
    main()

```

### Run directly from configuration file
Currently supports type of file: _yml_, _yaml_, _json_
```bash
easier-docker -c config.yaml
```
The content of config.yaml is
```yaml
# config.yaml
image: python:3.9
name: python_test
volumes:
  /Users/admin/data/code_project/easier-docker/example:
    bind: /path/to/container
    mode: rw
detach: true
command:
  - sh
  - -c
  - cd /path/to/container && python docker_example.py
      
    # >>> 2023-12-29 15:08:58,703 - INFO - easier-docker ==> config =
    # >>>  {
    # >>>     "image": "python:3.9",
    # >>>     "name": "python_test",
    # >>>     "volumes": {
    # >>>         "D:\\code-project\\EasierDocker\\example": {
    # >>>             "bind": "/path/to/container",
    # >>>             "mode": "rw"
    # >>>         }
    # >>>     },
    # >>>     "detach": true,
    # >>>     "command": [
    # >>>         "sh",
    # >>>         "-c",
    # >>>         "cd /path/to/container && python docker_example.py"
    # >>>     ]
    # >>>  }
    # >>> 2023-12-29 15:08:58,707 - INFO - easier-docker ==> Find docker image: [python:3.9] locally...
    # >>> 2023-12-29 15:08:58,724 - INFO - easier-docker ==> Image: [python:3.9] is found locally
    # >>> 2023-12-29 15:08:58,725 - INFO - easier-docker ==> Find docker container: [python_test] locally...
    # >>> 2023-12-29 15:08:58,730 - INFO - easier-docker ==> ContainerNotFound: [python_test], it will be created
    # >>> 2023-12-29 15:09:00,989 - INFO - easier-docker ==> Container name: [python_test] is running
    # >>> 2023-12-29 15:09:00,990 - INFO - easier-docker ==> Container id: [a9b642f2ddf3] is running
    # >>> 2023-12-29 15:09:00,990 - INFO - easier-docker ==> Container ip address: [172.17.0.2]
    # >>> 2023-12-29 15:09:00,991 - INFO - easier-docker ==> Successfully container is running and be created at 2023-12-29T07:08:58.738605891Z

```