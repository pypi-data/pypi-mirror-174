from jinja2 import DebugUndefined
from jinja2 import Environment
from jinja2 import StrictUndefined
from jinja2 import Template
from jinja2 import meta


def render(template: str, context: dict) -> str:
    return Template(template, undefined=StrictUndefined).render(**context)


def partial_render(template: str, context: dict) -> str:
    return Template(template, undefined=DebugUndefined).render(**context)


def infer_variables(template: str) -> set[str]:
    env = Environment()
    ast = env.parse(template)
    return meta.find_undeclared_variables(ast)
