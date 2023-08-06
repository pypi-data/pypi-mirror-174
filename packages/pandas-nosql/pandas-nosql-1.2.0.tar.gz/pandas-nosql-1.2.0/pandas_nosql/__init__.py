import pandas
from io import BytesIO
from uuid import uuid4
import pickle


def read_mongo(
        database: str,
        collection: str,
        normalize: bool = False,
        **mongo_client_kwargs):
    """Read a MongoDB collection into a Pandas DataFrame.
    Uses MongoClient from pymongo by MongoDB.

    Args:
        database (str): Name of the Database in MongoDB
        collection (str): Name of the Collection in database
        normalize (bool, optional):
        - Uses pandas.json_normalize to flatten json-like values.
        - Defaults to False.

    Returns:
        pandas.core.frame.DataFrame
    """
    try:
        from pymongo import MongoClient
    except ModuleNotFoundError:
        raise ModuleNotFoundError('read_mongo requires pymongo. Please pip or conda install pymongo.')
    with MongoClient(**mongo_client_kwargs) as client:
        db = client[database]
        collection = db[collection]
        if normalize:
            data = pandas.json_normalize(collection.find(), sep='_')
        else:
            data = pandas.DataFrame.from_records(collection.find())
    return data


pandas.read_mongo = read_mongo


def to_mongo(
        self,
        database: str,
        collection: str,
        mode: str = 'a',
        **mongo_client_kwargs):
    """Insert DataFrame records into a MongoDB collection.
    Uses MongoClient from pymongo by MongoDB.

    Args:
        database (str): Name of the Database in MongoDB
        collection (str): Name of the Collection in database
        mode (str):
            - 'w' to overwrite collection.
            - 'a' to append to collection.
            - Defaults to 'a'.
        **mongo_client_kwargs: All arguments are passed to MongoClient
    """
    try:
        from pymongo import MongoClient
    except ModuleNotFoundError:
        raise ModuleNotFoundError('to_mongo requires pymongo. Please pip or conda install pymongo.')
    with MongoClient(**mongo_client_kwargs) as client:
        db = client[database]
        collection = db[collection]
        records = self.to_dict(orient='records')
        match mode:
            case 'w':
                collection.drop()
                collection.insert_many(records)
            case 'a':
                collection.insert_many(records)
            case _:
                raise ValueError(f'{mode!r} provided for mode. Mode must be w or a')


pandas.core.frame.DataFrame.to_mongo = to_mongo


def read_elastic(
        hosts: str,
        username: str,
        password: str,
        index: str,
        fields: tuple,
        verify_certs: bool = False,
        split_source: bool = False,
        **es_kwargs):
    """Read an Elasticsearch index into a Panda DataFrame.
    Uses the Python package elasticsearch from Elastic.

    Args:
        hosts (str): Full url of Elasticsearch host with port number
        username (str): Username used to access Elasticsearch
        password (str): password for associated username
        index (str): Index in specified Elasticsearch host(s)
        fields (tuple): The fields in the Elasticsearch index to query
        verify_certs (bool): Defaults to False.
        split_source (bool):
        - If True, breaks _source into individual columns
        - If False, all fields specified in fields we be placed in a dictionary under _source
        - Defaults to False.
        es_kwargs: All arguments are passed to the Elasticsearch class

    Returns:
        pandas.core.frame.DataFrame
    """
    try:
        from elasticsearch import Elasticsearch
    except ModuleNotFoundError:
        raise ModuleNotFoundError('read_elastic requires elasticsearch-py. Please pip or conda install elasticsearch')
    assert isinstance(fields, tuple), 'fields must be a tuple'
    with Elasticsearch(hosts, basic_auth=(username, password), verify_certs=verify_certs, **es_kwargs) as es:
        index_count = es.count(index=index)['count']
        data = es.search(
            index=index,
            body={'_source': fields},
            size=index_count)['hits']['hits']
    if split_source:
        dataframe = pandas.json_normalize(data)
        dataframe.columns = dataframe.columns.str.removeprefix('_source.')
        return dataframe.drop(columns='_score')
    return pandas.DataFrame.from_records(data).drop(columns='_score')


