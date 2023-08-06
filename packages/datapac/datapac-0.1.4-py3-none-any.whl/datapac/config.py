import json
import os
import pathlib

import toml
from pydantic import BaseModel

from datapac.utils import templating


class S3Config(BaseModel):
    endpoint_url: str | None
    aws_access_key_id: str
    aws_secret_access_key: str


class PostgresConfig(BaseModel):
    host: str
    user: str
    password: str | None
    dbname: str | None


class Sources(BaseModel):
    postgres: PostgresConfig
    s3: S3Config


class Environment(BaseModel):
    sources: Sources
    variables: dict[str, str] = {}


class Config(BaseModel):
    env: dict[str, Environment]


def load(path: str) -> Config:
    extension = pathlib.Path(path).suffix.strip(".")

    with open(path) as f:
        raw_config = f.read()

    config = templating.render(raw_config, dict(os.environ))

    match extension:
        case "toml":
            return Config(**toml.loads(config))
        case "json":
            return Config(**json.loads(config))
        case format:
            raise RuntimeError(f"unsupported config type [{format}]")
