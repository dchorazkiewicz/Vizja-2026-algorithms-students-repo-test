# How the Full Online Classes Would Be Run

The repository presents the technical part of the proposed model for working with students: programming assignments, versioned solutions, automated analysis, collection of technical evidence, and preparation of feedback. However, the repository itself is not a complete description of how the classes would be conducted. The full model assumes that technology supports the teaching process, but does not replace it.

The fundamental idea is to shift the centre of activity from the instructor delivering knowledge to the student actively working with a problem. The goal is not to have the instructor spend most of the session demonstrating implementations while students passively observe how a problem should be solved. Students should receive a problem, prepare their own solution, make design decisions, and then be able to explain and justify those decisions and, when necessary, revise them in response to feedback.

A typical learning cycle therefore looks like this:

**assignment → independent analysis → implementation → commit → automated technical evidence → discussion and review → revision → next version**

The repository mainly supports the middle part of this process. It preserves concrete versions of student work, runs repeatable tests, observes algorithmic behaviour, and prepares information that the instructor can use during a substantive discussion with the student. It does not make the final educational decision on behalf of the instructor.

## Classes as Technical Review

In this model, an online session resembles a professional technical review.

The student does not merely demonstrate that the program returns the expected result. The student should also be able to explain:

- what problem the algorithm solves and what its contract is;
- why the chosen method is correct;
- which properties remain true during execution;
- why the algorithm terminates;
- what its time and space complexity are;
- what happens in edge cases;
- why the implementation actually corresponds to the required algorithm rather than merely producing the same final output.

The instructor can then compare the student's claims with the observed behaviour of the program.

If a student claims to have implemented binary search, but the measurements show several thousand element reads for a few thousand elements, the discussion should not end with a message saying that a test failed. The real questions become: why is this happening, which property of binary search has been violated, and what must change so that the implementation exhibits the expected behaviour?

Similarly, a correct final AVL tree is not sufficient if the implementation rebuilds the entire tree after every insertion. Correct output is one dimension of the solution, but the course is also about the method used to obtain that result.

This kind of discussion allows understanding to be assessed much more deeply than a test result alone.

## The Role of Automation

Automation is intended to increase the quality of the interaction between the instructor and the student.

Human attention and time are limited. Manually checking dozens of repetitive properties of student implementations—basic correctness, operation counts, violated contracts, or observable structural properties—is not the best use of an instructor's time.

The system can collect this information beforehand.

As a result, before speaking with a student, the instructor may already know, for example, that:

- the solution is functionally correct;
- the implementation exhibits unexpected cost growth;
- there is an excessive number of writes;
- the algorithm does not terminate early enough;
- a global structural invariant has been violated;
- a different method was used than the one required;
- the student has corrected a specific issue compared with an earlier commit.

The instructor does not therefore have to begin every review by manually discovering the basic facts. The discussion can immediately move to interpretation and to the student's reasoning.

In this model, the automated report is **material for the review, not a substitute for the review**.

The final interpretation belongs to the instructor. A student can also challenge an automated finding, justify an unusual implementation, or identify a case that the tool did not account for. That, too, can be an educationally valuable part of the process.

## What the Online Session Itself Looks Like

The online meetings do not need to take the form of a ninety-minute mini-lecture.

The instructor may briefly introduce a problem, explain a particularly important property, or highlight a concept that will be useful during the work. Most of the session, however, should belong to the students: presenting solutions, answering questions, discussing design decisions, comparing different approaches, and revising earlier versions.

Not every student has to go through a full review during every session. With a larger group, students can be reviewed in rotation. Automatically collected information helps identify cases that are especially worth discussing: solutions containing a common mistake, an unusual approach, an interesting optimisation, or a discrepancy between functional correctness and actual algorithmic behaviour.

The instructor can also use issues found in student work as the basis for a short explanation to the whole group.

In that case, theory appears at the moment when students already have a concrete context for it.

Instead of beginning with a long abstract explanation of sorting stability, the group can first examine a solution that sorts the data correctly but changes the relative order of elements with equal keys. Only then does the question, “What exactly is stability, and why was it lost here?” become directly connected with a real problem.

## The Role of Artificial Intelligence

The model deliberately takes modern tools, including AI systems, into account.

There is little value in designing classes around the assumption that students do not have access to documentation, search engines, language models, or programming assistants. These tools are already part of the real working environment.

For that reason, the more relevant question is no longer:

**“Did the student produce this code entirely without assistance?”**

but rather:

**“Does the student understand the solution for which they are taking responsibility?”**

Students may use supporting tools, but they must be prepared to explain the code, its properties, its limitations, and the design decisions behind it.

If a tool generated a correct implementation but the student cannot explain the invariant, the complexity, or the cause of a particular behaviour, the review will reveal that very quickly.

If, on the other hand, the student used AI to find an approach, verified it, understood it, and can defend it technically, then the tool has served exactly the role it may later serve in professional work.

The objective is therefore not to ban tools, but to establish **responsibility for the result**.

## Why This Model Matters Professionally

Professional software development rarely consists only of independently writing a correct piece of code.

A developer must also present a solution to other people, answer questions, justify a decision, accept criticism, recognise limitations in their own approach, and improve an earlier version.

A junior developer may know the syntax of a programming language and be capable of producing working code while still struggling with basic questions such as:

“Why did you do it this way?”

“What problem are you solving?”

“What are the costs of this approach?”

“What happens when the scale of the data changes?”

“How do you know this solution is correct?”

“Which assumption is essential here?”

These abilities cannot be developed effectively through a single seminar presentation near the end of a degree programme. They should be practised repeatedly, in the context of concrete technical problems.

For that reason, discussion of the solution is not an additional activity beside learning algorithms. It is part of learning algorithms.

## The Role of the Instructor

The role of the instructor also changes.

The instructor is not primarily a source of information that the student cannot obtain elsewhere. The instructor's value increasingly lies in asking the right questions, interpreting student work, identifying incorrect mental models, and adapting the level of challenge to the individual student.

The same problem can be discussed differently with a beginner and with a very strong student.

One student may be asked what the individual variables in binary search represent and why the loop terminates.

Another may be asked to formulate the loop invariant.

A stronger student may be asked how to modify the algorithm to obtain the equivalent of `lower_bound`, or what properties are required of the ordering relation.

Automation provides information. The instructor decides which question is educationally most valuable at that particular moment.

## The Overall Goal

The objective of this model is not to build a more complicated grading system.

The objective is to create an environment in which students repeatedly perform the complete cycle of professional intellectual work:

**understand the problem, design a solution, implement it, observe its behaviour, analyse evidence, explain their decisions, receive criticism, and improve the next version.**

The repository and automated analysis are intended to make this mode of work practical even with larger groups and to ensure that the instructor's limited time is spent primarily on activities that should not be automated: discussion, interpretation, questioning, and development of the student's way of thinking.

In this sense, the technical infrastructure and the way the classes are conducted are two parts of the same educational model.
