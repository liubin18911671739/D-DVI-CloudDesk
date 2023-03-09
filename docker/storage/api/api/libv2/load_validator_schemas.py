

import os

import yaml
from cerberus import Validator, schema_registry

from api import app


class IsardValidator(Validator):
    # def _normalize_default_setter_genid(self, document):
    #     return _parse_string(document["name"])
    pass


def load_validators(purge_unknown=True):
    snippets_path = os.path.join(app.root_path, "schemas/snippets")
    for snippets_filename in os.listdir(snippets_path):
        if snippets_filename.startswith("."):
            continue
        with open(os.path.join(snippets_path, snippets_filename)) as file:
            snippet_schema_yml = file.read()
            snippet_schema = yaml.load(snippet_schema_yml, Loader=yaml.FullLoader)
            schema_registry.add(snippets_filename.split(".")[0], snippet_schema)

    validators = {}
    schema_path = os.path.join(app.root_path, "schemas")
    for schema_filename in os.listdir(schema_path):
        try:
            with open(os.path.join(schema_path, schema_filename)) as file:
                schema_yml = file.read()
                schema = yaml.load(schema_yml, Loader=yaml.FullLoader)
                validators[schema_filename.split(".")[0]] = IsardValidator(
                    schema, purge_unknown=purge_unknown
                )
                validators[schema_filename.split(".")[0] + ".schema"] = schema
        except IsADirectoryError:
            None
    return validators
