Graphs
======

A **graph** consists of vertices and edges. Vertices are stored as documents in vertex collection and edges stored as documents in edge collections.

```bash
$from c8 import C8Client
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$fabric.graphs()
```
This will give you list of graphs present in a database.

### Create a new graph named "school" if it does not already exist.
```bash
$if fabric.has_graph('school'):
    school = fabric.graph('school')
else:
    school = fabric.create_graph('school')
```

### Delete the graph.
```bash
$fabric.delete_graph('school')

```

Edge Definitions
================

An **edge definition** specifies a directed relation in a graph. A graph can
have arbitrary number of edge definitions. Each edge definition consists of the
following components:

* **From Vertex Collections:** contain "from" vertices referencing "to" vertices.
* **To Vertex Collections:** contain "to" vertices referenced by "from" vertices.
* **Edge Collection:** contains edges that link "from" and "to" vertices.

Here is an example body of an edge definition:

.. testcode::

    {
        'edge_collection': 'teach',
        'from_vertex_collections': ['teachers'],
        'to_vertex_collections': ['lectures']
    }

### Create an edge definition named "teach".
```bash
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$if fabric.has_graph('school'):
    school = fabric.graph('school')
else:
    school = fabric.create_graph('school')
     
$if not school.has_edge_definition('teach'):
    teach = school.create_edge_definition(
        edge_collection='teach',
        from_vertex_collections=['teachers'],
        to_vertex_collections=['lectures']
    )
```
This means that you have a edge collection 'teach' which con

### List edge definitions.
```bash
school.edge_definitions()
```

### Delete the edge definition (and its collections).
```bash
school.delete_edge_definition('teach', purge=True)
```


Vertex Collections
==================

A **vertex collection** contains vertex documents, and shares its namespace
with all other types of collections. Each graph can have an arbitrary number of
vertex collections. Vertex collections that are not part of any edge definition
are called **orphan collections**. You can manage vertex documents via standard
collection API wrappers, but using vertex collection API wrappers provides
additional safeguards:

* All modifications are executed in transactions.
* If a vertex is deleted, all connected edges are also automatically deleted.

```bash
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$fabric = client.fabric(tenant='mytenant', name='test', username='root', password='passwd')
$school = fabric.graph('school')
$if school.has_vertex_collection('teachers'):
    teachers = school.vertex_collection('teachers')
else:
    teachers = school.create_vertex_collection('teachers')
```
This returns an API wrapper for "teachers" vertex collection.

### List vertex collections in the graph.
school.vertex_collections()

