---
title: Error handling with Async/Await in JS
summary: Learn error handling in JS.
date: 2019-04-17
tags: 
  - Javascript
---
*Published originally on [Medium](https://itnext.io/error-handling-with-async-await-in-js-26c3f20bc06a)*


This will be a small article, based on some issues I picked up during code reviews and discussions with other developers. This article is rather focused on the novice JS developers.

## A Simple Try Catch

Let’s start with the simple `try...catch` example.

```js
function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

try {
    thisThrows();
} catch (e) {
    console.error(e);
} finally {
    console.log('We do cleanup here');
}

// Output:
// Error: Thrown from thisThrows()
//   ...stacktrace
// We do cleanup here
```

This works as expected, we call the function `thisThrows()` which throws a regular error, we catch it, log the error and 
optionally we run some code in the `finally` block. No rocket science here.

## A Try Catch with a Rejecting Promise

Now we modify `thisThrows()` so it actually rejects with a promise instead of a regular error. 
For simplicity, I will make the `thisThrows()` function `async`. Remember that an `async` function always **returns** a promise:

* When no return statement defined, or a return statement without a value, it returns a resolving promise, equivalent to `return Promise.Resolve()`.
* When a return statement is defined with a value, it will return a resolving promise with the given return value, equivalent to `return Promise.Resolve("My return String")`
* When an error is thrown, a rejected promised will be returned with the thrown error, equivalent to return `Promise.Reject(error)`.

```js

async function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

try {
    thisThrows();
} catch (e) {
    console.error(e);
} finally {
    console.log('We do cleanup here');
}

// output:
// We do cleanup here
// UnhandledPromiseRejectionWarning: Error: Thrown from thisThrows()
```

Now we have the classic problem, `thisThrows` returns a rejecting promise, so the regular `try...catch` is not able to catch the error. 
As `thisThrows()` is `async` , so when we call it, it dispatches a promise, the code does not wait, so the `finally` block is executed first 
and then the promise executes, which then rejects. So we don’t have any code that handles this rejected promise.

We can handle this in two ways:
* We call `thisThrows()` in an `async` function and `await` the `thisThrows()` function.
* We chain the `thisThrows()` function call with a `.catch()` call.

The first solution would look like this:

```js
async function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

async function run() {
    try {
        await thisThrows();
    } catch (e) {
        console.error(e);
    } finally {
        console.log('We do cleanup here');
    }
}

run();

// Output:
// Error: Thrown from thisThrows()
//   ...stacktrace
// We do cleanup here
```

And the second one:

```js

async function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

thisThrows()
    .catch(console.error)
    .then(() => console.log('We do cleanup here'));

// Output:
// Error: Thrown from thisThrows()
//   ...stacktrace
// We do cleanup here
```

Both solutions work fine, but the` async/await` one is easier to reason about (at least in my personal opinion).

## Caveats

We had a look at simple error handling with and without errors. Let’s have a look now at some special cases.

**Returning from an async function**

Let’s start with a brain teaser, what will happen with the following code?

```js
sync function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

async function myFunctionThatCatches() {
    try {
        return thisThrows();
    } catch (e) {
        console.error(e);
    } finally {
        console.log('We do cleanup here');
    }
    return "Nothing found";
}

async function run() {
    const myValue = await myFunctionThatCatches();
    console.log(myValue);
}

run();
```

At first, we might expect the output to be:

```js
We do cleanup here
Nothing Found
```

But instead, we got a UnhandledPromiseRejection ! But why? Let’s step through the code:

* `thisThrows()` is an `async` method
* We throw an error in `thisThrows()`
* As `thisThrows()` is `async` the thrown error is returned as a rejected promises from the function.
* We return that rejected promised in `myFunctionThatCatches()` with the return statement.
* Our rejected promise reaches the `await` keyword. The await keyword discovers that the Promise is resolved with the status “rejected” and propagates the error as an unhandled promise rejection.

Based on how our code is structured, our error snuck past our `try...catch` block and propagated further down in the call tree. Not good!

We solve this by using the `await` keyword in the return statement.

```js{8}
async function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

async function myFunctionThatCatches() {
    try {
        // Notice we added here the "await" keyword.
        return await thisThrows(); 
    } catch (e) {
        console.error(e);
    } finally {
        console.log('We do cleanup here');
    }
    return "Nothing found";
}

async function run() {
    const myValue = await myFunctionThatCatches();
    console.log(myValue);
}

run();

// Outptut:
// Error: Thrown from thisThrows()
//   ...stacktrace
// We do cleanup here
// Nothing found
```

Now our `try..catch` works as expected. Now the `await` keyword on line 7 will first await the returned promise of 
`thisThrows()` and if that promise rejects, the error will be propagated to the catch `block` on line 8 . Problem solved!

**Resetting your stack trace**

How to handle these use cases will be different on a per-case basis, make sure to be aware of this common mistake and then decide if it’s relevant for you or not.

It’s not uncommon to see code where someone catches an error and wraps it in a new error, like in the following snippet:

```js{2,9}
function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

function myFunctionThatCatches() {
    try {
        return thisThrows();
    } catch (e) {
        throw new TypeError(e.message);
    } finally {
        console.log('We do cleanup here');
    }
}

async function run() {
    try {
        await myFunctionThatCatches();
    } catch (e) {
        console.error(e);
    }
}

run();

// Outputs:
// We do cleanup here
// TypeError: Error: Thrown from thisThrows()
//    at myFunctionThatCatches (/repo/error_stacktrace_1.js:9:15) <-- Error points to our try catch block
//    at run (/repo/error_stacktrace_1.js:17:15)
//    at Object.<anonymous> (/repo/error_stacktrace_1.js:23:1)
```

Notice that our stack trace only starts where we caught the original exception. When we create an error on line `2` and catch it on `9` , we lose 
the original stack trace as we now create a new error of type `TypeError` and only keep the original error message (sometimes we don’t even do that).

Imagine that the `thisThrows()` function has far more logic in it, and somewhere in that function an error is thrown, we won’t see in our logged stack trace the origin of the problem, as we created a new error which will build a brand new stack trace. If we just re-throw our original error, we won’t have that problem:

```js{2}
function thisThrows() {
    throw new Error("Thrown from thisThrows()");
}

function myFunctionThatCatches() {
    try {
        return thisThrows();
    } catch (e) {
        // Maybe do something else here first.
        throw e;
    } finally {
        console.log('We do cleanup here');
    }
}

async function run() {
    try {
        await myFunctionThatCatches();
    } catch (e) {
        console.error(e);
    }
}

run();

// Outputs:
// We do cleanup here
// Error: Thrown from thisThrows()
//     at thisThrows (/repo/error_stacktrace_2.js:2:11) <-- Notice we now point to the origin of the actual error
//     at myFunctionThatCatches (/repo/error_stacktrace_2.js:7:16)
//     at run (/repo/error_stacktrace_2.js:18:15)
//     at Object.<anonymous> (/repo/error_stacktrace_2.js:24:1)
```
Notice that the stack trace now points to the origin of the actual error, being on line `2` from our script.

It is important to be aware of this problem when handling errors. Sometimes this might be desirable, but often this obfuscates the origin of your problem, making it hard to debug the root of a problem. If you create your own custom errors for wrapping errors, make sure you keep track of the original stack trace so that debugging doesn’t turn into a nightmare.

## Summary

* We can use `try...catch` for synchronous code.
* We can use `try...catch` (in combination with `async` functions) and the `.catch()` approaches to handle errors for asynchronous code.
* When returning a promise within a `try` block, make sure to `await` it if you want the `try...catch` block to catch the error.
* Be aware when wrapping errors and rethrowing, that you lose the stack trace with the origin of the error.

