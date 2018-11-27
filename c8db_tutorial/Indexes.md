**Indexes** can be added to collections to speed up document lookups. Every
collection has a primary hash index on ``_key`` field by default. This index
cannot be deleted or modified. Every edge collection has additional indexes
on fields ``_from`` and ``_to``.

### Hashed Indexes
Hashed indexes maintain entries with hashes of the values of the indexed field.

```bash
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$cities = fabric.create_collection('cities')
$index = cities.add_hash_index(fields=['continent', 'country'], unique=True, sparse=True)

```
You create collection called 'cities'. You can add a new hash index on document fields "continent" and "country".
The sparse property of an index if set to True will also include entries for documents that have 'None' in the indexed field. 
If set to False,the index skips documents that do not have the indexed field.
You can combine the sparse index option with the unique index option to reject documents that have duplicate values for a field 
and include documents that do not have entries for the indexed key.

### Fulltext Indexes

```bash
$index = cities.add_fulltext_index(fields=['continent'], min_length=10)
```
We have added new fulltext indexes on fields "continent" and "country". You can specify minimum number of characters to index.

### GeoSpatial Indexes

```bash
$index = cities.add_geo_index(fields=['coordinates'], ordered=False)
```
You can specify a single document field or a list of document fields.The value of the field must be an list with at least two float values. The list must contain the latitude (first value) and the
longitude (second value). All documents, which do not have the field or with value that are not suitable, are ignored.If it is an list with two fields latitude and longitude,
then a geo-spatial index on all documents is created using latitude and longitude as paths the latitude and the longitude. The value of the field latitude and of the field longitude must a
float. All documents, which do not have the fields or which values are not suitable, are ignored. 
If ordered is True, the order is longitude, then latitude.

### List all indexes on a collection
```bash
$indexes = cities.indexes()
```
Retrieve all indexes belonging to 'cities' collection.

### Delete the last index from the collection.
 ```bash
$cities.delete_index(index['id']) 
 ```   
