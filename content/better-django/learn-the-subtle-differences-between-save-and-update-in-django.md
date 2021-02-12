Title: Learn the subtle differences between Save and Update in Django
Date: 2021-02-12 07:10
Category: Better Django

To save data in Django, you normally use [.save()]([Model instance reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/instances/#saving-objects)) on a model instance. However the ORM also provides a [.update()]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#update)) method on queryset objects. So which one should you use? Let's take a look at each, and then decide which one to use in which situations.

### Save

The `.save()` method is used to write a model instance to the database. It can be an existing record or even a new one. For an existing record, Django will run a SQL UPDATE  statement on the database. For a new record, Django will run an INSERT. [Before Django 3.0]([Model instance reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/instances/#how-django-knows-to-update-vs-insert)), it would also do a SELECT before the INSERT, to make sure that the primary key doesn't exist (if one was given), and do an UPDATE instead if it found something.

Examples:

```python
new_book = Book(title="How to code", author="Mike Lambda", price=9)
new_book.save()

book = Book.objects.get(title="Debugging like a pro")
book.price += 5
book.save()
```

When updating an existing record, Django will update every field. That means, if you changed only one field on the model instance (like the price in the example above), all the fields will be updated (with the values staying the same). This is rather inefficient, right? Especially if you model has many, many fields. And there's another problem. If there's a significant amount of time in between the fetching of the record and the saving of it, it is possible that another request will have updated one of the fields on that record, and your model instance still has the old value. If you call `.save()` now, it will overwrite the new value that someone else saved. These two problems can be prevented by using the [update_fields]([Model instance reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/instances/#specifying-which-fields-to-save)) parameter. It expects a list of fields (as strings) that you want to save. So if you have only a few fields to save, use this parameter to prevent such data overwrite problems. The UPDATE that is run against the database then only updates those fields that you have specified.

In the example above, it would change to:

```python
book.save(update_fields=["price"])
```

#### When to use Save

- You are creating a new record (an alternative is using the [.create()]([QuerySet API reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#create)) method).

- You have a model instance already, and you need to change some field values.

- You've overridden the `save` method to include some custom model logic.

- You've defined [pre_save]([Signals | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/signals/#pre-save)) and [post_save]([Signals | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/signals/#post-save)) signals for that model.

- The changes you need to make are dynamic, based on current field values (e.g. incrementing a value - see the example above).

- You want to update fields from a related model (like a [ForeignKey]([Model field reference | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/fields/#foreignkey))).

### Update

The `.update()` method is available on each queryset object of the ORM. Using it will typically look like this:

```python
Book.objects.filter(price__lt=10).update(price=10)
```

This would update the price of all books that are below a certain price. While this is for a range of records, it could also be used as in our first example, to update a single record:

```python
Book.objects.filter(title="Debugging like a pro").update(price=15)
```

You'll notice that this doesn't increment the price like it does in the first `save` example. You would need to use an [F expression]([Query Expressions | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/models/expressions/#f-expressions)) for that, but that's beyond the scope for now.

`Update` cannot be used to create a new record, like `save` can.

#### When to use Update

- You are updating fields of one or many records

- You don't need to re-use a model instance after updating

- You don't need your overridden `save` method or any `pre_save` or `post_save` signals to run

- You know what your new field values must be without having retrieved the record(s)

### Summary

If you need to update field values, without any other model logic needing to be run, and you know what the changes will be without fetching the record(s) first, use `update`. The SQL that is run against the database will be more efficient. However, if you need to, or have already, loaded the record from the database, and you possibly need the change to be dynamic based on existing data, or there's attached model logic that needs to run, use `save`.

I hope this has been helpful to you. If you have any questions or comments, please don't hesitate to reach out to me. I'd be glad to have a chat.