pandas.read_elastic = read_elastic


def to_elastic(
        self,
        hosts: str | list,
        username: str,
        password: str,
        index: str,
        verify_certs: bool = False,
        mode: str = 'a',
        stats_only: bool = True,
        **es_kwargs):
    """Insert DataFrame records into an Elasticsearch index.
    Uses the Python package elasticsearch by Elastic.

    Args:
        hosts (str): Full url of Elasticsearch host with port number
        username (str): Username used to access Elasticsearch
        password (str): password for associated username
        index (str): Index in specified Elasticsearch host(s)
        verify_certs (bool): Defaults to False.
        mode (str): 'w' to overwrite. 'a' to append. Defaults to a.
        stats_only (bool): Defaults to True.
    """
    try:
        from elasticsearch import Elasticsearch
        from elasticsearch.helpers import bulk
    except ModuleNotFoundError:
        raise ModuleNotFoundError('to_elastic requires elasticsearch-py. Please pip or conda install elasticsearch')
    with Elasticsearch(hosts, basic_auth=(username, password), verify_certs=verify_certs, **es_kwargs) as es:
        match mode:
            case 'w':
                if es.indices.exists(index=index):
                    es.indices.delete(index=index)
                es.indices.create(index=index)
                docs = ({'_index': index, '_source': value} for value in self.to_dict(orient='index').values())
                bulk(es, docs, stats_only=stats_only)
            case 'a':
                docs = ({'_index': index, '_source': value}
                        for value in self.to_dict(orient='index').values())
                bulk(es, docs, stats_only=stats_only)
            case _:
                raise ValueError(f'{mode!r} given for mode. Mode must be w or a')


pandas.core.frame.DataFrame.to_elastic = to_elastic


def read_redis(host: str, port: int, redis_key: str, db: int = 0):
    """Read a pandas DataFrame which was saved to Redis using "pandas.to_redis"
    Any DataFrames read that was not saved using "pandas.to_redis" is not guaranteed
    to appear as expected.
    Uses the Redis class from the Python package redis-py by Redis.

    Args:
        host (str): Redis host
        port (int): port for host
        redis_key (str): key stored in host
        db (int, optional): Defaults to 0.

    Returns:
        pandas.core.frame.DataFrame
    """
    try:
        from redis import Redis
    except ModuleNotFoundError:
        raise ModuleNotFoundError('read_redis requires redis-py.\nPlease `pip install redis` or `conda install redis-py`.')
    with Redis(host=host, port=port, db=db) as r:
        return pandas.read_pickle(BytesIO(r.get(redis_key)))


pandas.read_redis = read_redis


def to_redis(
        self,
        host: str,
        port: int,
        redis_key: str,
        db: int = 0,
        expire_seconds: int = None):
    """Save DataFrame into Redis under the given redis_key.
    Rerunning to_redis with a persisted redis_key already in Redis will overwrite the redis_key
    Uses the Redis class from the Python package redis-py by Redis.

    Args:
        host (str): Redis host
        port (int): port for host
        redis_key (str): key stored in host
        db (int, optional): Defaults to 0.
        expire_seconds (int):
        - Seconds before dataframe is purged from Redis.
        - None: Dataframe will persist in Redis
        - Defaults to None.
    """
    try:
        from redis import Redis
    except ModuleNotFoundError:
        raise ModuleNotFoundError('to_redis requires redis-py.\nPlease `pip install redis` or `conda install redis-py`.')
    with Redis(host=host, port=port, db=db) as r:
        if expire_seconds is None:
            r.set(redis_key, pickle.dumps(self))
        else:
            r.set(redis_key, pickle.dumps(self))
            r.expire(redis_key, expire_seconds)


pandas.core.frame.DataFrame.to_redis = to_redis


