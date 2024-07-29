---
title: Why you should stop using env variables for NPM modules
summary: Clean code your modules.
date: 2019-01-01
tags: 
  - Javascript
  - NPM
---
*Published originally on [Medium](https://medium.com/@segersian/why-you-should-stop-using-env-variables-for-npm-modules-8bf68717d81d)*

Recently I was reading through the readme of an NPM module on GitHub. As I was skimming through the configuration chapter, a big table of about 14 environment variables caught my attention. Holy *****!

Now, the number of environment variables was (fairly) extensive for a simple NPM module, although it’s not unusual to have an extensive configuration for a module/library, why even use environment variables at all?

**Why Not?**

Let’s have first a look at the call site of a fictional NPM module `custom-logger` which is a simple `express` middleware used to log requests.

```js
const logger = require('custom-logger');

app.use(logger({ level : 'info' }));
```

On the server bootstrap phase, we configure the `custom-logger` with a log level of `info`. 
Cool, now we’re ready to run our express server. We have a clear configuration of the `custom-logger`. It’s predictable and clear.

One day, we decide to configure the `level` of the `custom-logger` . Let’s say we still have the same call site:

```js
const logger = require('custom-logger');

app.use(logger({ level : 'info' }));
```

But before we start our `express` server, we modify the `level` via the `custom-logger` defined environment variable:

```bash
CUSTOM_LOGGER_LEVEL=debug
```

A question arises **“On what level will we log? Info? Or Debug?”**. Our experience tells us to consult the docs or skim the source code.

Any user of the `custom-logger` should not be skimming the source code, as a proper defined module should not require the user of that module to know the implementation details and inner workings.

Then what is wrong with consulting the docs? When you create a module, the usage should be as intuitive as possible, 
therefore to make the usage of it *pure and deterministic*. 
The module should not change behaviour because of a change or condition that is not explicit in your code. 
When I say “your code”, I mean the call site of the NPM module in our `express` server.

```js
const logger = require('custom-logger');

app.use(logger({ level : 'info' }));
```

Docs are definitely useful and important, but it should not be the band-aid for a bad, unintuitive API of a module.

**Docs are definitely useful and important, but it should not be the band-aid for a bad, unintuitive API of a module.**

No, not at all, but a reusable 3th party module like the custom-logger should be environment agnostic. When you are developing your application, you should take full control of how the you supply the configuration of the given NPM modules that you use. Environment variables are a I/O interface that should be fully controlled by you, the developer, with the aid of the **Dependency Inversion Principle.**

```js
const logger = require('custom-logger');

app.use(logger({ level : process.env.LOG_LEVEL }));
```

Now we took control of the `I/O` layer by injecting the configuration to given NPM module from our code. 
We also have the freedom to change the name of the environment variable or even the source itself, 
maybe we want to read it from a `config` file instead.

```js
const logger = require('custom-logger');
const config = require('./my-config');

app.use(logger({ level : config.logLevel }));
```

The additional advantage we get out of this is, we avoid the “decisions” of the `custom-logger` authors to bleed into 
our application and operations. An example of this would be that we have the names of the environment variables dictated by the NPM module. 
They might have decided on another naming convention than yours. 
Your code, architecture and operations should not be influenced by used tools and libraries.

**But what if I want to change the configuration at runtime?**

You got me there, somewhat. There is no guarantee that changes at runtime of an environment variable will be picked up by a library either, as this is implementation specific. In addition to that, it’s is common for developers to restart their service after the configuration was modified, as changing the configuration at run time can cause unpredictable behaviour of your service.

**Conclusion**

There is nothing wrong with environment variables for configuration, but do avoid using or supporting the configuration of modules/libraries (not only NPM) through environment variables, as this should be a concern and freedom of the user of the module/library and you don’t want implementation details of 3th party modules to bleed in your code base.
