---
title: You should do Everything-As-Code
summary: By adopting *-as-code methodologies/tools you can achieve advanced living documentation and enjoy an improved AI experience.
date: 2024-05-13
tags: 
  - IaC
  - DevOps
  - Automated Documentation
  - Living Documentation
  - Policy-As-Code
  - Infrastructure-As-Code
---

# Intro

In the early days, our code repositories just contained application code. Plain and simple. 
As time went by, "application configuration files" became a thing. 
Linting came around the corner and suddenly we had "linting configuration files".
CI/CD pipelines started using a declarative model and "pipeline definition files" were invented.
Let's add "infrastructure definition files" (Infrastructure-As-Code) and also some "policy definition files" (Policy-As-Code) for the fun of it.

We can see a solid trend of this *-as-code (Everything-As-Code) methodology which results in many additional metadata files in our code repository allowing for greater automation.

Aside of obvious purpose of each of these metadata files, do they have any other additional value? Just fill up disk space? Create an impressive file tree?

# Documentation

Did you forget to document any of it? Yes? Who cares, right? 
Just look at the code or the repo, all the answers are there (at least if you follow everything-as-code).
Why would we have to put additional effort to duplicate all this knowledge in written format? 
So we can forget about it?

Don't we hate documentation anyway? 

Yet, that less-tech-savvy person comes along and asks me "Is this change already in production?", "What is the data contract of that?", "What is authorization rule to access this data?". 
Ugh, No counter-strike match during break. 

# Be Lazy

How can we automate this?
Remember, our code repository is full of these metadata/definition/config files containing most of the answers. What do all of these files share? They're machine readable (JSON, YML, XML, ...), can we do something with that? I spidey sense automation opportunities. 

* Need a network diagram? Can we not generate one from our IaC files?
* Need to explain the authorization rules for an entity? Why not generate a human readable format from policy-as-code files?
* Need to document the share a data contract? Generate that from the source code.
* Need to document which services are listening to a specific event? Why not generate a list based on which services have permissions to read certain event streams?
* Need a class diagram? Why not generate from the source code a diagram-as-code?

The sky is the limit! You can generate so many views as you want. However, as always, only create what is used or necessary. No one likes fixing an automation step that serves no purpose.

# Consume It!

Just like in the MVC model, we have the "data models" available in machine-readable files, we just need to create different "views" of this data, or rather "user interfaces", cause there are a few possibilities:

* **Web Interface**: The straight forward use case
  * Who: For the non business stakeholder to easily access and consult key information. Or even for the developer, this might be easier and quicker to pull up during a meeting, instead of opening their IDE and navigating these files.
  * How: Generate a static site with tailed "view" for your needs. Displaying data contracts and deprecation information can be very useful here, put those annotation/decorators/whateverators to use!
* **(Knowledge) Graph Interface**: The analytical use case of all artifacts and their dependencies.
  * Who: Architects, Developers, IT Managers
  * How: By feeding the data models into (knowledge) graph databases or systems (e.g. [Ardoq](https://www.ardoq.com/)) it's easier to generate complex views, diagrams or analyze complex dependencies.
  * Also: Microsoft Azure offers out-of-the-box the [Azure Resource Graph](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview) which gives a graph interface to all of your azure resources.
  * Tip: Enrich your data with mechanism like "[Tags](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources)" to easily filter or query your knowledge graph.
* **AI Interface**: Knows who love graph data ? AI! Your casual ChatGPT and your Developer AI tools.
  * Who: Architects, Developers
  * How: By using the data models as source for your general AI or else developer AI tool.
  * Also: Some AI developer tools already scan your metadata/definition/config files to give your more insights. They love these machine-readable formats!
  * Tip: Remember to not blindly feed all your data to ChatGPT to avoid leaking sensitive information.

# A 10,000 Feet View

You know what the real amazing thing is about Knowledge graph and AI interfaces? They can aggregate all this valuable data from various code repositories, enabling cross-repository insights and data models.

# Benefits

* Up-to-date knowledge.
* Pan-repo views possible for any application.
* Many ways to combine these interfaces and ideas to solve documentation and governance challenges.
* Great potential for (enterprise) architects.
* Declarative models are easier to analyze than imperative code/implementation (e.g. Using Policy-As-Code libraries over implementing authorization policies in your code)
* You can basically mine your code, infrastructure and relevant artifacts.

# Resources

* https://github.com/microsoft/ps-docs
* https://betterprogramming.pub/automate-terraform-documentation-e9839deceb6e
* https://www.redpill-linpro.com/techblog/2021/02/11/terraform_documentation_with_terraform_docs.html
* https://www.linkedin.com/pulse/documenting-policies-code-jan-varga-jjaoe
* https://www.reddit.com/r/Kotlin/comments/18cbygl/do_you_think_we_need_an_automatic_code/
* My brain and experience