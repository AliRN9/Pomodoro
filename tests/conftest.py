import asyncio
import os
from dotenv import load_dotenv
import pytest

pytest_plugins = [
    "tests.fixtures.anonymous_async_client",
    "tests.fixtures.infrastructure",
    "tests.fixtures.users.auth.auth_service",
    "tests.fixtures.users.auth.clients",
    "tests.fixtures.users.user_profile.repository",

]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    env = os.path.join(os.getcwd(), f'.test.env')
    if os.path.exists(env):
        print("Removing existing .test.env")
        load_dotenv(dotenv_path=env, override=True)
