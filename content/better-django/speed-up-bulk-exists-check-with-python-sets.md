Title: Speed up bulk-exists check with python sets
Date: 2020-08-01 08:00
Category: Better Django

![image]({attach}/images/bulk-exists-check.jpg)

The ```.exists()``` function of Django's ORM is very useful. However, if you need to do this in bulk (think hundreds of thousands or more), this becomes a strain on your database. Let's say you are fetching records from an external system, and if the record doesn't exist locally, you need to do something:

```py
for item in external_records:
    if not Data.objects.filter(external_id=item.id).exists():
        # Do something
```

If you are working with a large quantity of records, this will flood your DB with queries. Instead, you could first pull all `external_id` values from the DB:

```py
existing_ids = Data.objects.all().values_list("external_id", flat=True)
for item in external_records:
    if item.id not in existing_ids:
        # Do something
```

But again, for large volumes of data, this will be slow in terms of computing time. The trick is to use a `set` instead of a `list`. The python `in` operator performs much, much better for sets, since items in sets are guaranteed to be unique. The above code thus becomes:

```py
existing_ids = set(Data.objects.all().values_list("external_id", flat=True))
for item in external_records:
    if item.id not in existing_ids:
        # Do something
```

A very simple change that increases performance dramatically.

(Code above can be found on [GitHub](https://gist.github.com/psyonara/26e9098fc179cc6d4d406d7449fa26e1))
