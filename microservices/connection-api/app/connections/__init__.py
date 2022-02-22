from app.connections.schemas import ConnectionSchema  # noqa


def register_routes(api, app, root="api"):
    from app.connections.controllers import api as connections_api

    api.add_namespace(connections_api, path=f"/{root}")
