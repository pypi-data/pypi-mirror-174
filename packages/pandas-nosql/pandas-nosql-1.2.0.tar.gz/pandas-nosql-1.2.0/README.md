# Pandas-NoSQL
__Pandas-NoSQL adds read and write capabilities to pandas for several nosql databases__

---
Pandas read and write methods for:

* MongoDB
* Elasticsearch
* Redis
* Apache Cassandra

The dependencies used for the functions are:

* pymongo by MongoDB
* elasticsearch by Elastic
* redis-py by Redis
* cassandra-driver by DataStax

---

## Installation
```bash
$ pip install pandas-nosql
```
---
## Documentation

### MongoDB
```python
# Read a MongoDB collection into a DataFrame
# Defaults: host='localhost' port=27017
# For nested collections use normalize=True

import pandas as pd
import pandas_nosql

df = pd.read_mongo(
    database = 'test_db',
    collection = 'test_col',
    normalize = True,
    host = 'localhost',
    port = 27017
    )

# Write DataFrame to MongoDB collection
# modify_colletion parameter is to help prevent accidental overwrites

df.to_mongo(
    database = 'test_db',
    collection = 'test_col2',
    mode = 'a',
    host = 'localhost',
    port = 27017
    )
```

### Elasticsearch
```python
import pandas as pd
import pandas_nosql

# Read an Elastic index into a DataFrame
# To Access localhost: 
#   * hosts='https://localhost:9200'
#   * verify_certs=False
# If "xpack.security.enabled: false" use http instead
# To split out _source use split_source=True

elastic_cols = ('make', 'model', 'purchase_date', 'miles')

df = pd.read_elastic(
    hosts = 'https://localhost:9200',
    username = 'elastic',
    password = 'strong_password',
    index = 'test_index',
    fields = elastic_cols,
    verify_certs = False
    split_source = True
    )

# Write DataFrame to Elastic Index
df.to_elastic(
    hosts = 'https://localhost:9200',
    username = 'elastic',
    password = 'strong_password',
    index = 'test_index',
    mode = 'w'
    )
```

### Redis
```python
import pandas as pd
import pandas_nosql

# Read a DataFrame that was sent to Redis using the to_redis method
# A DataFrame not sent to Redis using the to_redis method is not guaranteed to be read properly

# To Access localhost:
#   * host='localhost'
# To persist the DataFrame in Redis use expire_seconds=None
# To set an expiration for the DataFrame pass an integer to expire_seconds

df = pd.read_redis(
    host = 'localhost',
    port = 6379,
    redis_key = 'test_key'
    )

# Write a DataFrame to Redis
df.to_redis(
    host = 'localhost',
    port = 6379,
    redis_key = 'test_key',
    expire_seconds = None
    )


```

### Apache Cassandra
```python
import pandas as pd
import pandas_nosql

# Read an Apache Cassandra table into a Panda DataFrame
# To Access localhost:
#   * contact_points=['localhost']
#   * contact_points must be a list

df = pd.read_cassandra(
    contact_points = ['localhost'],
    port = 9042,
    keyspace = 'test_keyspace',
    table = 'test_table'
    )

# Append a DataFrame to Apache Cassandra
# DataFrame Columns must match table Columns
replication = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
    }
df.to_cassandra(
    contact_points = ['localhost'],
    port = 9042,
    keyspace = 'test_keyspace',
    table = 'test_table',
    mode = 'w',
    replication = replication
)
```