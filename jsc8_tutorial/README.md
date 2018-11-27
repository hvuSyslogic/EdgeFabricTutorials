jsc8 tutorial
=============

This is a short tutorial to get started with jsc8.

### Install the JavaScript driver

```js
npm install jsc8
```

If you want to use the driver outside of the current directory, you can also install it globally using the --global  flag:

```js
npm install --global jsc8
```

### Getting a handle
In order to do anything useful we need a handle to an existing C8 database.
Let’s do this by creating a new instance of Database using a connection string:

```js
fabric = new Fabric("https://default.dev.macrometa.io");
```

This connection string actually represents the default values, so you can just omit it:

```js
fabric = new Fabric();
```

If that’s still too verbose for you, you can invoke the driver directly:

```js
fabric = require('jsc8')();
```
The outcome of any of the three calls should be identical.

### Creating a fabric

We don’t want to mess with any existing data, so let’s start by creating a new fabric called “myfabric”:

```js
await fabric.createFabric("myfabric", [{ username: 'root' }], { dcList: "fabric1.ops.aws.macrometa.io", realTime: true });
```
Because we’re trying to actually do something on the server, this action is asynchronous. All asynchronous methods in the C8 driver return promises but you can also pass a node-style callback instead.

Keep in mind that the new fabric you’ve created is only available once the callback is called or the promise is resolved.

### Switching to the new fabric

We’ve created a new fabric, but we haven’t yet told the driver it should start using it. Let’s change that:

```js
fabric.useFabric("myfabric");
```

You’ll notice this method is executed immediately.
The handle “fabric” now references the “myfabric” database instead of the (default) “_system” database it referenced before.

### Creating a tenant

```js
const guestTenant = fabric.tenant("mytenant");
await guestTenant.createTenant("my-password");
```

Here a tenant named "mytenant" will be created with password as "my-password". As in the case for creating a fabric, this call is also asynchronous.

### Switching to the new tenant

We’ve created a new tenant, but we haven’t yet told the driver it should start using it. Let’s change that:

```js
fabric.useTenant("mytenant");
```
Again like in fabric, this will be executed immediately.
The handle "fabric" now references the "mytenant" tenant instead of the (default) "_mm" tenant it referenced before.

### Another handle

Collections are where you keep your actual data.
There are actually two types of collections but for now we only need one.

Like databases, you need a handle before you can do anything to it:
```js
collection = fabric.collection('firstCollection');
```
Again notice that it executes immediately.
Unlike databases, the collection doesn’t have to already exist before we can create the handle.

### Creating a collection
We have a handle but in order to put actual data in the collection we need to create it:

```js
await collection.create();
```

### Creating a document
What good is a collection without any collectibles? Let’s start out by defining a piece of data we want to store:

```js
doc = {
  _key: 'employees',
  firstname: 'Bruce',
  lastname: 'Wayne'
};
```
Collection entries (called documents in C8) are plain JavaScript objects and can contain anything you could store in a JSON string.
You may be wondering about the `_key` property: some property names that start with underscores are special in C8 and the key is used to identify the document later.
If you don’t specify a key yourself, C8 will generate one for you.

### Saving and updating the document

C8 also adds a `_rev` property which changes every time the document is written to, and an `_id` which consists of the collection name and document key.
These “meta” properties are returned every time you create, update, replace or fetch a document directly.

Let’s see this in action by fist saving the document:

```js
await collection.save(doc);
```
… and then updating it in place:

```js
await collection.update('employees', { email: 'wayne@gmail.com' });
```

### Removing the document

We’ve played around enough with this document, so let’s get rid of it:

```js
try {
    await collection.remove('employees');
} catch (e) {
    console.log(e);
}
```
Once the promise has resolved, the document has ceased to exist.
We can verify this by trying to fetch it again (which should result in an error).

If you see the error message `"document not found"`, we were successful.

### C8QL Queries
```js
const cursor = await fabric.query(c8ql`FOR employee IN employees RETURN employee`);
const result = await cursor.next();
```

> Note that most queries return a cursor object representing the result set instead of returning an array of all of the results directly.

This helps avoiding unnecessarily cluttering up memory when working with very large result sets.

All interactions with the cursor object are asynchronous as the driver will automatically fetch additional data from the server as necessary.
Keep in mind that unlike arrays, cursors are depleted when you use them.
They’re single-use items, not permanent data structures.

### Template strings

When writing complex queries you don’t want to have to hardcode everything in a giant string.
The driver provides the same c8qlQuery template handler you can also use within C8 itself:

```js
c8ql = require('jsc8').c8ql;
```

You can use it to write c8ql templates.
Any variables referenced in c8ql templates will be added to the query’s bind values automatically.
It even knows how to treat collection handles.

```js
const cursor = await fabric.query(c8ql`FOR employee IN employees RETURN employee`);
const result = await cursor.next();
```

### Removing all the documents

Enough fooling around. Let’s end with a clean slate.
The method for completely emptying a collection is called “truncate”:

```js
try {
    await collection.truncate();
} catch (e) {
    console.log(e);
}
```
When you truncate a collection, you discard all of its contents.
There’s no way back.

Keep in mind that you can also truncate databases.
Don’t worry about your collections though, truncating only deletes the documents.
Although it’s still probably not something you want to take lightly.
