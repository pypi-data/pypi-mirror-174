# rocktrie

A trie library based on a single RocksDB database

## Usage

```
>>> import rocksdb
>>> from rocktrie import list_to_trie_db, lookup, ROW_KEY, TERMINAL_KEY, PAYLOAD_KEY
>>> db = rocksdb.DB('/tmp/trie1', rocksdb.Options(create_if_missing=True))
>>> list_to_trie_db([("CAT", 100), ("RAT", 200), ("DOG", 300)], db)
>>> lookup(db, 0, 0, "O")
>>> 
>>> lookup(db, 0, 0, "C")
[0, False, None]
>>> lookup(db, 0, 1, "A")
[0, False, None]
>>> lookup(db, 0, 2, "T")
[0, True, 100]
>>> 
```
