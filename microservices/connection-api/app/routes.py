def register_routes(api, app, root="api"):
    from app.connections import register_routes as attach_locations

    # Add routes
    attach_locations(api, app)
