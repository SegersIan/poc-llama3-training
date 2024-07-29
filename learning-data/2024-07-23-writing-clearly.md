---
title: From Code to Clarity - How Writing Can Transform Your Coding Skills
summary: This article delves into the thought process behind code refactoring and how it parallels with writing to achieve clarity. We'll explore the iterative nature of coding and its impact on clear thinking. Discover practical tips for writing more clearly, the benefits of clarity in software engineering, and how mastering these skills can unlock your full potential, one iteration at a time.
date: 2024-07-23
tags:
  - Programming
  - Clear Thinking
---

How often do you find yourself tweaking or refactoring your code? Have you ever thought about your thinking process while doing this? Let's explore how this process of refining your code can be used to find more clarity in your work, your code, and other thoughts.

# The Refactoring Process

Your client wants to teach kids to count, their problem is, they need help to show how counting goes. You need to create a solution that prints all numbers from 1 to 5. You start off with a Test-Driven-Development (TDD) mindset and implement the solution in the most straightforward way:
```js
console.log(1);
console.log(2);
console.log(3);
console.log(4);
console.log(5);
```

You run it... and it works, 1 minute of work. You glance at your watch and realize, I'm charging by the hour, might as well refactor it a bit. You are a "Do Not Repeat Yourself" (DRY) advocate, so you refactor your solution:

```js
for(var number = 1; number < 6; number++){
    console.log(number);
}
```

The client changes their mind and wants to teach only about odd numbers. The program must print all odd numbers from 1 till 5". You update your test case and take the path of least resistance to make that test pass:

```js
for(var number = 1; number < 6; number++){
    if(number === 2) continue;
    if(number === 4) continue;
    console.log(number);
}
```

You stare at the solution and realize it makes you uncomfortable. "If they increase that range, I need to update the code in multiple places, nor is the code very self-explanatory, it's not obvious what it is intended to do" you tell yourself. The hour is still far from over, enough time to tidy up:

```js
for(var number = 1; number < 6; number++){
    if(isOdd(number)){
      console.log(number);
    }
}

function isOdd(number){
  return number % 2 > 0;
}
```

Now the code starts to become a bit more self-explanatory and it's easy to change the range (cause [you think you know how the client will change their mind](https://www.xkcd.com/974/)). You realize you still have 30 minutes left. After reading your code, you think it's still too imperative. One last shot to make it easier to understand:

```js
var numbers = createListOfSequentialNumber(1, 5);

for(const number of numbers){
  if (isOdd(number)){
    console.log(number);
  }
}

function createListOfSequentialNumber(startNumber, endNumber){
  // Implementation omitted for brevity
}

function isOdd(number){
  // Implementation omitted for brevity
}
```

After reading the solution once again, you feel fairly content with the solution, it's clear, readable, easy to understand and a change in range can be easily done.
You tell yourself "another hour of honest work", close your editor and send out an invoice to the client.

One might feel the urge to discuss overengineering as we reflect on this case study, that's not what this article is about. The focus of this article leads towards another thought process to examine.

# Clarity Of Thought

Your code is a text that describes your solution to a problem. When you rewrite or refactor, you basically are "rephrasing" that solution. Why do you rephrase your code, or any text at all? One reason can be, you are not satisfied with the current wording of the text (or code) that describes your solution. It feels messy, uncomfortable, maybe it's too verbose, hard to read, or lacks structure?

You go back over the problem and its solution. You analyze it, maybe spot some flaws, and you gain some new insights. Armored with this new wisdom, you restructure, reorganize and improve your solution. After a cup of coffee, you repeat that process once more, eventually, after a few iterations, you are hopefully satisfied with the structure, the phrasing and the clarity of your solution.

Notice, you went through a process of reading, understanding, reflecting, reasoning, refining and rephrasing your thoughts (e.g. the solution), a process that you repeated a few times. With each iteration, you reached a higher level of understanding about the problem and a potential solution. Is this process unique to writing code?

When you write any text (even non-fiction) a great start is to "just write freely" (aka outlining), let your thoughts flow, unfiltered, no resistance. You are basically brain dumping your thoughts in a text format. As you write code, a solution to a problem, you often will write the first version like this. Along the way you might realize something, make observations or have an AHA moment. As you read this first version (out loud) you'll notice some spelling and grammar mistakes, maybe a lack of structure. It is in need of refinement.

Some writers fix all grammar and spelling mistakes and wrap it up there. Others will go through an iterative process of refinement. One way to go about it, is by asking yourself "What do I want to say?", then read your text once again and ask "Have I said what I wanted to say?" or "Does what I said make sense?" and then you go about rephrasing that text. On each iteration you might realize something new again, make more observations or have more AHA moments. Do you spot the similarities with writing code?

