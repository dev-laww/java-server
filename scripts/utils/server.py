import subprocess
import time
from typing import Optional

from mcstatus import JavaServer

from .docker import get_docker_client, read_docker_compose
from .logging import get_logger
from ..models import ServerStatus

logger = get_logger(__name__)


def start_server(timeout: int = 100) -> None:
    logger.info('Starting Minecraft server...')

    client = get_docker_client()

    if not client:
        logger.error('Docker client could not be initialized. Cannot start server.')
        return

    subprocess.run(['docker', 'compose', 'up', '-d'], check=True)

    logger.info('Waiting for the server to start...')

    start_time = time.time()
    services_name = read_docker_compose().get('services', {}).keys()

    while time.time() - start_time < timeout:
        all_ready = True

        for service in services_name:
            containers = client.containers.list(filters={'name': service})

            if not containers:
                all_ready = False
                break

            for container in containers:
                container.reload()

                if container.status != 'running':
                    all_ready = False
                    break

        if all_ready:
            logger.info('All services are running.')
            client.close()
            break

        time.sleep(1)

    logger.info('Minecraft server started successfully.')


def stop_server() -> None:
    logger.info('Stopping Minecraft server...')

    client = get_docker_client()

    if not client:
        logger.error('Docker client could not be initialized. Cannot stop server.')
        return

    subprocess.run(['docker', 'compose', 'down'], check=True)

    logger.info('Minecraft server stopped successfully.')


def get_status() -> Optional[ServerStatus]:
    client = get_docker_client()

    if not client:
        logger.error('Docker client could not be initialized. Cannot fetch status.')
        return None

    services_name = read_docker_compose().get('services', {}).keys()

    if not services_name:
        logger.error('No services found in docker-compose file.')
        return None

    try:
        server = JavaServer.lookup('localhost:25565')
        status = server.status()
        players_online = status.players.online
        max_players = status.players.max if status.players.max else 0
        latency = status.latency
        server_logs = client.containers.get('server-server-1').logs(tail=20).decode('utf-8', errors='ignore')
        playit_logs = client.containers.get('playit-agent').logs(tail=20).decode('utf-8', errors='ignore')

        return ServerStatus(
            status='Online',
            players_online=players_online,
            max_players=max_players,
            latency=latency,
            server_logs=server_logs,
            playit_logs=playit_logs,
        )
    except Exception as e:
        logger.error(f'Error fetching server status: {e}')
        return ServerStatus(status='Unreachable')
    finally:
        client.close()
