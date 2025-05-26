import subprocess
import time

from .docker import get_docker_client, read_docker_compose
from .logging import get_logger

logger = get_logger(__name__)


class ServerInfo:
    server_logs: str
    playit_logs: str
    server_status: str
    time_idle: str


def start_server(timeout: int = 100) -> None:
    logger.info("Starting Minecraft server...")

    client = get_docker_client()

    if not client:
        logger.error("Docker client could not be initialized. Cannot start server.")
        return

    subprocess.run(["docker", "compose", "up", "-d"], check=True)

    logger.info("Waiting for the server to start...")

    start_time = time.time()
    services_name = (read_docker_compose().get('services', {}).keys())

    while time.time() - start_time < timeout:
        all_ready = True

        for service in services_name:
            containers = client.containers.list(filters={"name": service})

            if not containers:
                all_ready = False
                break

            for container in containers:
                container.reload()

                if container.status != "running":
                    all_ready = False
                    break

        if all_ready:
            logger.info("All services are running.")
            break

        time.sleep(1)

    logger.info("Minecraft server started successfully.")
