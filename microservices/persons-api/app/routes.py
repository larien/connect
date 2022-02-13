def register_routes(api, app, root="api"):
    from app.persons import register_routes as attach_persons

    # Add routes
    attach_persons(api, app)
