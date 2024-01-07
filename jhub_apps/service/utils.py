import base64
import logging
import os
from unittest.mock import Mock

import requests
from jupyterhub.app import JupyterHub
from traitlets.config import LazyConfigValue

from jhub_apps.spawner.types import FrameworkConf, FRAMEWORKS_MAPPING


logger = logging.getLogger(__name__)


def get_jupyterhub_config():
    hub = JupyterHub()
    os.environ["PROXY_API_SERVICE_PORT"] = "*"
    os.environ["HUB_SERVICE_PORT"] = "*"
    jhub_config_file_path = os.environ["JHUB_JUPYTERHUB_CONFIG"]
    logger.info(f"Getting JHub config from file: {jhub_config_file_path}")
    hub.load_config_file(jhub_config_file_path)
    config = hub.config
    logger.info(f"JHub config from file: {config}")
    logger.info(f"JApps config: {config.JAppsConfig}")
    return config


def get_conda_envs(config):
    """This will extract conda environment from the JupyterHub config"""
    if isinstance(config.JAppsConfig.conda_envs, list):
        return config.JAppsConfig.conda_envs
    elif isinstance(config.JAppsConfig.conda_envs, LazyConfigValue):
        return []
    elif callable(config.JAppsConfig.conda_envs):
        try:
            logger.info("JAppsConfig.conda_envs is a callable, calling now..")
            return config.JAppsConfig.conda_envs()
        except Exception as e:
            logger.exception(e)
            return []
    else:
        raise ValueError(
            f"Invalid value for config.JAppsConfig.conda_envs: {config.JAppsConfig.conda_envs}"
        )


def get_fake_spawner_object(auth_state):
    fake_spawner = Mock()
    fake_spawner.user.get_auth_state.return_value = auth_state
    fake_spawner.log = logger
    return fake_spawner


async def get_spawner_profiles(config, auth_state=None):
    """This will extract spawner profiles from the JupyterHub config
    If the Spawner is KubeSpawner
    """
    profile_list = config.KubeSpawner.profile_list
    if isinstance(profile_list, list):
        return config.KubeSpawner.profile_list
    elif isinstance(profile_list, LazyConfigValue):
        return []
    elif callable(profile_list):
        try:
            logger.info("config.KubeSpawner.profile_list is a callable, calling now..")
            return await profile_list(get_fake_spawner_object(auth_state))
        except Exception as e:
            logger.exception(e)
            return []
    else:
        raise ValueError(
            f"Invalid value for config.KubeSpawner.profile_list: {profile_list}"
        )


def encode_file_to_data_url(filename, file_contents):
    """Converts image file to data url to display in browser."""
    base64_encoded = base64.b64encode(file_contents)
    filename_ = filename.lower()
    if filename_.endswith(".jpg") or filename_.endswith(".jpeg"):
        mime_type = "image/jpeg"
    elif filename_.endswith('.svg'):
        mime_type = "image/svg+xml"
    else:
        file_extension = filename_.split('.')[-1]
        mime_type = f"image/{file_extension}"
    data_url = f"data:{mime_type};base64,{base64_encoded.decode('utf-8')}"
    return data_url


def get_default_thumbnail(framework_name):
    framework: FrameworkConf = FRAMEWORKS_MAPPING.get(framework_name)
    thumbnail_url = framework.logo
    try:
        response = requests.get(thumbnail_url)
    except Exception as e:
        logger.info(f"Unable to fetch thumbnail from url: {thumbnail_url}:")
        logger.exception(e)
        return
    if response.status_code == 200:
        thumbnail_content = response.content
        thumbnail_filename = thumbnail_url.split("/")[-1]
        return encode_file_to_data_url(filename=thumbnail_filename, file_contents=thumbnail_content)


async def get_thumbnail_data_url(framework_name, thumbnail):
    if thumbnail:
        thumbnail_contents = await thumbnail.read()
        thumbnail_data_url = encode_file_to_data_url(
            thumbnail.filename, thumbnail_contents
        )
    else:
        thumbnail_data_url = get_default_thumbnail(framework_name)
    return thumbnail_data_url
