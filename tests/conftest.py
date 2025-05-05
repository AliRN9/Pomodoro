import os
from dotenv import load_dotenv

pytest_plugins = [
    "tests.fixtures.load_env",
    "tests.fixtures.settings",
    "tests.fixtures.users.auth.auth_service",
    "tests.fixtures.users.auth.clients",
    "tests.fixtures.users.user_profile.repository",

]

