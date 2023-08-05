from __future__ import annotations
import logging
from enum import Enum
from pathlib import Path

try: # usage with Django
    from django.db import router, connections
    from django.core.exceptions import ImproperlyConfigured
    with_django = True
except: # usage without Django
    with_django = False


logger = logging.getLogger(__name__)

ZUT_DB_BASE_DIR = Path(__file__).parent

class Backend(Enum):
    POSTGRESQL = 1


class BackendNotSupported(ValueError):
    def __init__(self, info: Backend|type):
        if isinstance(info, Backend):
            message = f"backend not supported: {info.name}"
        elif isinstance(info, type):
            message = f"connection type not supported: {info.__module__}.{info.__name__}"
        else:
            message = info
        super().__init__(message)


def get_backend(connection):
    search = type(connection).__module__ + "." + type(connection).__name__
    if search == "django.utils.connection.ConnectionProxy":
        search = connection._connections[connection._alias].vendor
    elif hasattr(connection, "vendor"):
        # e.g. django.db.backends.postgresql.base.DatabaseWrapper, django.contrib.gis.db.backends.postgis.base.DatabaseWrapper
        search = connection.vendor

    if search in ["postgresql", "psycopg2.extensions.connection"]:
        return Backend.POSTGRESQL
    else:
        raise BackendNotSupported(type(connection))


def get_connection(connection = None, model: type = None, for_write: bool = False):
    if connection:
        if model:
            raise ValueError("connection and model options cannot be both used")
        if not isinstance(connection, str):
            return connection

    if not with_django:
        raise ValueError("usage without connection option requires Django")

    try:
        if isinstance(connection, str):
            alias = connection

        elif model:
            if not hasattr(model, "objects"):
                raise ValueError(f"type {model.__name__} does not seem to be a Django model")

            alias = router.db_for_write(model) if for_write else router.db_for_read(model)
            if not alias:
                alias = "default"

        else:
            alias = "default"

        return connections[alias]

    except ImproperlyConfigured as err:
        raise ValueError(f"Django improperly configured: please provide \"connection\" option")


def dictfetchall(cursor) -> list[dict]:
    """
    Return all rows from a cursor as a dict.
    """ 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]


def deploy_sql(*paths: Path|str, encoding = "utf-8", connection = None):
    connection = get_connection(connection=connection)

    actual_paths: list[Path] = []
    for path in paths:
        if isinstance(path, str):
            path = Path(path)
        actual_paths.append(path)

    actual_paths.sort()

    for path in actual_paths:
        if path.is_dir():
            subpaths = sorted(path.iterdir())
            deploy_sql(*subpaths, encoding=encoding, connection=connection)

        elif not path.name.endswith(".sql"):
            continue # ignore

        elif path.name.endswith("_revert.sql"):
            continue # ignore

        else:
            logger.info("execute %s", path)
            sql = path.read_text(encoding=encoding)
            with connection.cursor() as cursor:
                cursor.execute(sql)


def revert_sql(*paths: Path|str, encoding = "utf-8", connection=None):
    connection = get_connection(connection=connection)

    actual_paths: list[Path] = []
    for path in paths:
        if isinstance(path, str):
            path = Path(path)
        actual_paths.append(path)

    actual_paths.sort(reverse=True)

    for path in actual_paths:
        if path.is_dir():
            subpaths = sorted(path.iterdir())
            revert_sql(*subpaths, encoding=encoding, connection=connection)

        elif not path.name.endswith("_revert.sql"):
            continue # ignore

        else:
            logger.info("execute %s", path)
            sql = path.read_text(encoding=encoding)
            with connection.cursor() as cursor:
                cursor.execute(sql)
