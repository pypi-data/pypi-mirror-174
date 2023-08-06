from datapac.config import Environment
from datapac.package.package import Package
from datapac.rcave.sources.postgres import source as postgres
from datapac.rcave.sources.s3 import source as s3
from datapac.rcave.utils.query import Graph
from datapac.rcave.utils.query import PostgresNode
from datapac.rcave.utils.query import Query
from datapac.rcave.utils.query import S3Node


def pull(
    env: Environment,
    query: Query,
    variables: dict,
    pkg: Package,
):
    for artefact in crawl(env, query.graph, variables):
        pkg.add_artefact(artefact)


def crawl(env: Environment, node: Graph, variables: dict):
    if isinstance(node, PostgresNode):
        for result in postgres.pull_node(env, node, variables):
            yield result

            for child in node.relationships:
                yield from crawl(env, child, variables | {"parent": result.data})
    elif isinstance(node, S3Node):
        yield s3.pull_node(env, node, variables)
    else:
        raise ValueError(f"unknown node: {node}")
