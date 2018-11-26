Documents
==========

In pyC8, a **document** is a Python dictionary with the following
properties:

* Is JSON serializable.
* May be nested to an arbitrary depth.
* May contain lists.
* Contains the ``_key`` field, which identifies the document uniquely within a
  specific collection.
* Contains the ``_id`` field (also called the *handle*), which identifies the
  document uniquely across all collections within a fabric. This ID is a
  combination of the collection name and the document key using the format
  ``{collection}/{key}`` (see example below).
* Contains the ``_rev`` field. C8 Data Fabric supports MVCC (Multiple Version
  Concurrency Control) and is capable of storing each document in multiple
  revisions. Latest revision of a document is indicated by this field. The
  field is populated by C8 Data Fabric and is not required as input unless you want
  to validate a document against its current revision.

For more information on documents and associated terminologies, refer to
`C8 Data Fabric manual`_. Here is an example of a valid document in "students"
collection:

.. testcode::

    {
        '_id': 'students/bruce',
        '_key': 'bruce',
        '_rev': '_Wm3dzEi--_',
        'first_name': 'Bruce',
        'last_name': 'Wayne',
        'address': {
            'street' : '1007 Mountain Dr.',
            'city': 'Gotham',
            'state': 'NJ'
        },
        'is_rich': True,
        'friends': ['robin', 'gordon']
    }

.. _edge-documents:

**Edge documents (edges)** are similar to standard documents but with two
additional required fields ``_from`` and ``_to``. Values of these fields must
be the handles of "from" and "to" vertex documents linked by the edge document
in question (see :doc:`graph` for details). Edge documents are contained in
:ref:`edge collections <edge-collections>`. Here is an example of a valid edge
document in "friends" edge collection:

.. testcode::

    {
        '_id': 'friends/001',
        '_key': '001',
        '_rev': '_Wm3dyle--_',
        '_from': 'students/john',
        '_to': 'students/jane',
        'closeness': 9.5
    }

Standard documents are managed via collection API wrapper:

### Create and access the collection
```bash
from c8 import C8Client
client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
fabric = client.fabric(tenant='demotenant', name='test', username='root', password='passwd')
students = fabric.collection('students')
lola = {'_key': 'lola', 'GPA': 3.5, 'first': 'Lola', 'last': 'Martin'}
abby = {'_key': 'abby', 'GPA': 3.2, 'first': 'Abby', 'last': 'Page'}
john = {'_key': 'john', 'GPA': 3.6, 'first': 'John', 'last': 'Kim'}
emma = {'_key': 'emma', 'GPA': 4.0, 'first': 'Emma', 'last': 'Park'}
```
You can connect to 'demotenant' and access the 'students' collection.Assuming it is created, you can insert documents as shown.
You can examine the metadata of each document. You can verify that '_id' field will be 'students/lola'.

### Retrieve the total document count in multiple ways.
```bash
$docs = students.count()
or 
$docs = len(students)
```
You can retrieve the document count as shown.

### Insert multiple documents in bulk.
```bash
$students.import_bulk([abby, john, emma])
```
You can insert multiple documents at once in the students collection by passing a list of documents.

### Retrieve one or more matching documents.
```bash
$for student in students.find({'first': 'John'}):
    student_name = student['_key']
    student_gpa = student['GPA']
    student_last = student['last']
```
You can retrieve > 1 documents on any one particular key, say 'first'. 

### Retrieve a document by key.
```bash
$students.get('john')
```
### Retrieve multiple documents by ID, key or body.
```bash
$students.get_many(['abby', 'students/lola', {'_key': 'john'}])
```
You can retrieve multiple documents based on different selection criterias.

### Update a single document.
```bash
lola['GPA'] = 2.6
students.update(lola)
```
You can update individual fields of a document. It must contain the '_id' or '_key' field.

### Delete a document by key.
students.delete('john')

### Delete a document by body with "_id" or "_key" field.
students.delete(emma)
You can delete individual documents. It must contain the '_id' or '_key' field.

### Delete multiple documents. Missing ones are ignored.
students.delete_many([abby, 'john', 'students/lola'])
