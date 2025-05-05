import os
import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    env = os.path.join(os.getcwd(), f'.test.env')
    if os.path.exists(env):
        load_dotenv(dotenv_path=env, override=True)
