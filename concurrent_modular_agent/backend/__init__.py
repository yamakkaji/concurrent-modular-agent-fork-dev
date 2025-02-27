import subprocess
from loguru import logger
# from logging import getLogger
# logger = getLogger(__name__)
from os import path as osp


DOCKER_COMPOSE_FILE = osp.join(osp.dirname(__file__), "docker-compose.yml")
DOCKER_COMPOSE_FILE_TEST = osp.join(osp.dirname(__file__), "docker-compose.test.yml")


def _get_docker_compose_command(test_env=False):
    if test_env:
        docker_compose_file = DOCKER_COMPOSE_FILE_TEST
    else:
        docker_compose_file = DOCKER_COMPOSE_FILE
    cmd = ["docker", "compose", "-f", docker_compose_file]
    if test_env:
        cmd += ["-p" "test"]
    return cmd

def start(test_env=False):
    if is_alive(test_env=test_env):
        logger.info("Docker Compose is already running")
        return
    try:
        cmd = _get_docker_compose_command(test_env) + ["up", "-d"]
        result = subprocess.run(
            cmd,
            #cwd=osp.dirname(docker_compose_file),
            check=True,
            text=True,
            capture_output=True,
        )
        for l in result.stdout.splitlines():
            logger.info(l)
        for l in result.stderr.splitlines():
            logger.info(l)
        # logger.debug(f"Docker Compose up with {file_path} executed successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running docker compose up: {e.stderr}")
        raise


def stop(test_env=False):
    try:
        cmd = _get_docker_compose_command(test_env) + ["down"]      
        result = subprocess.run(
            cmd,
  #          ["docker", "compose", "-f", docker_compose_file, "down"],
   #         cwd=osp.dirname(docker_compose_file),
            check=True,
            capture_output=True,
            text=True
        )
        for l in result.stdout.splitlines():
            logger.info(l)
        for l in result.stderr.splitlines():
            logger.info(l)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running docker compose down: {e.stderr}")
        raise

def is_alive(test_env=False):
    try:
        cmd = _get_docker_compose_command(test_env) + ["ps"]     
        result = subprocess.run(
            cmd,
#            ["docker", "compose", "-f", docker_compose_file, "ps"],
 #           cwd=osp.dirname(docker_compose_file),
            check=True,
            capture_output=True,
            text=True
        )
        if "Up" in result.stdout:
            return True
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while checking docker compose status: {e.stderr}")
        return False
