---
title: How to Async Generators In NodeJS
summary: How to use the new ES2018 features like async generator functions and for-async-of looping.
date: 2018-04-40
tags: 
  - Javascript
---
*Published originally on [Medium](https://medium.com/@segersian/howto-async-generators-in-nodejs-c7f0851f9c02)*

At the time of writing, [NodeJS v10](https://nodejs.org/en/blog/release/v10.0.0/) was just released in the wild, 
which comes with some neat ES2018 features. 
The new features I am excited to talk about are the `async generator` functions and `for-await-of` loops which complement each other. 
Lots of bling bling, but how does it work? Is there even a valid use case for these things? Let’s find out!

**The Generator Function**

Let’s refresh our memory for a moment here about generator functions. How did that thing, called a generator, work again? I won’t dive too deep, but to give you an idea:

```js
function* sequenceGenerator(maxValue = 2) {
	let currentValue = 0;
	while (currentValue < maxValue) {
		currentValue++;
		yield currentValue;
	}
}
```

A generator function is declared like `function* functionName` , hence, 
the asterisk that comes after the `function` keyword. Such a function can generate multiple return values. You do this by first, calling the generator function, 
this function will return a generator object. 
This generator object can be used to iterate over all the return values. We can do this the explicit way :

```js
const sequence = sequenceGenerator();
console.log(sequence.next()); // Prints : { value: 1, done: false }
console.log(sequence.next()); // Prints : { value: 2, done: false }
console.log(sequence.next()); // Prints : { value: undefined, done: true }
```

Or, we can do it more implicit. As our returned generator object is iterable, we can use the `for-of` loop. 
Notice that the `for-of` loop will return the value itself and not an object, like `sequence.next()` does.

```js
const sequence = sequenceGenerator();
for (const value of sequence) {
	console.log(value)
}
/* prints :
1
2
*/  
```

We can generate multiple values with a generator function. 
This can be useful to generate a number sequence like in the example above. 
A more concrete example would be to generate a [Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number). 
Generator functions were also temporarily [used](https://github.com/tj/co) for mimicking the behaviour of `async functions` when they were not supported yet.

**Then it got asynchronous**

By now,`async` functions and `promises` have become popular concepts in JS. 
An async function allows us to write asynchronous code, in a synchronous fashion. 
An async function is declared by prefixing the `function` keyword with the `async` function.

```js
async function myFunction(){
  const apiResponse = await someFunctionCallingAnAPI()
  console.log(apiResponse)
}
```

Now we’re good to go and we can use the `await` keyword to await any Promise. Don’t forget, any value that a async function returns, *will be wrapped in a promise*.

**Putting it together**

We did a refresher about the `generator` function and the `async` function, what if, 
we want to combine those two? The folks at [TC39](https://github.com/tc39) added this possibility in ES2018, and it was implemented in NodeJS v10.

As you might expect, the definition of a `async generator` goes like this:

```js
async function* myAsyncGenerator(){
  // We can now use the YIELD and AWAIT keywords here
}
```

We’re now able to `yield` and `await` in our function. Let’s take our first example of the sequence generator and make it `async`.

```js

async function* asyncSequenceGenerator(maxValue = 2) {
	let currentValue = 0;
	while (currentValue < maxValue) {
		currentValue++;
		yield currentValue;
	}
}
```

We’ll get back to using the `await` later. First we need to rewrite how we use our generator in the explicit way. 
We need to `await` every `next()` call because an async function returns a promise, 
therefore an `async generator` will return also every time a promise when we ask for the next value.

```js
async function printSequence() {
	const sequence = asyncSequenceGenerator();
	console.log(await sequence.next()); // Prints : { value: 1, done: false }
	console.log(await sequence.next()); // Prints : { value: 2, done: false }
	console.log(await sequence.next()); // Prints : { value: 3, done: false }
}
```

The same for the implicit approach, using the `for-of` loop…

```js
async function printSequence() {
	const sequence = asyncSequenceGenerator();
	// Throws UnhandledPromiseRejectionWarning: TypeError: sequence is not iterable
	for (const value of sequence) {
		console.log(value) 
	}
}
```

… woops! This one throws `TypeError : sequence is not iterable` ! Since we’re not explicitly calling `next()` , 
how are we supposed to await the next value? 
Remember the `for-await-loop` that I mentioned earlier? 
Remember I told you it was complementary to `async generators` ? Behold why:

```js
async function printSequence() {
	const sequence = asyncSequenceGenerator();
	for await (const value of sequence) {
		console.log(value) 
	}
}
```

Because we can iterate over a generator object with a `for-of` loop, it was crucial that, 
if a generator object could return promises, 
we should be able to use the `for-of` loop properly to handle such a use case. 
Therefore, the `for-await-of` loop was born.

The `for-await-of` loop will await every time the next value is requested from our generator. So this `await` will happen before the start of every loop.

**Are there valid use cases for this?**

There definitely are! I have created an example were I use an `async generator` for paging through the Google Books API. 
Paging through the API results that is. 
In the code example I will get from each API request, 
3 books and I page till there are no more items OR I have reached a max page index. 
The max page index is just a safety precaution.

The `getBooksPaged` async generator function encapsulates neatly the paging implementation details that I don’t want to worry about. 
Have a look at the code and notice that you could use the same approach for reading a file, line by line.

```js
// npm i request request-promise-native
const request = require('request-promise-native'); 

searchAndPrintBooks();

async function searchAndPrintBooks() {
	const pages = getBooksPaged({query: 'bitcoin'});
	
	console.log('Searching books about bitcoin...');
	for await(const page of pages) {
		console.log('Page Results : ');
        // e.g. [ { title: 'Bitcoin: Introducción simple' }, { title: 'Bitcoin' }, { title: 'Bitcoins' } ]
		console.log(page) 
	}
}

async function* getBooksPaged({query}) {
	const pageSize = 3;
	const lastPageIndex = 5;
	let currentIndex = 0;
	let isDone = false;
	
	while (currentIndex < lastPageIndex && !isDone) {
		
		const pageResults = await getBooksPage({
			query: query,
			startIndex: currentIndex,
			maxResults: pageSize
		});
		
		yield pageResults;
		
		if (pageResults.length < pageSize) {
			isDone = true
		} else {
			currentIndex++
		}
		
	}
}

async function getBooksPage({query, startIndex, maxResults}) {
	const response = await request({
		method: 'GET',
		url: 'https://www.googleapis.com/books/v1/volumes',
		json: true,
		qs: {
			q: query,
			startIndex: startIndex,
			maxResults: maxResults
		}
	});
	
	const mapEssentialInfo = ({volumeInfo}) => ({title: volumeInfo.title});
	return response.items.map(mapEssentialInfo);
}
```

**Conclusion**

I can definitely see valid use cases where we can put `async generators` to work, like paging an API endpoint, read files, 
handle streams and such. 
Be aware of the `for-await-of` loop which really reduces the boilerplate code else required for iterating over the generator. Worth checking out!