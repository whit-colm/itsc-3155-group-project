# AskHole - A Crowdsourced Instant Tutoring Platform

# Scenarios

## John Smith's Student Succcess

John Smith (*he/him*) is a Junior student at UNCC. While he excels in his gen-ed mathematics, he struggles in major of computer science. John works most of the day so a lot of his work happens at odd hours of the night or on week-ends.

John's most recent project uses Python to create a webserver, which sends and recieves JSON data. While he has most of the back-end down, he's confused on the method of converting to and from JSON. In prior years, he was at a difficult crossroads on achieving this, none of his options seemed good:

- Be forced to wait a few days to start the project after a back-and-forth with the professor over email.
- Hope the tutoring centre has a time slot he can slide into without ruining his workday.
- Violate university policy by just searching for the answer on Google.

However, he can play with his AskHole instead. He logs on to the system and creates a new thread, tagging it with `# Python` and `# ITSC-3155`. 

In the meantime, John looks at `# MATH-1242` questions, as he did very well in the class. He sees a question by Erika Mustermann about u-substitution. There's a couple answers already given but at best they only tell half the story. He votes on the better ones and also gives his own explanation.

20 minutes later, Seán Ó Rudaí (*they/them*) is browsing the webiste and sees John's question. It reminds them of a Python framework that they were asked to use when they took John's class. They make a response to the thread linking the framework. John really appreciates this when he checks back, and gives the *Author Award* to Seán's answer.

## Meili Wang's Assisting Adventure

Meili Wang (王美丽) (*zie/hir*) is a student at UNCC, and quite a good one. Zie got excellent marks in hir Data Structures and Algorithms course, and was even asked to be a TA. However, zie lives in a town ~100km from UNCC, and mostly does online classes. Meili exclusively uses Zoom for office hours because of this, but hir hours are mostly empty because of how few people want to use Zoom. Now that zie can get into hir AskHole, zie also spends those hours reviewing recent posts tagged `# ITSC-2214` and giving helpful answers. Normally this involves answering the questions and then giving hir own response the Instructor Award to pin it at the top of the thread.

In one of the threads, Seán Ó Rudaí has provided a very good answer. So Meili doesn't even need to answer hirself. Instead zie gives them the award.

In another thread, Erika Mustermann (she/her) answered a question regarding an in-class quiz with a link to a GitHub Gist with all the answers. Meili reports the message for "Suspected violation of academic integrity". Zie adds as a comment in the report the GitHub user who created the gist's username is "emustermann".

## Prof. Sharma's Instructional Investment

Aman Sharma, PhD. (*he/they*) is a recent postgrad who has started teaching at UNCC. While he is eager to teach, his first semester has not been going great as his pedagogic methods aren't well honed. He encourages all his students to try AskHole, even creating a specific tag for his class, and monitors posts with that tag to try and see common questions. A lot of questions over one week revolve around pthreads in UNIX-like operating systems, and most of them start with "I'm in Dr. Sharma's class and they...". With this in mind, he updates the lecture notes for next class with some more examples and re-words some test questions to try and be more intuitive with answers.

Before logging out, he checks the reports. He sees one from Meili Wang regarding potential academic integrity violations from Erika Mustermann. The case seems pretty cut-and-dry so he hides it from view, preventing any students from viewing it. However another report has been made against Juan Pérez by a Ulysses Nancy Owen for "Offensive or inappropriate behavior"; when he looks at the message in question however, Juan has not said anything vulgar, so he does not take action against the message.

# User Stories

- As a student, I am often late to class and miss the first ~8 minutes of instruction, and therefore am confused on minor points that do not warrant a whole tutoring session.
- As a student, despite being in a high level class, I have a rather silly question. I want to ask it in class but feel it will be embarassing. I want a method to ask my peers in a way where I won't feel stupid.
- As a student, I want to help my peers but have to care for my disabled partner at home, so I can't stick around on campus. I want a method to help people that can do so remotely.
- As a student, I feel I have to cheat to stay afloat because of how little time I have to work outside of a job. I don't like to cheat, but between 5 minutes on Chegg and 50 flipping through a textbook, I cannot afford to do otherwise. If I am to stop cheating, I need a more viable alternative than the 50 minute crawl.
- As a TA, I want to be able to work with my students on thier problem points in a more streamlined way. I get too many emails already so some questions slip through the cracks.
- As a tutor, I want to be more approachable; many students avoid me because of the time, effort, and pants commitment of the tutoring center.
- As an instructor, I want to work with my students in a more casual environment, as they seem to respond better that way.
- As a university administrator, we need to cut down on the rampant amount of academic integrity violations. A "war on cheating", where we more harshly penalize those caught, does not effect this much. So we need to meet students where they're at.
- As a univerity administrator, we need to make sure students' learning environments are safe and welcoming. Any new platform needs to have moderation at the forefront. 


# Feature List

Minimum Viable Product:

- Users are put into 3 groups: Students, IAs[^1], and Instructors
- Users' capabilities are determined by their permissions.
- No authentication is done, only authorization on demonstration barer tokens
- **Students**, **IAs**, **Instructors** can view a reverse-chronological ordered list of questions by creation date (threads)
- **Students**, ***IAs**, **Instructors***[^2] can post a question
  - Threads can be made pseudo-anonymously
  - Threads can be tagged with a class (`# ITSC 1212`) or technology (`# Java`)
- **Instructors** can de-anonymize anonymous users.
- **Students**, **IAs**, **Instructors** can answer questions (respond, create responses)
- **Students**, **IAs**, **Instructors** can vote on answers
- Three types of awards can be given to messages in threads. Each award type can only be given to a single response. a response can recieve multiple award types. Awarded responses are shown at the top of the thread; in the following order top-to-bottom.
  1. **IAs**, **Instructors** can award an "*Instructor Award*"
  2. **The thread OP** can award an "*Author Award*"
  3. **System** automatically gives a response with the highest votes the *Community Award*
      - The *Community Award* is issued by the system 4 hours after the creation of the thread to the response with the highest number of votes (`>2`). The *Community Award* attempts to be reissued every 6 hours after its first issuing to a new message insofar as it has a strictly greater number of votes than the incumbent recipient.
- **Students**, ***IAs**, **Instructors***[^2] can report messages for anti-social behaviour.
  - Reasons include "Suspected violation of academic integrity", Offensive or inappropriate behavior", "Hate speech", "Spam", "Promotion of illegal activities", or "Something else"
- **Instructors** can view a reverse-chronological feed of the most recent reports made.
- **Instructors** can view a specific report and take moderation actions against it.
- **Instructors** can hide messages following a report
- **IAs**, **Instructors** can view hidden messages' content and author.
  - **Students** can only see that a message has been hidden.
- **Instructors** can create new system-wide tags for posts.
- **Instructors** can delete system-wide tags.

[^1]: IAs include tutors and TAs
[^2]: Due to how permissions work, IAs and Instructors *can* do this, but there's no actual reason for them to.

While an enhanced feature set will be easy to implement assuming a well thought out technology stack, this MVP will suffice to show the benefits of such a system.