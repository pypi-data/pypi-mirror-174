# NoSQL Storage Wrapper
A simple library for easy work with key-value storages and document databases


## Instalation
```bash
pip install nosql-storage-wrapper
```


## Work with MongoDB

By default work asynchrous version
```py
from nosql_storage_wrapper.mongo import Storage

```

For synchrous version use this code:
```py
from nosql_storage_wrapper.mongo.sync import Storage

```

## Configuring
This library requires the MagicConfig library to work.
```bash
pip install magic-config
```

Configuring with .env file:
```
MONGO_HOST="127.0.0.1"
MONGO_USER="user"
MONGO_PWD="******"
MONGO_DB="basename"
MONGO_PORT=27017
```

## Using
For example some code in aiogram

```py
from nosql_storage_wrapper.mongo import Storage

async some_foo():
  await Storage("aiogram_state").delete_one({"chat": Config.DEBUG_USER_ID})

```
