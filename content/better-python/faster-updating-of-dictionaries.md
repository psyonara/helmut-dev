Title: Faster updating of dictionaries
Date: 2020-07-09 17:18
Category: Better Python

When updating a dictionary, no one would object to this:

```py
ages["Pete"] = 42
```

But what about this?

```py
ages["Tom"] = 29
ages["Linda"] = 37
ages["Pam"] = 62
ages["Coraline"] = 21
```

Still fine, right? There is another way of writing this, using the `.update()` method.

```py
ages.update(
    {
        "Tom": 29,
        "Linda": 37,
        "Pam": 62,
        "Coraline": 21,
    }
)
```

Which one do you prefer? Would you say it's a matter of preference? I always preferred using the `.update()` method when there were at least 3 updates being done. But one day I wondered about the performance of each method. Let's see if one is slower than the other.

Using Python's `timeit`, we run the following code to test our first method. This updates the dictionary three times.

```py
ages = {}; ages["Tom"] = 29; ages["Linda"] = 37; ages["Pam"] = 62
```

Then, using the same method, we test `.update()`.

```py
ages = {}; ages.update({"Tom": 29, "Linda": 37, "Pam": 62})
```

The results?

Straight assignment: *225 nsec per loop*

Using `.update()`: *522 nsec per loop*

And the pattern stays linear with more keys.

So we see that straight assignment is about twice as fast. Does that mean we never use `.update()`? No. Like so many other things, it depends on your specific case.

#### The Case for Assignment

If you're updating a few keys, and your new data is not already gathered in a second dictionary, it probably makes sense to just use normal assignment.

#### The Case for Update

If you've got new data in a second dictionary (either a few items or many), and you'd like to update the first dictionary with these items, I would use the `.update()` method. It makes for cleaner code.
