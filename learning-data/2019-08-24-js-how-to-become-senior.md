---
title: Things To Learn To Become Medior/Senior
summary: Learn more about the core concepts around the JavaScript ecosystem
date: 2019-08-24
tags: 
  - Javascript
---
*Published originally on [Medium](https://itnext.io/javascript-things-newbies-should-know-e04bab10449f)*

**In this article, I’ll be covering some important aspects of JavaScript and its ecosystem that are useful to know for the more medior JavaScript developers should know and understand.**

*I won’t cover any web development topics that are non-JavaScript related.*

## About the JavaScript Language

Like most languages, we have multiple versions of the language. The language, the new features, and future are determined by a technical committee, called [TC-39](https://github.com/tc39).

There are two naming conventions to refer to a JavaScript version. First one is ES6, this is the short version. This implies the arbitrary version (v5, v6, v7, …). Then we have the other naming convention like ES2016, which rather implies the year that the version was published. The ES refers to “EcmaScript”. To give an example:

* ES6 is equal to ES2015
* ES7 is equal to ES2016
* And so on…
* ESNEXT refers to the next upcoming version and related suggestions.

So the language and the version defines the native keywords, features and native methods that are available to you as a developer (simplified definition). My favorite reference regarding JavaScript is [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript).

The philosophy of TC-39 is to make sure that JavaScript is always backward compatible. The language changes based on suggestions that can be made by anyone, if a proposal gains support and maturity it will move from stage-0 (Strawman), stage-1 (proposal), stage-2 (draft), and stage-3 (candidate).

Once a suggestion went through all stages, TC-39 will eventually reject or accept the suggestion and add it to the ECMAScript specification.

Actually, JavaScript is just an implementation of the ECMAScript specification, this means there are other implementations of this specification (e.g. ActionScript, JScript, …) but this article focuses on JavaScript so no need here to go deeper on the subject.

If you work in NodeJS, use [Node.green](https://node.green/) to check out which JavaScript features are supported by the NodeJS version you are using.

## The JavaScript Engine

We know now that we have JavaScript the language, different version and how it evolves over time. But that is just the language itself, we need some application that actually reads, interprets and executes the JavaScript code that we write.

The [JavaScript engine](https://en.wikipedia.org/wiki/JavaScript_engine) is the application that is responsible for that. The engine is the actual place that the JavaScript code comes to life and put in action. The engine also takes care of memory management and garbage collection. There are several JavaScript engines out there in the world:

* [V8](https://v8.dev/): Created by Google
* [SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey): Created by Mozilla
* [JavaScriptCore](https://en.wikipedia.org/wiki/WebKit#JavaScriptCore): Created by Apple
* [Chakra](https://github.com/Microsoft/ChakraCore): Created by Microsoft

So why would you care about JavaScript engines? Well for 2 reasons that I can think of:

* **Version Support**: TC-39 might decide what new features we get into our JavaScript, and you can decide which ES version you want to write your code in, but it’s up to the engine to support this. Therefore, once a new JS feature is introduced, you still need to make sure that the engine it runs on, supports this.
* **Performance**: When we want to talk about performance in JavaScript, we can argue for hours about the “logical” performance (e.g. does my algorithm have an O(1) or O(N) complexity). But it also comes down to how efficient the engine is. The engine can do a lot of magic under the hood to boost performance, even for inefficient code. So the eventual performance can really differ for the same code snippet on different engines. In addition to that, the performance can differ between the different versions of the same engine.

Notice we’ve been talking about the “engine”, not the browser or something like that. The thing is, the browser uses a JavaScript engine for executing JavaScript engine, as it also might use a dedicated engine for rendering the HTML and CSS. A browser does far more than just executing JavaScript (rather offloading it to the JS engine), remember that.

An engine has its own versioning, a new version of an engine might bring performance improvements and/or support for new ES features.

## Client-side and Server-side JavaScript

As you might now, we can run JavaScript in the Browser (e.g. Chrome) or on the server (e.g. NodeJS). Just like in the browser, the server-side javascript is also executed by a JavaScript engine. NodeJS uses V8, the same engine used by Chrome.

## Single and Multi Thread

JavaScript is single-threaded and uses the Event Loop. In the NodeJS docs, you can find a really [deep explanation](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/). This means, only one piece of code can be executed at any given moment. You can have concurrent things happening, but not in parallel. The even loop design enforces this, that you cannot have 2 functions within the event loop executing in parallel.

If you are confused, read about [Concurrency vs Parallelism](https://howtodoinjava.com/java/multi-threading/concurrency-vs-parallelism/).

So yes, JavaScript is strictly a single-threaded language, but does it mean there is no multithreading at all going on? It could be! But that is abstracted away from the entire Event Loop design. When I initiate 5 web requests, read 2 files, and 10 DB queries asynchronously, these IO actions are handed off to the JavaScript engine, which it hands off to the OS. Past this point, the OS can decide (if possible) to use multithreading. This is something that you as a JavaScript developer should not care about, that’s outside your scope, you don’t have any control over it, and you shouldn’t care about it either.

So simply put, your JavaScript code itself, is single-threaded and IO is one big black box you don’t care about.

## WEB APIs

You might have used in your past, Web APIs like “[GeoLocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation)”, “[Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)”, “[Gamepad](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API)”, or more likely “[Document](https://developer.mozilla.org/en-US/docs/Web/API/Document)”. These are APIs which are an interface to your browser. Your **browser**, let that sink in for a moment. The browser is responsible to make sure that those APIs exist in your global scope.

When you do something like `document.getElementById()` , the browser made that `document` object and `getElementById()` method available to you, because you are interacting with parts of the web page or the browser (e.g. when you use `navigation.userAgent` ). The browser is also responsible for the implementation.

The reason I point this out is, these are [WEB API’s](https://developer.mozilla.org/en-US/docs/Web/API). Meaning, these APIs are only available when your JavaScript code is executed, in the browser, not on the server like with NodeJs. This might be obvious to many developers, but for the novice JS developer, this is a very important difference. This is why the `document` object does not exist when you execute your code in NodeJS, because the code is not executed in a browser.

Some of the WEB APIs though are **mimicked** in NodeJS, a good example for that is the `console.log()` API. But the implementation is very different, in the browser `console.log()` will print to your developer console, in NodeJS this would print to `stdout` by default.

So when you see something coming out of thin air, like `console.log()` or `document.getElementById()` while you did not explicitly import these objects or methods (e.g. `import console from 'console'` or `const console = require('console')` ) your working most likely with an API that was included by the runtime environment, being the browser or NodeJS. This is not done by the engine.

**Note**: *The engine itself can (but it’s rare) also introduce some APIs itself, an example is `Error.captureStackTrace` by [V8](https://v8.dev/docs/stack-trace-api#stack-trace-collection-for-custom-exceptions). Goes without a saying, that this function will not exist when you run this in another JavaScript engine.*

## Transpiling

We know that there are multiple JavaScript version, multiple browsers, multiple JavaScript engines having also their own versions. What a sh*tstorm to deal with when you just want to write JavaScript.

When working in NodeJS, your environment is fairly static. You decided which NodeJS version is running, which also defines which type and version of the engine that you are using. Do you want to use a newer JavaScript version? Upgrade your NodeJs version, no harm done (aside of a [few possible issues](https://nodejs.org/en/docs/guides/buffer-constructor-deprecation/)). What I mean is, you don’t need to care about anything else than one contained environment.

This dream scenario does not exist in the browser. All your users can be using a different browser (and different versions), which have different JavaScript engines (and again their different versions).

Easy would be to tell all your users to upgrade to the latest browser version but not everyone has the know-how to do so or permissions (corporate restrictions). So how to use a new JavaScript version, while not breaking your web application? Transpiling!

Transpiling is usually defined as “porting the source code from one high order language to source code in another high order language”. For the browser, we do pretty much the same, but instead we “port the source code in a newer JavaScript version to an older version of JavaScript”.

As most browsers do support ES5 as it’s so old, the community came up with this concept by translating your ES7 JavaScript code to ES5 compatible code. You write your code in ES7, you transpile it, and you use the transpiled ES5 version of your application to serve to all of your users. Nifty right?

The most common “transpiler” for JavaScript is [Babel](https://babeljs.io/). They have an online tool where you can [see the transpiled version](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=IYZwngdgxgBAZgV2gFwJYHsIwBYFMA2-6A6ugE74AmAFAJQDeAUDDFJiOvrgHREDm1AOQAJAkRikKlQbQDcjAL5A&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2017&prettier=false&targets=&version=7.5.5&externalPlugins=) of any code you type.

If you want to check more what browser supports what, and not only JavaScript, but also CSS and HTML. Check out [caniuse.com](https://caniuse.com/).

## Edit: iOS 3rd party browsers all need to use WebKit.

Did you know that any browser on iOS can’t use their own JavaScript engine? They need to use the one from WebKit, due to Apple regulations. On top of that, these 3rd party browsers are not allowed to use the “fast” JavaScript engine that WebKit provides. So to make it more annoying, the Google Chrome on your Desktop (Windows, Linux, Mac) will use the V8 JavaScript engine, but not on iPhone/iPad (iOS).

You can find more on that [here](https://www.howtogeek.com/184283/why-third-party-browsers-will-always-be-inferior-to-safari-on-iphone-and-ipad/) and [here](https://www.quora.com/Are-all-web-browsers-on-iOS-required-to-use-the-WebKit-kernel).