def read_cassandra(contact_points: list, port: int, keyspace: str, table: str):
    """Read an Apache Cassandra table into a Panda DataFrame
    Uses the Python package cassandra-driver By DataStax.

    Args:
        contact_points (list): A list of urls/nodes for the desired Cassandra database.
        port (int): The port for the contact_points.
        keyspace (str): The keyspace for the Cassandra database.
        table (str): The table for the keyspace

    Returns:
        pandas.core.frame.DataFrame
    """
    try:
        from cassandra.cluster import Cluster
    except ModuleNotFoundError:
        raise ModuleNotFoundError('read_cassandra requires cassandra-driver. Please `pip install cassandra-driver`.')
    with Cluster(contact_points=contact_points, port=port) as cluster:
        session = cluster.connect(keyspace=keyspace)
        rows = [row for row in session.execute(f'SELECT * FROM {table};')]
        return pandas.DataFrame.from_records(rows, columns=rows[0]._fields)


pandas.read_cassandra = read_cassandra


def to_cassandra(
        self,
        contact_points: list,
        port: int,
        keyspace: str,
        table: str,
        mode: str = 'a',
        replication: dict | None = None):
    """Write or append a Pandas Dataframe to a Cassandra database table.
    Write mode will automatically create a primary key column "uuid" if one does not exists.
    The primary key will always be "uuid".

    Pandas dtypes will be inserted as the following:
        * object -> text
        * int64 -> bigint
        * float64 -> double
        * bool -> boolean
        * datetime64[ns] -> timestamp
    No other pandas dtypes are supported at this time.

    Uses the Python package cassandra-driver By DataStax.

    Args:
        contact_points (list): A list of urls/nodes for the desired Cassandra database.
        port (int): The port for the contact_points.
        keyspace (str): The keyspace for the Cassandra database.
        table (str): The table for the keyspace
        mode (str): 'w' to overwrite. 'a' to append. Defaults to a.
        replication (dict | None): Behavior alters base on mode.
        - If mode 'w', replication should be a dictionary with replication setting for create a keyspace
        - If mode is 'a' replication is ignored
        - Default is None
    """
    try:
        from cassandra.cluster import Cluster, BatchStatement
    except ModuleNotFoundError:
        raise ModuleNotFoundError('to_cassandra requires cassandra-driver. Please `pip install cassandra-driver`.')
    type_mapping = {
        'object': 'text',
        'int64': 'bigint',
        'float64': 'double',
        'bool': 'boolean',
        'datetime64[ns]': 'timestamp'}
    with Cluster(contact_points=contact_points, port=port) as cluster:
        match mode:
            case 'w':
                session = cluster.connect()
                session.execute(f'CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH REPLICATION = {replication};')
                session = cluster.connect(keyspace=keyspace)
                session.execute(f'DROP TABLE IF EXISTS {table};')
                session.execute(f'CREATE TABLE {table} ("uuid" uuid PRIMARY KEY);')
                for col, col_type in self.dtypes.items():
                    if col != 'uuid':
                        session.execute(f'ALTER TABLE {table} ADD {col} {type_mapping[col_type.name]};')
            case 'a':
                session = cluster.connect(keyspace=keyspace)
            case _:
                raise ValueError(f'{mode!r} given for mode. Mode must be w or a')
        df_has_uuid = 'uuid' in self.columns
        if df_has_uuid:
            cols = ','.join(self.columns)
            col_len = len(self.columns)
        else:
            cols = ','.join(self.columns) + ',uuid'
            col_len = len(self.columns) + 1
        qs = ('?,' * col_len).rstrip(',')
        insertions = session.prepare(f'INSERT INTO {table} ({cols}) VALUES ({qs})')
        batch = BatchStatement()
        if df_has_uuid:
            for row in self.itertuples(index=False):
                batch.add(insertions, row)
        else:
            for row in self.itertuples(index=False):
                r = list(row)
                r.append(uuid4())
                batch.add(insertions, r)
        session.execute(batch)


pandas.core.frame.DataFrame.to_cassandra = to_cassandra
