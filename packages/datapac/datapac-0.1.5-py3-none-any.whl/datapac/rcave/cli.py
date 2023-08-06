import os

import click

from datapac.config import Config
from datapac.config import Environment
from datapac.config import load as load_config
from datapac.package import package
from datapac.rcave.services.pull import pull as pull_service
from datapac.rcave.services.push import push as push_service
from datapac.rcave.sources.postgres.source import load_artefacts as pg_load_artefacts
from datapac.rcave.sources.s3.source import load_artefacts as s3_load_artefacts
from datapac.rcave.utils.query import Query
from datapac.rcave.utils.query import infer_variables
from datapac.rcave.utils.query import load as load_query

config: Config | None


def validate_query(ctx, param, value) -> Query:
    return load_query(value)


def validate_env(ctx, param, value) -> Environment:
    if config is None:
        raise click.UsageError("Missing config file")

    if value not in config.env:
        raise click.UsageError("Invalid env name")

    return config.env[value]


def validate_vars(ctx, param, value) -> dict:
    return {k: v for k, v in value}


def validate_path(ctx, param, value) -> str:
    return os.path.join(os.getcwd(), value)


def validate_config(ctx, param, value) -> Config:
    return load_config(value)


def resolve_variables_for_pull(variables: dict, query: Query):
    missing = infer_variables(query) - set(variables.keys())
    prompts = {var: click.prompt(f"Enter {var}", type=str) for var in missing}
    return variables | prompts


@click.group()
@click.option(
    "c",
    "--config",
    "-c",
    help="Path to datapac config",
    callback=validate_config,
    default=os.environ.get("DATAPAC_CONFIG_PATH"),
)
def cli(c):
    global config
    config = c


@cli.command()
@click.option(
    "query",
    "--query",
    "-q",
    required=True,
    help="Path to datapac query",
    callback=validate_query,
)
@click.option(
    "env",
    "--env",
    "-e",
    required=True,
    help="Name of env to pull from",
    callback=validate_env,
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=(str, str),
    multiple=True,
    callback=validate_vars,
)
@click.argument(
    "path",
    type=str,
    callback=validate_path,
)
def pull(query: Query, env: Environment, variables: dict, path: str):
    resolved_variables = resolve_variables_for_pull(
        env.variables | variables,
        query=query,
    )

    with package.create(path) as pkg:
        pull_service(env, query, resolved_variables, pkg)


@cli.command()
@click.option(
    "env",
    "--env",
    "-e",
    required=True,
    help="Name of env to pull from",
    callback=validate_env,
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=(str, str),
    multiple=True,
    callback=validate_vars,
)
@click.argument(
    "path",
    type=str,
    callback=validate_path,
)
def push(env: Environment, variables: dict, path: str):
    with package.open(path, [pg_load_artefacts, s3_load_artefacts]) as pkg:
        with package.render(pkg, env.variables | variables) as rendered:
            push_service(env, rendered)


if __name__ == "__main__":
    cli()
