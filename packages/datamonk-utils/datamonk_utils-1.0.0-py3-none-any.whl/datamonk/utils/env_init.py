from dotenv import dotenv_values, find_dotenv, load_dotenv
from logging import config
import time
import os


def get_env_vars(flow_name):
    env_location = find_dotenv(filename=f".env.{flow_name}",
                               raise_error_if_not_found=True,
                               usecwd=True
                               )

    load_dotenv(env_location)

    CONFIG=dotenv_values(env_location)
    os.environ["FLOW_NAME"], CONFIG["FLOW_NAME"] = flow_name, flow_name
    os.environ["run_timestamp"], CONFIG["run_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S"),\
                                                           time.strftime("%Y-%m-%dT%H:%M:%S")
    return CONFIG


config.fileConfig('logging.conf', disable_existing_loggers=False)
