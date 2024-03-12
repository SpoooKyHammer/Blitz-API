

class Dev:
    """Conatins resources used in dev."""

    REDIS_URL = "redis://localhost:6379"
    """Directs to the local machine."""

class Prod:
    """Contains resources used in prod."""
    
    REDIS_URL = "redis://redis:6379"
    """Directs to the docker service"""


