import sqlalchemy as __sq__

# ----------------------------------------------------
# Context manager class to open and close connections as required
# ----------------------------------------------------


class ConnectionManager:
    """
    Context manager class to open and close connections as required.
    """

    def __init__(self, engine: __sq__.engine):
        self.engine: __sq__.engine = engine

    def __enter__(self):
        self.connection: __sq__.engine.base.Connection = self.engine.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
