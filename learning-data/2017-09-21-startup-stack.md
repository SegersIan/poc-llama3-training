---
title: How to choose a startup stack
summary: My methodology for choosing a startup stack
date: 2017-09-21
tags: 
  - Javascript
---
*Published originally on [Medium](https://medium.com/saveboost/how-i-chose-our-startup-stack-70ddd8e164b)*

Last January I started my job as a full stack engineer at Saveboost. I was responsible for bootstrapping the product as I was the first software engineer and employee that joined the startup.

My first task at hand, carefully choose a stack and start hacking my way to the first MVP/MLP/M*P, take your pick. With this post I’d like to share how I chose our stack and my reasoning behind it, and yes, I ended up with a typical startup stack.

---

## Requirements

Like any project, I’d had to first analyze our requirements. We were at the idea stage, everything was new, we had a small investment to bank roll the team for a few months, we had no product market fit, no customers, just an idea and a small sum of money. This translates into the following requirements :

* **We should be able to move fast with the stack**
* **The stack should be affordable to host**
* **The stack should be easy to bootstrap**
* **Future potential hires should not be too expensive for chosen stack**
* **No steep learning curves in the near future**

I felt that these requirements reflected the needs of the company at the current stage to be able to get to product market fit.

## Language

Starting with myself, what was my current skill level? In the 5 years prior to Saveboost I mostly did C# (backend), and spend the last year in my free time diving into Javascript. Generally the advise they give to engineers for a start up is, “Choose the stack you’re most comfortable/experienced with, because speed is essence”.

“I will have to take C# in that case” I thought to myself, but wait. Does it make sense? Let’s revise our requirements:

* **We should be able to move fast with the stack**
    * *Yes, at least me.*
* **The stack should be affordable to host**
    * *No, at the time .NET core was still in an early stage, so a gamble, hosting a C# server requires a windows server and they’re considerable expensive.*
* **The stack should be easy to bootstrap**
    * Yes
* ** Future potential hires should not be too expensive for chosen stack.**
    * No, I just moved to Barcelona, so I was unfamiliar with the salary ranges for .NET developers in town. But often they work for consultancy companies, and they have money, so after some locale market research, this seemed like a no.*
* **No steep learning curves in the near future.**
    * No, at least not for me, but if there are not many C# developers or they’re expensive, potential hires might have to face a steep learning curve.
    
Hmm, 3/5 No’s, that’s not a very positive projection. So what else do I know? Javascript, but I never created something of significant size, but I liked it. I got some tips on Ruby, they claimed it’s easy to learn, but still a huge gamble to start something new. After asking around I also discovered that the demand for Ruby developers was insanely high in Barcelona, which translates in high salaries, something which is not affordable in the first stages of a real startup.

Skimming the internet a bit further I stumbled upon some other languages that are being sold for having a low learning curve, like Go and Python. Python is pretty popular, Go isn’t compared to many other languages.

Javascript means one language for the entire stack, it was my second strongest skill at that point, it’s extremely cheap to host, many developers know it, or at least the basics (affordable hires), the learning curve is pretty ok in my opinion and it’s easy to bootstrap. That’s like almost 5/5 Yes’s, **Javascript it is then!**

## Frameworks and BaaS

Now we had that sorted out, I did some research to Backend-as-a-service’s and (opinionated) frameworks. These might speed up to development time to get to our product market fit. Don’t forget, speed is crucial since money is very scarce. A working prototype that can generate revenue or reach product market fit is more important than a solid architecture but no users for a company at this stage.

* **Firebase**: A full reactive stack, pretty sweet, did a 2 day hack-a-ton with it, has many features and services that come out of the box, but the combination of vendor lock-in and limited backend freedom gave me the impression that this wouldn’t be a wise choice. I knew in advance that our solution would have a lot of backend processes, at this point we decided to go for a chatbot as the initial user interface. So not sure if the reactive features would be of any use.
* **Meteor**: Like Firebase, full reactive, but very opinionated. Hosting options were limited, did also a mini hack-a-ton with it to try it out. Same limitations as Firebase; vendor lock-in and at a later stage hard to move out of this architecture. Taking the chatbot into consideration, were we mostly gonna needed a REST api, it seemed obvious this was not an interesting option.
* **NodeJS**: Slower for bootstrapping compared to Firebase and Meteor, but an architecture/framework that probably would survive long term, without a vendor lock-in, but endless hosting options. Since we were starting of with a chatbot at first, I didn’t need much of the Firebase and Meteor special features, so NodeJS seemed like a good option, along with KoaJS v1 because of it’s generator support for working with Promises. At this stage async/await was not yet production ready in Node.

## Database

Great, now we have a language and a framework to bootstrap our project! What’s left… a database! Like previous decisions, this was not a no-brainer. Majority of the people choose MongoDb in NodeJS, but was it really such a wise decision? I researched many options, but let’s highlight the most important ones I researched:

* **RethinkDb**: Reactive database, pretty neat features. I played with it for a while, I really liked it, but the community was very negative at this point in time. The core contributors or company that was maintaining RethinkDb just announced they planned to stop maintaining it, they published in a blog post that they were talking with prospects that would be interested in taking over the project. In addition to that, I read a lot of frustration of the community regarding a low activity in commits and pull request approvals. This made me step away from this.
* **PostgreSQL**: Solid database engine, has document support, along with SQL. Since we were gonna work with financial processes I really liked the transaction support of a good old fashioned SQL database. This database engine is already somewhat of a proven veteran. I heard many positive comments about it regarding speed, stability and I know quite some companies that transitioned from MongoDB to PostgreSQL once their product was mature enough and got past product market fit.
* **MongoDb**: For the document databases, this is the most popular one and maturing quite well. It had at least somewhat of support for left-join queries and again the syntax is very native to Javascript, that’s always a nice extra. This database engine has good documentation and is actively maintained, many affordable hosting options also.

I have spent countless hours in choosing between PostgreSQL and MongoDB. They both have pro’s and con’s. I was starting to run out of time and had to make a decision. I discussed the pro’s and con’s with friends and advisors. The ideal use case for MongoDb is for storing unstructured data that you would get from external API.

SQL is mature and withstood the test of time, don’t forget the countless of man hours that went into developing, improving and finetuning SQL databases. Transaction management remains to be a huge benefit, they help you for not having to resort immediately to Saga implementations until a certain level.

**In the end I decided to go for MongoDb**, I knew in the first months of prototyping the product, the data model would change countless times, and I didn’t want loose time on running SQL migration scripts after every local change and production deploy. One person told me once during a discussion “It’s easier to move from Document to SQL than the other way around”, maybe, maybe not, but an interesting point.

This was a decision with a small margin, time was passing and I had to start working on the product. Until today I still contemplate the decision, but time goes on, I know that I spend a decent amount of time on weighing the pro’s and con’s. Now it is time to move forward.

## Frontend framework

Now I had the full stack ready to build our first prototype with a chatbot interface. But it was obvious that at a later stage we would have to start implementing a web UI. So after a while I started skimming the interwebz for viable frontend frameworks. Sadly my experience with these were very limited.

* **Angular 2**: I played around with Angular 2 when I co-founded Nexpat, but it left a strong impression on me because of the steep learning curve. At the point that I first experimented with Angular 2 which was in Beta, and it took a lot of me to learn. In retrospect I know now that it was because I was still fresh to Javascript and the Typescript along with learning the Angular 2 paradigm was all new to me, so I was learning a lot of new things all together. This could have clouded my judgement at the time.
* **Angular 1**: I used this in a small one month project (after I played around with Angular 2 @ Nexpat) when I was creating a small app with the Ionic framework. This had a lower learning curve due to the absence of Typescript and my increased Javascript experience.
* **ReactJS**: While I was applying for a job, I had to make a small project in ReactJS as a technical test. I liked it, the learning curve was pretty low and the community was booming at this point.
* **VueJS**: Never had heard of this one before, but one of our advisors, [Michael Karliner](https://medium.com/@mkarliner) tipped me about this one. I was at doubt at first, I thought, yet another new framework, dammit. But after creating some mini prototypes, I really liked the documentation, how it worked, the handelbars templating and the low learning curve.
* **EmberJS**: [Edit 2, forgot this one]. We used this in a previous company I worked for, I did experiment with it one day. The learning curve felt a bit steep at that point. But now know that it was rather due the immaturity of my Javascript skills at that point. Ember comes with best practices like JSON API and such, so I’d advice anyone to at least experiment a bit with it.

Being the last ‘big’ decision in the stack, I spend countless hours reading blogs regarding the topics of Angular vs React vs VueJS. After thorough reading and discussions with fellow developers **I decided to go with VueJS**.

VueJs had the lowest learning curve of them all, a good vibrant community and excellent documentation. It just fell comfortable to use. I do not argue that other frameworks are better or not. This was just the right framework for me, I already had so much on my plate, I had to choose something that was easy to learn and understand so I could move fast.

My only concern was that it was extremely new/young. This is always a risk you should take into consideration. Another benefit of VueJS was that they have official supplementary libraries for routing and state management. This means that they most likely won’t introduce any crazy breaking changes that would make the libraries incompatible from each other.

---

## Reflection

There we have it, the full stack:
* Javascript
* NodeJs
* MongoDB
* VueJS

When I looked at the final stack, I did got nervous. This really looks like a hype driven stack decision, no? Did I let myself seduce in all the new shiny hot things? Did I made the right decisions for this startup? Was I a victim of confirmation bias? It really freaked me out to be honest.

Do I regret my decisions? No, for sure not. I know that I took a considerable amount of time in researching all the options. I weighed all the pro’s and con’s of each technology and had exhaustive discussions with senior developers. I did a lot of prototyping to compare different frameworks and technologies.

Taking all the interests of Saveboost at heart with a potential to success, I feel I made a good choice to the best of my abilities.

---

Note : This is a condensed version of the decision process, many details on the decisions process has have been omitted to keep the article bite size.

Edit 1 : After some feedback I realized that I failed to mention anything regarding learning curve of the databases. The benefit of SQL is that the majority of graduates have a good basic skill regarding rational databases. So for majority of potential hires, this would be low entry to get into, Document databases are not common in a curriculum of computer science degree (at least when I was studying). MongoDb however has a very nice Javascript native api, meaning a minimal bootstrap, but a different philosophy compared to SQL.