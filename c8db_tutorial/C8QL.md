C8QL Queries
===========

C8QL queries are invoked from C8QL API wrapper. Executing queries returns cursors.**C8 Data Fabric Query Language (C8QL)** is used to read and write data. It is similar
to SQL for relational fabrics, but without the support for data definition operations such as creating or deleting fabrics, collections or indexes.
```bash
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$fabric.collection('students').insert_many([
    {'_key': 'Abby', 'age': 22},
    {'_key': 'John', 'age': 18},
    {'_key': 'Mary', 'age': 21}
])
$c8ql = fabric.c8ql
$c8ql.explain('FOR doc IN students RETURN doc')
```
You can understand the query better using 'explain'.'explain' inspects the query and return its metadata 
without executing it.

### Validate the query without executing it.
```bash
$c8ql.validate('FOR doc IN students RETURN doc')
```
You can validate the query. It ensures the correctness of query without executing it.

### Execute the query
```bash
cursor = fabric.c8ql.execute(
  'FOR doc IN students FILTER doc.age < @value RETURN doc',
  bind_vars={'value': 19}
)
result = [doc['_key'] for doc in cursor]

```
Cursors fetch query results from C8Db server in batches. Cursor objects are stateful as they store the fetched items in-memory. 

### List currently running queries.
c8ql.queries()

### List slow queries
c8ql.slow_queries()

### Clear slow C8QL queries if any.
c8ql.clear_slow_queries()