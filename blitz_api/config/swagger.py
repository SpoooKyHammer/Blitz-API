template = {
    "swagger": "2.0",
    "info": {
        "title": "Blitz API",
        "description": "API for creating 3D model in `.obj` format from an image. ",
        """"contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "Romulus Darwin",
            "email": "darwinromulus@gmail.com",
            "url": "",
        },
        "termsOfService": "","""
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http"
    ],
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}
