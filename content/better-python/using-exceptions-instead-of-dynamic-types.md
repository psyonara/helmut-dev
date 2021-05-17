Title: Using Exceptions instead of Dynamic Typing
Date: 2021-05-17 22:00
Category: Better Python

![Photo]({attach}/images/using-exceptions-instead-of-dynamic-types.jpg)

Python's dynamic typing is great, right? You can just do whatever you want with variables. FREEDOM! ;-) This comes at a price though, and sometimes one we're not always aware of.

### Trying not to fail

For years I took advantage of Python's dynamic typing by having functions return an error state via a different data type. For example:

```py
def double(int_input):
    if not isinstance(int_input, int):
        return "An integer must be provided"

    return int_input * 2
```

And consuming this function would have looked like this:

```py
doubled_int = double(user_input)
if isinstance(doubled_int, str):
    print("You did not provide an integer")
    return

print(f"Your doubled value: {doubled_int}")
```

Seems kind of legit. Performance wise there shouldn't be any problems, right?

But what we're ignoring here is maintainability. This is an over-simplified example, but if you have longer functions with multiple return statements, and you're using more than just one data type to signify different things, this can quickly become a problem.

If another developer has to use or modify this function somewhere down the line, it becomes more work to understand what the function is returning in which cases. They will need to read through the function in order to know which return types to expect, and what they mean.

### The Catch

Can we improve on this? Can we make it easier for that developer to use or modify that function? I think there is a way, and that is using exceptions.

Exceptions are a built-in part of Python, and for some reason, over the years, I made a habit of trying to avoid raising of exceptions. But in this case they can serve us pretty well. Our goal is to have a function that has a consistent return data type. And any problems are caught by said exceptions. If we now refactor the function above, we get this:

```py
def double(int_input):
    if not isinstance(int_input, int):
        raise ValueError("An integer must be provided.")

    return int_input * 2
```

Simple, right? Instead of returning a string, we just raise an exception. So far we haven't complicated anything, but the benefit will become apparent in the next step. We are now going to consume this refactored function and catch the exception.

```py
try:
    doubled_int = double(user_input)
    print(f"Your doubled value: {doubled_int}")
except ValueError:
    print("You did not provide an integer")
```

### Finally

So, what exactly happened? We use a try/catch block to catch this new exception that we raised. If everything goes well, our integer is doubled and printed to the screen. However, if we provided a wrong value, the exception is caught and we print an error to the screen.

Have we gained anything? It has come at the cost of an extra line of code, but I think it's clear that we have gained in readability. For any Python developer it is now immediately clear that this function might result in an error, and it's also clear what happens in that case.

Maintainability has also improved. Any future consumer of this function doesn't need to wonder about the different return types that they could/should be expecting. And if the function is modified, one can now just raise other exceptions if new error cases are added. Again, the return type stays consistent.
