import time

from docker.models.containers import Container

from .constants import ContainerStatus
from .log_re import log


def check_container(container: Container) -> ContainerStatus:
    for _ in range(60):
        time.sleep(1)
        if container.status != ContainerStatus.RUNNING.name.lower():
            container.reload()
        elif container.status == ContainerStatus.RUNNING.name.lower():
            return ContainerStatus.RUNNING
        elif container.status == ContainerStatus.EXITED.name.lower():
            log(f"Container name: [{container.name}] is exited")
            return ContainerStatus.EXITED