Writing code is writing a solution to [a problem that needs fixing](https://xkcd.com/1739/), only, you write the solution in a different language, a programming language. Programming languages are a human creation, so they often have strong similarities to our [way of thinking and writing](https://esolangs.org/wiki/Brainfuck). As in writing, there are different writing styles that can be applied in each programming language, some enforce a certain style. You might adopt a very imperative style or a more self-explanatory style, some languages don't give that flexibility. One might wonder how writing styles relate to [programming paradigms](https://en.wikipedia.org/wiki/Programming_paradigm), I'll leave that one for you to ponder about. So, why do we seem to share a similar process between writing and coding?

The human brain stores information in a tree-like structure, if you think about work, you have a whole bucket of information about your work. Within that work related bucket, you have a smaller bucket with information about coworkers. Again, that coworker bucket has a bucket about Bob and so on. When you recall Bob's annoying behavior, you are reminded of your aunt Elize who makes the same dreadful jokes. Wait, doesn't Elize fit in the "family" bucket? Yes, the human brain also keeps references across the tree-like structure. Your brain is a multi-dimensional storage unit for your memories. When writing, you are converting this multi-dimensional information into a one-dimensional string of words. The tree-like structure and its cross references are for many people quite vague when they examine these.
Due to this vagueness and this complex conversion it would be quite remarkable if you can do the conversion from thought to written format properly on the first attempt.

It's only natural that you have to go back, re-read that text and make sure it  came out properly. The same happens when talking, sometimes you realize what you just said was incoherent, nonsensical, or incomplete. It is normal that you need to revise, edit and correct the end result of your attempt to express larger ideas and thoughts in text. But that's not all that's happening.

Remember the last time you tried to explain a complex problem you struggle with to a coworker, did you ever have the answer come to you, as you were trying to [articulate the problem](https://en.wikipedia.org/wiki/Rubber_duck_debugging) to your coworker? There is a feedback loop here. As you go through this process, you are further improving the structure of your thoughts, you might even learn new things and make new neural connections along the way, resulting in greater understanding and clarity. The tree-like structure in your brain becomes clearer with stronger cross references. That's the reason why writing a summary about anything you just learned can be so effective or why asking "What have you learned from this?" can be so powerful. This back and forth process happens also while coding and refactoring.

This process is not limited to writing or natural languages. A mathematician used math to express and think, a musician uses notes and their hearing to create and improve, anyone might use a whiteboard to express and visualize their thoughts and put them up for scrutiny, an architect draws blueprints on paper to share his plans and an artist uses a blank canvas to paint and express abstract concepts. All these channels, languages, annotations allow for expressing, reflection and play with the abstract. Along the way making for more clarity of your thought and useful learnings *(An exploration of this multi-modal concept is for another article)*.

There it is, *clarity of thought*, giving you the ability to communicate clearly, to express your thoughts clearly, to reason more clearly, write code more clearly and more importantly, to learn. Clarity of thought gives you a major advantage in any work you do as a software engineer: improved critical thinking, write cleaner code, write effective emails, do impactful code reviews, express new ideas, write a design document that makes sense to others and properly express your arguments. Very few are born with a talent for this, you can learn and develop this skill.

# Writing More Clearly

Pushing yourself to write your thoughts in a clear manner will give you a clearer understanding of the subject, as well as learning useful new insights along the way. If you are a software engineer, you probably often write more text than code on any given day, writing advice works well for your daily work as for writing code (aka writing a solution). Some programming languages are not so close to natural languages, in that case, you could consider writing  the pseudocode first. My advice is a non-exhaustive and informal list, pick what works for you.

Although writing is most commonly thought of as a way of expressing thoughts that we have already formed, it is also an excellent tool for discovering and clarifying thoughts. Improving your writing will directly improve your ability to write better code and vice-versa.

## The Reader
Some of the best and clearly written articles are jargon articles that are even accessible to people from outside that given jargon. Many TED talks discuss scientific topics, made accessible by the speaker. Within the field of software engineering it is hard to agree on what constitutes a minimum general knowledge within the field. There are countless technologies, libraries, experience levels, tools, languages and frameworks, making it impossible to all know the same things. In addition, the majority of software engineers must communicate with non or semi technical stakeholders to get things done. There is no point to fight this. Mind the reader or target audience.

Reading Tip: [Rhetorical Situations](https://wac.colostate.edu/repository/teaching/intro/rhetoric/)

## The Writing Process

"What do I want to say?" Start with that question and write freely from there. Once you got that first outline you can reread it and work through your text iteratively, on global level, but also per paragraph/sentence:

### Guiding questions
* "What do I want to say?"
* "Did I say what I wanted to say?"
* "Does it make sense what I just said?".
* "Is this sentence/paragraph/text clear to someone who knows nothing about the subject?"
* "What do I need to say next? Will it lead logically out of what I’ve just written?"
  * A linear built up of your text is key to increase understanding by the reader, one step at a time. You wouldn't start teaching someone to program if they never have worked with a computer.
* "Is there any ambiguity for the reader?"
* "Am I sticking to what I want to say and the subject?"
  * Avoid scope creep and make sure you remain focused, you might get too eager to share things that are not within the actual scope or that relevant to the topics at hand.

### Simplify
Did you know TED talks have a hard stop at 18 minutes to force speakers to avoid inflating its content? It doesn't allow for unclarity if you want to introduce a new idea in a short time frame.

Prune words and sentences that repeat or don't add value. Be ruthless, if it does not help the reader, it's just taking space. Great writing is all about the power of the deleted word (Richard Bach). Rewrite if it doesn't work, don't be attached to everything you write. Choose short words over lengthy ones.

Consider using GenAI to improve how you formulate your ideas, take this with caution though, ChatGPT loves by default a lengthy and cluttered writing style. Make sure to prompt for "simplified", "concise", or "clear" language. However, it can be a great sparring partner.

Don't be tempted nor intimidated by others with their pompous or snobbish writing style. Academia and business suffers from this pretentious writing style. Trim any clutter or pompous writing, all readers will be thankful. Writing in a short, clear style takes more effort and skill than academic or business writing. Simple writing doesn't mean a simple mind. One must argue the opposite, someone who can articulate things clearly, often thinks clearly and has little fog and clutter in their mind. The French mathematician and philosopher, Blaise Pascal said "If I had more time, I would have written a shorter letter".

### Iterate

The cognitive benefits of iteration are profound.

For software engineers, the concept of iteration probably isn't new.
Iteration is at the foundation of agile, lean, DevOps, TDD and many other movements and methodologies because iteration establishes an important feedback loop for improvement and learning.
It's almost industry-wide knowledge that the first solution is rarely the best solution, same for expressing complex ideas in some language:

* Iteration deepens your understanding on a subject because it forces you to re-examine and re-think aspects of that subject.
* Iteration enhances creativity as you continuously try to seek better ways to express ideas or find solutions.
* Writing (code) is a process, not a product.

As you iterate, do keep these tips in mind to remain productive:

* Break down the problem or the tasks allowing for lightweight iterations, allowing for smaller, manageable incremental improvements.
* Don't overdo it, perfection is not the goal, make sure that each iteration still adds sizable value.
* Take a mental break between iterations of minutes, hours, days based on the scope, deadline and importance.
* Iterate on the overall scope (e.g. overall structure) as well as on local parts (wording, sentence structure, ...).

### Blog, Teach, Talk, Explain

"To teach is to learn twice" (Joseph Joubert), this exemplifies how teaching deepens one's own understanding of a subject. One of the most effective ways to deepen your understanding and learn to clearly formulate is by teaching, explaining or public speaking. That's why *good* public speakers, bloggers and content creators know their subject so well, through the process of preparing their content, they learn and improve. It's a natural self-reinforcing loop. The more content they create, the better they become. I personally experienced this as I was coaching students on [FreeCodeCamp](https://www.freecodecamp.org/) meetups, blogging and doing tech talks.

# Final Thoughts

As I wrote this article, I've only started the journey myself, I went through this process, expressing and iterating on my thoughts and ideas. I gained many insights along the way, hopefully resulting in a clearer and more enjoyable article.

By mastering the art of clear thinking and concise writing, you'll not only transform your code but also unlock your full potential as a software engineer, one iteration at a time.

# Resources

* [Art Of Thinking](https://www.amazon.com/Art-Thinking-critical-Creative-Thought/dp/0321953312) by Vincent Ruggiero.
* [On Writing Well: The Classic Guide to Writing Nonfiction](https://www.goodreads.com/book/show/53343.On_Writing_Well) by William Zinsser.
* [Ted Talks: The Official TED Guide to Public Speaking](https://www.goodreads.com/book/show/41044212-ted-talks?) by Chris J. Anderson.
* [WAC: Writing Across The Curriculum](https://wac.colostate.edu/repository/teaching/intro/)
* [WAC: Writing To Engage](https://wac.colostate.edu/repository/teaching/intro/wte/)
* [Writing To Learn](https://www.goodreads.com/book/show/53343.On_Writing_Well) by Willian Zinsser.
* [Writing Process (MIT)](https://writingprocess.mit.edu/)
