---
title: A Developer Introduction To The Cloud
summary: A quick guide on understanding and distinguishing cloud vendors and their numerous products.
date: 2019-03-30
tags: 
  - Cloud
  - AWS
  - Azure
  - GCP
---
*Published originally on [Medium](https://itnext.io/a-developer-introduction-to-the-cloud-91012abbaed4)*

The cloud has become mainstream for many businesses. Big companies like Netflix are deployed on Amazon Web Services, others do hybrid solutions and then there are companies that are even moving away of big cloud vendors create their own data centers/cloud (e.g. Dropbox).

As a developer, the chances of working with a cloud service or vendor grow by the day, some of you might have worked only with the cloud. In this article, I will elaborate on how the major cloud vendors (Google Cloud, AWS and Azure) are build and how you can easily understand their numerous products which all seem so similar. The goal is that after reading this article, you can easily understand any cloud product of any provider on what it does and how it distinguishes itself from other products.

## The Core Resource Types

Cloud vendors provide you with different types of resources that help you build any type of solutions:

* **Compute**: Your computing power to run code, software, jobs and such.
    * *(e.g. EC2, Lambda, Cloud Functions, and Azure Virtual Machines)*
* **Storage**: Methods to data, this can be to store simple files, the filesystem for your virtual machine, or the storage space for your database.
    * *(eg. AWS S3, AWS EBS, and Azure Storage Disk)*
* **Networking**: Resources for organizing your network of storage and compute resources, how do they communicate? Can they communicate? How can we access these resources?
    * *(e.g. VPC, Virtual Network, Fixed IP addresses, and DNS)*
    
The majority of cloud services and products usually delivery some service based one of the above resource types or a combination. When you are reading about a product/service, ask yourself:

> Which resource type(s) does the product/service use?

E.g. A database service like AWS RDS is a combination of **compute** and **storage** resources. A service like AWS S3 is a **storage** resource.

*One could argue that each resource is always combined with networking resource(s) for access, which might be true, but this is something the cloud vendor takes care of under the hood.*

## The Scale Of Managed-Ness

Each cloud vendor has a wide variety of services and products that try to solve a particular problem. Some products are very similar in what they provide, often the key distinction (besides pricing) is how “managed” the service is.

The **more managed** a service is, the less maintenance and overhead you have to use and operate this service.

> Example: Lambda/Cloud Functions, you don’t provision servers, nor do you write the code to bootstrap the server, you just write the code that is relevant for solving your use case. You don’t have to take care of patching the software and OS nor the security access to these servers which execute this code.

The **less managed** a service is, the more freedom you have but also more responsibility in operating and using these services.

> Example: EC2/Virtual Machines, you provision the server instances yourself, you decide on the computing characteristics (RAM, CPU), you attach storage to it, you have to maintain the OS, do security patches and all that stuff, but you have the full control of these virtual machines.

For example, the compute resource has many different products/services solely focused on compute, but differ in the scale of how managed they are.

![An Image](./assets/cloud-introduction_01.png)

When you are reading about a product/service, ask yourself:

> Where on the scale of managed-ness does the product/service fall?

We do have some cool naming for (some) of the different types of compute:
* IaaS: Infrastructure as a Service
* PaaS: Platform as a Service
* FaaS: Function as a Service

## The Location
Products/services which you provision or deploy might or might not be bound to a (physical) location where you want to deploy and operate. Every cloud vendor has a notion of “global”, “regions” and “zones”.

![An Image](./assets/cloud-introduction_02.png)

* **Global**: Services on this level usually don’t deploy services, like AWS IAM which basically is the user management for all the AWS users of a certain organization. This is region/zone agnostic. Let’s say I want Peter the sysadmin to have the privileges to provision virtual machines. Depending on the cloud vendor I might limit in which regions and zones Peter can provision virtual machines, but we organize these users and their privileges on a global scope.
* **Region**: A region is a geo-specific location, usually denoted by a country or a city. This groups a set of zones, or rather data centers within a certain vicinity of each other.
* **(Availability) Zones**: Each region has (usually) two or more zones. Each zone is a distinct data center. The idea is that each zone has its own power supplier, network, and power backup infrastructure, isolated from the other zones. These zones are also located geographically away from each other. This isolation is meant so that if one zone goes down because of a natural disaster or a power grid failure, that the other zones within a region are not impacted. Most vendors will create high-speed network connectivity between the zones of the same region.

The idea is that you provision your resources close to your user base. If the majority of your users are in Europe, then the Region Frankfurt, Germany might be a good choice, as your services will run close to your users. But to maintain high availability, it’s wise to deploy your resources across different zone’s within that region, in case one zone might go down due to a power failure.

Zones are often denoted with an alphabetic value (eg. a, b, c), and the regions are often denoted with their continent and orientation.

* In AWS, the Frankfurt region is named **eu-central-1**. If it has 3 zones, the zones will be named **eu-central-1a, eu-central-1b, eu-central-1c**.

**Fun Fact**: Often the name of a zone is randomized for each cloud vendor customer. Meaning if you provision a virtual machine in eu-central-1a it does not mean it will be the same zone when I specify eu-central-1a when provisioning a virtual machine. The reason this is done (at least in AWS) is that many customers often provision in a default selected region (e.g. “a”), which would cause the region “a” to overloaded while region “b” and “c” are underused.

When you are reading about a product/service, ask yourself:

> Is given service/resource global, regional (aka cross zone) or zone specific?

A virtual machine is always provisioned within a zone, some managed database services might be deployed regionally as they under the hood take care of failover instances in different zones, then this database services is provisioned within a region, not a zone.

Virtual networks (AWS/GCP VPC’s) are often also regional. You create a virtual private cloud (VPC) within a region, but then within that VPC, you provision multiple virtual machines in the different zones. VPC’s are split into subnets, and (at least in AWS) a subnet can only live in one zone.

## The Product/Service Types

Products and services are grouped in different fields and types often. Some of them are closely related to a resource type (computed, storage and networking) while others use a combination of resources (like a database), while others are democratized services(like a Text-To-Speech service).

Some services have nothing to do with the aforementioned and are just utilities for developing your solution (like a hosted git server or CI pipeline) or managing your cloud environment (like AWS IAM, which is to manage the users and privileges within your cloud account).

It is impossible (and not worthy) to list all types and services of cloud providers as this changes daily but these are the most common:

* **Compute**: Virtual Machines, managed hosting, serverless, and machine learning solutions.
* **Storage**: File storage for Virtual Machines, block storage like AWS S3 or equivalent “bucket” solutions.
* **Database**: Services that host databases.
* **Developer Tools**: CI pipelines, deployment, repository hosting, …
* **Democratized services and APIs**: Text-To-Speech, Speech-To-Text, image recognition, NLP.
* **Monitoring**: Monitor and log aggregation of all the services that you use.
* **Administration**: User administration, privileges, key management, authentication, and billing.

Many of these services and products combine different resources under the hood. Beside differing on how “managed” they are, some services try to tackle a niche or very specific challenge, like “batch jobs” in AWS. It mostly “compute” but with a very specific use case in mind.

---


The advantage of using a single cloud vendor for building solution is that cloud vendors tend to create tools and interfaces so that all their products and services can interact with each other. This can be in a direct way (my web service in my virtual machine uploads files to a storage solution like S3) or in an indirect way by listening to events. (When the event “a new file was uploaded to S3” happened, trigger a lambda function. If a file on S3 is older than 30 days, move it to a cold storage solution).

This can be extremely helpful to build solutions in a fast cost-effective way but bare in mind, it does increase your vendor lock-in.

## Pricing

Pricing differs between vendors but often there are similar characteristics they invoice on. Do your due diligence to understand the price of each product/service. They change over time so always better to read up to the latest values. Therefore my statements can be outdated or wrong at the time of reading.

* **Data in/out:** Aside of the products and services you might use, AWS, for example, charges you based on the data that moves out of a region. You don’t pay for bandwidth between zones within the same region.
* **Compute time:** You usually pay for the compute time that is required to run a service, this can be per x amount of milliseconds (like for Cloud Functions/Lambdas) or per hour (like for virtual machines).
* **Storage:** The type of storage and the amount used impact the pricing also. Notice that compound service like a managed DB uses compute and storage. When we talk about block storage like S3 you might have pricing on how often you access the data and how fast. Using cold versus hot storage.

Any service will have its own specific pricing or be the accumulated pricing of the different parts like compute time, storage and data in/out. Carefully read the pricing and FAQ of each service/product to understand the total cost picture.

When you are reading about a product/service, ask yourself:

> How does the pricing work?

## Summary

When you try to understand a cloud service/product you should ask yourself the following 4 questions:

* **Which resource type(s) does the product/service use?**
* **Is given service/resource global, regional (aka cross zone), or zone specific?**
* **Where on the scale of managed-ness does the product/service fall?**
* **How does the pricing work?**

These are the key questions to understand any of the products and services that cloud vendors provide to you. The key difference between 2 similar products/services will lie in the answers of the 4 key questions.

Understand the answers to these questions and you’ll be able to decide if a product/service is appropriate or not. Remember that the more managed the service is, the faster you can create and deploy solutions. But you do lose certain freedom. The more specific your needs are or become and you need more freedom the less managed you want your service probably to be, which will result in a higher maintenance overhead.

### Some useful links

* [Comparison between AWS and Azure](https://docs.microsoft.com/en-us/azure/architecture/aws-professional/services)
* [Comparison between AWS and Google Cloud](https://cloud.google.com/docs/compare/aws#service_comparisons)
* [Comparison between Google Cloud and Azure](https://cloud.google.com/docs/compare/azure#service_comparisons)

