# Scope and provenance

## What this repository is

This repository is a **proof of concept for the programming-exercise and automated-feedback side of Algorithms and Complexity**.

It demonstrates how I would organise that workflow if I were responsible for this part of the course:

- publish structured programming assignments;
- let students work in GitHub forks;
- observe concrete student commits through a private mirror;
- evaluate those commits with private automated tests and instrumentation;
- produce versioned technical reports;
- turn those reports into actionable GitHub feedback;
- re-evaluate later revisions without losing the history of earlier work.

It is a demonstrator of an approach, not a record of an already-running official course process.

## What this repository is not

This repository is not:

- an official university course repository;
- an official student workbook;
- a claim that I am the lecturer for the course;
- a description of lecture delivery;
- a description of classroom management;
- an official grading policy currently in force.

The focus here is deliberately limited to the asynchronous technical workflow around programming exercises and feedback.

## Relationship to the syllabus

The **course syllabus is the authoritative common input** used to identify the subject areas that exercises should cover.

This repository uses that syllabus to design a demonstrator for practical programming work.

## Relationship to Algorithms_and_Complexity

The repository [Algorithms_and_Complexity](https://github.com/dchorazkiewicz/Algorithms_and_Complexity) is a **separate proof of concept**.

That project explores a different question:

> What could student-facing self-study material look like if the syllabus were expanded into a structured web-based learning resource?

It contains syllabus-derived explanatory material, examples, and a navigable website.

It is **not an official set of lecture notes**, does not document a lecture taught by me, and does not imply ownership of the lecture component of the course.

## Why both repositories exist

The two repositories explore two independent transformations of the same source syllabus:

~~~text
                       source syllabus
                       /             \
                      /               \
                     v                 v
 syllabus → learning-material PoC    syllabus → exercise/feedback PoC
 Algorithms_and_Complexity           this repository
~~~

The first explores how a syllabus can become readable learning material.

The second explores how the same syllabus can become executable programming assignments, private automated assessment, technical evidence, and iterative feedback.

Neither repository is presented as an official university artifact unless it is explicitly adopted as such later.

## Current demonstration status

The repository now contains three self-contained demonstrations:

- List 01 — foundations and simple algorithm observability;
- List 02 — searching, sorting and divide-and-conquer;
- List 03 — binary trees, BST and AVL trees.

For presentation purposes, each demonstration keeps student-facing files, private-grader files, hidden-test equivalents, simulated submissions, CI and evidence together so the entire mechanism can be inspected from one link.

A production deployment would separate the public student layer from the private mirror/grader layer.
