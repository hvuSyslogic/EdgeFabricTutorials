PyC8 tutorial
============

This is an introduction to C8's Python driver PyC8, a Python driver for the Digital Edge Fabric.

This allows you to operate on and administer C8 tenants and fabrics from within your applications.

### Build & Install

To build,

```bash
 $ python setup.py build
```
To install locally,

```bash
 $ python setup.py build
```
Once the installation process is finished, you can begin developing C8 database application in Python.

### Usage
In order to operate on C8 database entities from within your application, you need to establish a connection to a particular region(server) then use it to open or create any resource on that server.

PyC8 manages server connections through the conveniently named C8Client class.

```bash
 $ from c8 import C8Client
 $ client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
 
```
When this code executes, it initializes the server connection to the region URL you sepcified. 

### Pre-requisite

Let's assume your tenant name is `demotenant` and `root` usern password is `demopwd`.

### Connecting and Creating Fabrics

```bash
$demotenant = client.tenant(name='demotenant', fabricname='_system', username='root', password='demopwd')

$if not demotenant.has_user('demouser'):
    demotenant.create_user(username='demouser', password='demouserpwd', active=True)

$if not demotenant.has_fabric('demofabric'):
    demotenant.create_fabric(name='demofabric', dclist=demotenant.dclist(), realtime=True)

$demotenant.update_permission(username='demouser', permission='rw', fabric='demofabric')
```
You can now connect to the default sys_tenant and attempt to create a user `demouser` having password `demouserpwd`.

You can then create fabric called `demofabric` by passing a parameter called dclist. A call to dclist returns a list of all Edge Locations (AKA Datacenters) deployed in the Macrometa Fabric.

The fabric `demofabric` is created in all the regions specified in the dclist. You can assign `rw` permissions over `demofabric` to `demouser`.

You need to check existence for both `has_user(demouser)` and `has_fabric(demofabric)` to ensure we do not create duplicate resources.

### Create and populate Collections

```bash
$fabric = client.fabric(tenant='demotenant', name='demofabric', username='demouser', password='demouserpwd')
$employees = fabric.create_collection('employees') # Create a new collection named "employees".
$employees.add_hash_index(fields=['email'], unique=True) # Add a hash index to the collection.

$employees.insert({'firstname': 'Jean', 'lastname':'Picard', 'email':'jean.picard@macrometa.io'})
$employees.insert({'firstname': 'James', 'lastname':'Kirk', 'email':'james.kirk@macrometa.io'})
$employees.insert({'firstname': 'Han', 'lastname':'Solo', 'email':'han.solo@macrometa.io'})
$employees.insert({'firstname': 'Bruce', 'lastname':'Wayne', 'email':'bruce.wayne@macrometa.io'})
```

You can create collection in a fabric. In the above example, first you connect to `demotenant`,`demofabric` having `demouser` and `demouserpwd`.

You can then create a collection called `employees`. We add hash_index called `emails` to our collection `employees`. You can then insert 4 documents in the employees collection.

### Query to retrieve documents using C8QL

```bash
$fabric = client.fabric(tenant="demotenant", name="demofabric", username="demouser", password='poweruser')
$cursor = fabric.c8ql.execute('FOR employee IN employees RETURN employee') # Execute a C8QL query
$docs = [document for document in cursor]
```
You can execute C8QL query on our newly created collection `employees`. C8QL is C8's query language. This aforementioned query is equivalent to SQL's SELECT query.

### Delete tenant

```bash
$sys_tenant.delete_tenant(demo_tenant)

```
We deleted our `demotenant` using sys_tenant admin privileges.


Chapters
--------

- [Documents](Documents.md)
- [Graphs](Graphs.md)
- [C8QL](C8QL.md)
- [Indexes](Indexes.md)
- [Streams](Streams.md)
