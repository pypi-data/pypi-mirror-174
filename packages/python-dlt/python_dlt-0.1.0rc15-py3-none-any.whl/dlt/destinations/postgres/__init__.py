from typing import Type

from dlt.common.schema.schema import Schema
from dlt.common.typing import ConfigValue
from dlt.common.configuration import with_config
from dlt.common.destination import DestinationCapabilitiesContext, JobClientBase, DestinationClientConfiguration

from dlt.destinations.postgres.configuration import PostgresClientConfiguration


@with_config(spec=PostgresClientConfiguration, namespaces=("destination", "postgres",))
def _configure(config: PostgresClientConfiguration = ConfigValue) -> PostgresClientConfiguration:
    return config


def capabilities() -> DestinationCapabilitiesContext:
    # https://www.postgresql.org/docs/current/limits.html
    caps = DestinationCapabilitiesContext()
    caps.update({
        "preferred_loader_file_format": "insert_values",
        "supported_loader_file_formats": ["insert_values"],
        "max_identifier_length": 64,
        "max_column_length": 64,
        "max_query_length": 32 * 1024 * 1024,
        "is_max_query_length_in_bytes": True,
        "max_text_data_type_length": 10485760,
        "is_max_text_data_type_length_in_bytes": True
    })
    return caps


def client(schema: Schema, initial_config: DestinationClientConfiguration = ConfigValue) -> JobClientBase:
    # import client when creating instance so capabilities and config specs can be accessed without dependencies installed
    from dlt.destinations.postgres.postgres import RedshiftClient

    return RedshiftClient(schema, _configure(initial_config))  # type: ignore


def spec() -> Type[DestinationClientConfiguration]:
    return PostgresClientConfiguration
