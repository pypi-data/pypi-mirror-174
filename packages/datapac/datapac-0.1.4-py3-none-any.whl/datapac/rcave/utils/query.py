from typing import Literal
from typing import Union

import yaml
from pydantic import BaseModel
from pydantic import Field
from typing_extensions import Annotated

from datapac.utils import templating

Graph = Annotated[Union["S3Node", "PostgresNode"], Field(discriminator="type")]


class S3Node(BaseModel):
    type: Literal["s3"]

    key: str
    bucket: str


class PostgresNode(BaseModel):
    type: Literal["postgres"]

    table: str
    where: dict

    relationships: list["Graph"] = []


class Query(BaseModel):
    path: str
    graph: Graph

    class Config:
        orm_mode = True


def infer_variables(query: Query):
    with open(query.path) as f:
        return templating.infer_variables(f.read()) - {"parent"}


def load(path: str) -> Query:
    with open(path) as f:
        return Query(path=path, **yaml.safe_load(f.read()))
