General Overview
================

*Bericht* is a platform that aims to provide a sort of "hub" for de-centralized 
content. Current plans include articles obtained from news feeds (using the RSS 
and Atom file format) and calendars that provide iCalendar export. 

Besides imported content, articles and events can be created on the platform. 
Users can pose Questions and provide Answers (*Q&A*). Furthermore, dossiers 
provide a means to tie together topic-specific content from various sources 
augmented with an introductory article. A live ticker should provide means to 
cover live events on-line. 

Users can register at the platform. In order to ensure that content on the 
platform stays on topic, users are divided into three groups:

* **Normal users** can author non-imported content, i.e. comments and Q&A. They 
  can also propose new sources for imported content. 
* **Trusted users** can vote on content from normal users and sources that are 
  not fully trusted. Their content is also subject to the vote of other trusted 
  users.
* **Editors** can put users into the trusted users group, can author articles 
  and static pages (e.g. terms of service, about, etc.) and organize the 
  content in various ways. 

Content Types
=============

This section details the individual content types.

Global Content Types
--------------------

These content types form the backbone of the platform and are connected to 
several other content types. 

* **Entry** is an abstract concept that links to the more specific content type
  (i.e. they sub-class Entry). The trust system (voting, etc.) is linked to 
  this content type and all inheriting classes. Every inheriting content type 
  has a method to return teaser-like HTML. 
* **Comment** can be appended to any of the following content types: Article, 
  Q&A questions and answers, and events. 
* **Static Page** are for some static stuff, like 'About', 'Contact', 'Terms of 
  Service', etc. 

*Static Pages* and *Comments* are provided by mezzanine, *Entry* is, together 
with the *voting system* and the *front page* contained in an app. 

Articles
--------

Articles are long(ish) texts with formatting, possibly multimedia, etc. They 
are shown to the public and users. We decided not to use abstract article as a 
common parent class to reduce complexity, instead use Entry (see at the top).

* **Article** is authored on Bericht
* **ImportedArticle** is created from a news feed item (*FeedItem*)


Q & A
-----

This should provide questions & answers similar to the various 
http://stackexchange.com sites. But here it should be the case that people ask 
questions anonymously (to all but the administrators), i.e. the nickname should 
not be visible. Answers and comments (except from the person who asked) are 
with names. It is not yet clear if we include up- and down-voting of answers 
and approval of "the correct" answer.

The sub-content for Q&A is

* **Question**
* **Answer**


Event Calendar
--------------

An event calendar that supports singular and recurring events. Input/Editing is 
done on the EventDefinition while EventInstance is used for display (i.e. a 
recurring event has several EventInstances for one EventDefinition). It should 
support export for individual EventInstances, full calendars and all events 
from all calendars (which is the collection of events from one user) in the 
iCalendar format. Goal is also to support iCalendar import someday in the 
future.

* **EventDefintion** holds most information about an event, including how/if 
  it is recurring
* **EventInstance** is used for display and can be N for 1 *EventDefinition*. 
  Title, Body, etc. is taken from *EventDefinition*, what changes is date (and 
  possibly time).


Dossier
-------

A *Dossier* is a topic-specific collection of content with an introductory 
text, a small number of manually curated "must-reads" and the possibility to 
show a list of items based on keywords/tags. Dossiers should always have the 
same url but the content is meant to be updated regularly. Content types that 
can be connected are Articles, Q&A and Bookmarks. As it should be 'timeless', 
no events (? up for debate). Multiple users should be able to edit dossiers, 
revisions should be stored for a editing history (display of that history is 
not a priority).


Live Ticker
-----------
TODO

Bookmarks
---------
TODO

Content Handling
================

Content on *Bericht* is often imported from external sources and much of the 
content needs approval from trusted users. A few words on how imported content 
is handled and how the workflow for user-interaction is currently designed. 


Aggregator
----------

Aggregator takes care of importing content from news feeds. This should be as 
much separated from *ImportedArticle* as possible: Aggregator models store the 
"original" data, while *ImportedArticle* (which can be created from *FeedItem*) 
should be what is being displayed and maybe edited/augmented (with additional 
tags, better teaser, fixed content, etc.)

* **FeedFile** stores the feed file and archives it, time-stamped
* **Feed** stores the parsed feed
* **FeedItem** holds individual feed items
