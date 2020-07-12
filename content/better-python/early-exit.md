Title: Early Exit
Date: 2020-07-12 07:46
Category: Better Python

![Photo]({attach}/images/early-exit.jpg)

You will have definitely come across the following pattern often:

```python
if post_data:
    thing = post_data.get("thing")
    if thing is not None:
        setting = get_user_setting(user, thing)
        if setting is not None:
            permission = get_user_permission(user)
            if permission is True:
                if user.is_superuser:
                    return DataPoint.objects.all()
                elif user.is_staff:
                    return DataPoint.objects.filter(user=user)
                else:
                    return DataPoint.objects.filter(user=user, thing=thing)
            else:
                return "Permission denied"
        else:
            return "Setting not found"
    else:
        return "Thing not specified"
else:
    return "No data posted"
```

What is good about the code above? It follows the thought process that most developers would have: which conditions must be met for me to execute the core logic of this feature? So I check each of those conditions and proceed if it is met. Then, in the middle of the code block, I have my core logic bundled up nicely. And at the end I deal with the cases where the conditions were not met.

But are there any downsides?

1. The condition checks are quite disjointed. If you  want to see what happens when a condition is not met, you have to carefully follow the indentation down to where the corresponding `else` is. This is not ideal, but often accepted by a lot of developers.

2. The indentation can become very acute if there are many layers of conditions.

Is there a better way? Yes, there is: the early exit. Instead of following the thought process of "Which conditions must be met?", we rather ask "Which conditions can I eliminate right off the bat?" Here's how we would rewrite the code above:

```python
if not post_data:
    return "No data posted"

thing = post_data.get("thing")
if thing is None:
    return "Thing not specified"

setting = get_user_settig(user, thing)
if setting is None:
    return "Setting not found"

permission = get_user_permission(user)
if permission is False:
    return "Permission denied"

if user.is_superuser:
    return DataPoint.objects.all()

if user.is_staff:
    return DataPoint.objects.filter(user=user)

return DataPoint.objects.filter(user=user, thing=thing)        
```

For each condition that is not met, we return immediately, since no further processing is necessary. And then at the end we have our core logic bundled up again.

This does a few things for us.

1. It still keeps the core logic in one place.

2. The conditions are also bundled up with their corresponding logic.

3. We don't have the indentation problem any more.

4. This may be just me, but I find the refactored code easier to read.

There is one caveat to this pattern: it mostly makes sense if you return something when a conditions is not met. If your application logic needs to *not* return anything, but for example append an error message to a list instead (and then continue), the above might have to be structured differently.

But you'll find tons of places where this pattern is applicable, and if it makes sense in your scenario, go ahead and use it liberally. It's awesome.

(Code above can be found on [Github](https://gist.github.com/psyonara/3cf53bc7f16e71030b5ad190214002d7))
