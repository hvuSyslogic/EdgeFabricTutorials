# How to do Joins in C8QL?

## Problem 

I want to join documents from different collections in a C8QL query.
- One-to-Many: I have a collection users and a collection cities. Now, A user lives in a city and I need the city information during the query.
- Many-To-Many: I have a collection authors and books. An author can write many books and a book can have many authors. I want to return a list of books with their authors. 

## Solution

C8DB support joins in C8QL queries. If one has familiarity with joins with traditional relational databases, understanding this will be easy. However, the documents have more flexibility hence joins are also more flexible. The following sections provide solutions for common questions.

### One-To-Many

You have a collection called **users**. Users live in city and a city is identified by its primary key. In principle you can embedded the city document into the users document and be happy with it.

```js
{
    "_id" : "users/2151975421",
    "_key" : "2151975421",
    "_rev" : "2151975421",
    "name" : {
        "first" : "John",
        "last" : "Doe"
        },
    "city" : {
        "name" : "Metropolis"
        } 
}
```

This works well for many use cases. Now assume, that you have additional information about the city, like the number of people living in it. It would be impractical to change each and every user document if this numbers changes. Therefore it is good idea to hold the city information in a separate collection.

A document from **cities** will look something like this -

```js
{
    "population" : 1000,
    "name" : "Metropolis",
    "_id" : "cities/2241300989",
    "_rev" : "2241300989",
    "_key" : "2241300989"
}
```

Now you instead of embedding the city directly in the user document, you can use the key of the city. A document from **users** collection will look something like the following -

```js
{
    "name" : {
        "first" : "John",
        "last" : "Doe"
        },
    "city" : "cities/2241300989",
    "_id" : "users/2290649597",
    "_rev" : "2290649597",
    "_key" : "2290649597" 
}
```
We can now join these two collections very easily.

```js
FOR u IN users
    FOR c IN cities
        FILTER u.city == c._id 
        RETURN { user: u, city: c }
```

Result will be something like this - 

```js
[
    {
        "user" : {
            "name" : {
                "first" : "John",
                "last" : "Doe"
                },
            "city" : "cities/2241300989",
            "_id" : "users/2290649597",
            "_rev" : "2290649597",
            "_key" : "2290649597"
            },
        "city" : {
            "population" : 1000, 
      		"name" : "Metropolis", 
      		"_id" : "cities/2241300989", 
      		"_rev" : "2241300989", 
      		"_key" : "2241300989"
            } 
  	}
]
```

Unlike SQL there is no special JOIN keyword. The optimizer ensures that the primary index is used in the above query.

However, very often it is much more convenient for the client of the query if a single document would be returned, where the city information is embedded in the user document - as in the simple example above. With C8QL there you do not need to forgo this simplification.

```js
FOR u IN users
    FOR c IN cities
        FILTER u.city == c._id 
        RETURN merge(u, {city: c})
```

Result - 

```js
[
    {
        "_id" : "users/2290649597",
        "_key" : "2290649597",
        "_rev" : "2290649597",
        "name" : {
            "first" : "John",
            "last" : "Doe"
            },
        "city" : {
            "_id" : "cities/2241300989",
            "_key" : "2241300989",
            "_rev" : "2241300989",
            "population" : 1000,
            "name" : "Metropolis”
        } 
  	} 
]
```
So you can have both: the convenient representation of the result for your client and the flexibility of joins for your data model.

### Many-To-Many

In the relational word you need a third table to model the many-to-many relation. In C8DB you have a choice depending on the information you are going to store and the type of questions you are going to ask.

Assume that authors are stored in one collection and books in a second. If all you need is "which are the authors of a book" then you can easily model this as a list attribute in users.

If you want to store more information, for example which author wrote which page in a conference proceeding, or if you also want to know "which books were written by which author", you can use edge collections. This is very similar to the "join table" from the relational world.

#### Embedded Lists

If you only want to store the authors of a book, you can embed them as list in the book document. There is no need for a separate collection.

```js
[
    {
        "_id" : "authors/2661190141", 
        "_key" : "2661190141", 
        "_rev" : "2661190141", 
        "name" : { 
            "first" : "Maxima", 
            "last" : "Musterfrau" 
        } 
  	}, 
  	{ 
        "_id" : "authors/2658437629", 
        "_key" : "2658437629", 
        "_rev" : "2658437629", 
        "name" : { 
            "first" : "John", 
            "last" : "Doe" 
        } 
  	} 
]
```

You can query books. 

```js
FOR b IN books
RETURN b
```

Result - 

```js
[
    {
        "_id" : "books/2681506301", 
        "_key" : "2681506301", 
        "_rev" : "2681506301", 
        "title" : "The beauty of JOINS", 
        "authors" : [ 
            "authors/2661190141", 
            "authors/2658437629" 
        ] 
  	} 
]
```

and join the authors in a very similar manner given in the one-to-many section.
 
```js
FOR b IN books 
    LET a = (FOR x IN b.authors FOR a IN authors FILTER x == a._id RETURN a) 
    RETURN { book: b, authors: a }
```

Result - 

```js
[
    { 
        "book" : { 
        "title" : "The beauty of JOINS", 
        "authors" : [ 
            "authors/2661190141", 
            "authors/2658437629" 
        ], 
        "_id" : "books/2681506301", 
        "_rev" : "2681506301", 
        "_key" : "2681506301" 
    	}, 
    	"authors" : [
            {
                "name" : {
                    "first" : "Maxima",
                    "last" : "Musterfrau" 
        		}, 
                "_id" : "authors/2661190141", 
                "_rev" : "2661190141", 
                "_key" : "2661190141" 
            },
            {
                "name" : {
                    "first" : "John",
                    "last" : "Doe" 
        		}, 
                "_id" : "authors/2658437629", 
                "_rev" : "2658437629", 
                "_key" : "2658437629"
            } 
    	]
    } 
]
```

or embed the authors directly

```js
FOR b IN books 
    LET a = ( FOR x IN b.authors FOR a IN authors FILTER x == a._id RETURN a)
    RETURN merge(b, { authors: a })
```

Result - 

```js
[
    {
        "_id" : "books/2681506301",
        "_key" : "2681506301",
        "_rev" : "2681506301",
        "title" : "The beauty of JOINS",
        "authors" : [
            {
                "_id" : "authors/2661190141",
                "_key" : "2661190141",
                "_rev" : "2661190141",
                "name" : {
                    "first" : "Maxima",
                    "last" : "Musterfrau"
                    }
            },
            {
                "_id" : "authors/2658437629",
                "_key" : "2658437629",
                "_rev" : "2658437629",
                "name" : {
                    "first" : "John",
                    "last" : "Doe"
                    }
            }
        ]
    } 
]
```

#### Using Edge Collections

If you also want to query which books are written by a given author, embedding authors in the book document is possible, but it is more efficient to use a edge collections for speed.
Or you are publishing a proceeding, then you want to store the pages the author has written as well. This information can be stored in the edge document.

First create the authors collection and books collection(without any author information).

An edge collection is now used to link authors and books. 

```js
LET e = [{
    "_from": "authors/2935261693",
    "_to": "books/2980088317",
    "pages": "1-10"
}]
FOR txn in e
    INSERT txn in written
```

In order to get all books with their authors you can use a graph traversal, for example - 

```js
FOR b IN books 
    LET authorsByBook = (FOR author, writtenBy IN INBOUND b written 
                            RETURN {vertex: author, edge: writtenBy })
    RETURN { book: b, authors: authorsByBook }
```

You can do various other graph queries like bfs etc. 
