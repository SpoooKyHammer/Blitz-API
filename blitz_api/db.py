
import pymongo
import gridfs


class DataBase:

    """
    Provides database connectivity works with MongoDB driver 

    Methods
    -------
        `init()`
            Initializes the database, this method should be called at the app level for establising database connectivity
        `get_mongo_client()`
            Gives the database client i.e `pymongo.MongoClient`
        `get_gridFs()`
            Gives GFS to work with files 
    """

    __mongo_client = None
    __gfs = None

    @classmethod
    def init(cls) -> None:
        """
        Initializes the `pymongo.MongoClient` and `gridfs.GridFs` at app level for database connectivity.
        """
        
        if cls.__mongo_client is None:
            print("[DATABASE] Connecting...")
            cls.__mongo_client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.kcofxlo.mongodb.net/?retryWrites=true&w=majority")
            print("[DATABASE] Successfully connected")

        if cls.__gfs is None:
            print("[GFS] Initializing...")
            cls.__gfs = gridfs.GridFS(cls.__mongo_client.get_database("blitz"))
            print("[GFS] Successfully initialized")

    @classmethod
    def get_mongo_client(cls) -> pymongo.MongoClient | None:
        """
        Returns
        -------
            `pymongo.MongoClient` or `None` if `DataBase` is not initialized
        """
        return cls.__mongo_client
    
    @classmethod
    def get_gridFs(cls) -> gridfs.GridFS | None:
        """
        Returns
        -------
            `gridfs.GridFS` or `None` if `DataBase` is not initialized
        """
        return cls.__gfs

