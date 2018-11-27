**Indexes** can be added to collections to speed up document lookups. Every
collection has a primary hash index on ``_key`` field by default. This index
cannot be deleted or modified. Every edge collection has additional indexes
on fields ``_from`` and ``_to``.

```bash
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$cities = fabric.create_collection('cities')
$index = cities.add_hash_index(fields=['continent', 'country'], unique=True)

```
You create collection called 'cities'. You can add a new hash index on document fields "continent" and "country".

```bash
$indexes = cities.indexes()
```
Retrieve all indexes belonging to 'cities' collection.

### Delete the last index from the collection.
 ```bash
$cities.delete_index(index['id']) 
 ```   
