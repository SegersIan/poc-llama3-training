---
title: Tools you need as a web/full-stack developer
summary: Your toolkit plays a significant role in your productivity. Allow me to share you the ones I use.
date: 2018-03-23
tags: 
  - Javascript
---
*Published originally on [Medium](https://medium.com/@segersian/productivity-tools-381c8a63e8cb)*

Your toolkit plays a significant role in your productivity. Therefore every web and full-stack developer should have a toolkit that helps you to get the job done. I want to share an overview of the tools that help me with my everyday work as a full-stack developer.

## HTTP Client

An HTTP Client is crucial to test quickly and efficiently any API, that being your own API or a 3th party API. I use [Postman](https://www.postman.com/) for this. I love it for its straight forward user interface and the persisted history of all API calls I made. I save hours of my time with this tool when needing to play around with APIs. I am just scratching the surface regarding its features and benefits. Definitely worth checking out.

## Tunneling

In todays world many services and APIs offer a webhook feature, basically a 3th part service that pushes updates to your publicly exposed API endpoint. This can range from receiving a webhook when a build has completed on your continuous integration server, to receiving message updates from Facebook while developing a chatbot.

When developing and testing such integration, you need to be able to expose publicly your local development server to receive these payloads for testing purposes.

A great tool for this is [ngrok](https://ngrok.com/), comes with a CLI which enables you to create a tunnel in a single command that exposes a public URL to your local development server. What I love about this tool is that it’s easy to use and for a small fee you can have a dedicated subdomain.

When launching the ngrok tunnel you get a public url (like http://somerandomstring.ngrok.io) that you can use to register your webhooks to. On your local machine you get a web interface which allows you to inspect the request and response payloads sent to your tunnel with the ability to replay any of those request. This is great, because you don’t need to re-trigger the received webhooks while testing.

This tool is also supper for a demo when you want to give access to anyone on the web to your locally hosted server or web application. Supports also HTTPS!

## Local Proxy

A local proxy to inspect any API calls that your local server makes can be extremely useful for debugging and diagnosing failing API calls. I’am gonna kill two birds with one stone here, because I use [OWASP ZAP](https://github.com/zaproxy/zaproxy) for that.

Primarily this tool is used for security testing, like, penetration testing, so in addition to getting a great security testing tool, you get a local proxy that gets the job done when you need to inspect all API calls that your local development server makes to figure out what you’re doing wrong.

Make sure to track the OWASP project, which stands for Open Web Application Security Project, helps you in improving the security of your web application.

## Regex Tester

Regex is a necessary evil for us, developers. I still often struggle to break down and comprehend the syntax, I use [regex101](https://regex101.com/) to help me to debug and format any regular expressions. With its explanation feature it really helps to understand any Regex and debug them.

## Database Client

Being able to directly view and update the data while developing is paramount. In my current project we’re using MongoDB, so I use a MongoDB Client. My favorite is [Robo 3T](https://robomongo.org/) (former RoboMongo). This tool has all the basic features that I need with a proper MongoDB shell to execute and test my queries. Nothing fancy, just all the basics I need to do my job.

Robo 3T has also a bigger brother, called Studio 3T (former MongoChef) which comes with excellent features, but not without a price tag.

## Terminal

As I use a Mac for development (Hipster Alert), I want to be fast and productive when using the terminal. I use [iTerm2](https://www.iterm2.com/) as my primary Terminal interface, which gives me more freedom in customizing my terminal interface. Comes with useful shortcuts, like creating side by side terminal views and such.

In addition to iTerm2 I use the [ZSH shell](http://www.zsh.org/) with many of the plugins from the [Oh My Zsh community](https://ohmyz.sh/). These plugins can be very useful since they come with auto complete for several CLI tools like git, docker, kubectl and many others. Check out all the available plugins [here](https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins).

I strongly suggest to anyone who is comfortable in the terminal to research tools and plugins that elevates their CLI experience.

## Conclusion

These tools I use on a daily basis to increase my productivity, therefore they are worth sharing with you. Do you want to share any tools, or do you have great alternatives worth looking into? I am eager to hear your thoughts in the comments below.