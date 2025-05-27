import platform
import subprocess
import time

import docker
import yaml

from .env import environment
from .logging import get_logger

logger = get_logger(__name__)


def get_docker_client(tries: int = 3) -> docker.DockerClient:
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        if tries > 0:
            logger.warning(f'Docker client initialization failed: {e}. Retrying... ({tries} attempts left)')
            start_docker()
            return get_docker_client(tries - 1)
        else:
            logger.error(f'Failed to initialize Docker client after multiple attempts: {e}')
            raise RuntimeError('Docker client could not be initialized') from e


def start_docker(timeout: int = 100) -> bool:
    try:
        time_start = time.time()
        system = platform.system()

        if system == 'Darwin':
            subprocess.Popen(['open', '-a', 'Docker'])
        elif system == 'Windows':
            docker_path = environment.docker_path

            if not docker_path:
                logger.error('Docker Path is not set in the environment variables.')
                return False

            subprocess.Popen([docker_path])
        else:
            subprocess.Popen(['sudo', 'systemctl', 'start', 'docker'])

        while time.time() - time_start < timeout:
            try:
                client = docker.from_env()
                if client.ping():
                    logger.info('[green]Docker daemon started successfully.[/green]')
                    client.close()
                    return True
            except docker.errors.DockerException:
                time.sleep(1)

    except Exception as e:
        logger.error(f'Failed to start Docker: {e}')
        return False


def get_logs(container_name: str, tail: int = 100) -> str:
    client = get_docker_client()

    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=tail, follow=True, stream=False).decode('utf-8')
        return logs
    except docker.errors.NotFound:
        logger.error(f'Container {container_name} not found.')
        return ''
    except docker.errors.APIError as e:
        logger.error(f'Error retrieving logs for container {container_name}: {e}')
        return ''
    finally:
        client.close()


def read_docker_compose(file_path: str = 'docker-compose.yml') -> dict:
    try:
        with open(file_path, 'r') as file:
            compose_data = yaml.safe_load(file)
            return compose_data
    except FileNotFoundError:
        logger.error(f'Docker Compose file not found at {file_path}.')
        return {}
    except yaml.YAMLError as e:
        logger.error(f'Error parsing Docker Compose file: {e}')
        return {}
    except Exception as e:
        logger.error(f'Unexpected error reading Docker Compose file: {e}')
        return {}
