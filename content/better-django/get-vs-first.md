Title: Understanding the difference between .get and .first in Django
Date: 2021-05-21 07:30
Category: Better Django

![Photo]({attach}/images/get-vs-first.jpg)

When retrieving a single record in Django, the ORM offers two possible methods: `.get()` and `.first()`. Let's learn how each one works and when to use them.

#### Get

Django's most basic way to retrieve a single record is [the .get() method]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get)). It is used as follows:

```py
burger = Menu.objects.get(name="Beef Burger")
```

Quick facts about `.get()`:

- It retrieves only one record.

- If no record exists that meets the given criteria, it raises a `DoesNotExist` exception.

- If more than one record with the given criteria exists, it raises a `MultipleObjectsReturned` exception.

### First

A different way to get one record is to use [.first()]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first)) on a QuerySet. For example:

```py
burger = Menu.objects.filter(name="Beef Burger").first()
```

Quick facts about `.first()`:

* It will return the first item of a recordset.

* If no record exists, it returns `None`.

### Handling unexpected situations

#### Get

If Django's ORM can't return one record (i.e. there is either no record, or there are more than one), you have to catch the relevant exception. For example:

```py
try:
    return Menu.objects.get(name="Beef Burger")
except Menu.DoesNotExist:
    raise Exception("Could not find a burger")
except Menu.MultipleObjectsReturned:
    raise Exception("Found too many burgers")
```

#### First

When using `.first()`, the only unexpected situation is if no record was present in the QuerySet. Since it's not a problem if multiple records exist that meet the criteria, we have to deal only with the one case. For example:

```py
burger = Menu.objects.filter(name="Beef Burger").first()
if not burger:
    raise Exception("Could not find a burger")

return burger
```

### Subtle differences

Did you notice the differences between the two above? For `.get()` we have to deal with more "error" scenarios. But why is that? The `.get()` method expects no more and no less than one record to be returned, whereas `.first()` assumes there might be multiple records, and it returns the first. So we have a fundamental difference in the assumptions each of these makes.

Should we care? Does it really make a difference which of the two methods we use if we get the same result?

I used to think it didn't matter, but I was wrong.

1. Using `.get()` might point to a problem with our Model that we are unaware of. If we are expecting only one record to be returned, but we get back multiple, we have failed to make sure that one of the fields (or multiple ones) enforce a [unique constraint]([Model field reference | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.unique)). Handling this at a database layer is crucial. If we had used `.first()`, and had not added a unique constraint, we might have never noticed if there were multiple records where we are expecting only one.

2. What about readability? I never thought about how the code reads in each case, and what it tells the reader about the data models. When you use `.get()`, the reader will (or should) know immediately that the record should be unique for the fields you filtered on. However, if you use `.first()`, it implies to the reader that multiple records might exist, but you only care about the first one.

### When to use which

#### Get

Use `.get()` when you are expecting only one (or a maximum of one) record to be returned. The code makes your intentions clear, and there's less room for undetected errors.

#### First

Use `.first()` when you know there might be multiple records (and that's ok), but you only care about the first. In most cases you should also have some [order]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by)) defined [on the model]([Model Meta options | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering)) (or specified [on your query]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by))), otherwise the first record might be random. In some cases you might not even care about the order, but just be aware of it. 

### Gotchas

* If you use `.first()`, you run the risk of using the `None` (in the case of no record found) as a different return data type to signify the fact that nothing was found. It's not very likely, but I've caught myself doing this. I wrote about that trap [here](https://www.helmut.dev/using-exceptions-instead-of-dynamic-typing.html).

* The SQL query generated by `.get()` does not have a limit. So if you have multiple records, before the `MultipleObjectsReturned` exception is raised, your database will return all the records matching that criteria. But using `.first()` adds a `LIMIT 1` to your query, so it will only ever return one record. Be careful which one you choose.

### Summary

If you query the database and only ever expect one record (maximum) to be returned, don't use `.first()`, but rather `.get()` instead. You'll thank yourself later.
