General Overview
================

*Bericht* is a platform that aims to provide a sort of "hub" for small to 
medium communites. Core for this "hub" is de-centralized content and debates 
around this content. Current plans include articles obtained from news feeds 
(using the RSS and Atom file format) and calendars that provide iCalendar 
export. 

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
* **ImportedArticle** is created from a news feed item (*FeedItem*) and holds 
  the feed item's link HTML


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

A *Live Ticker* is a feature that should provide infrastructure to do live 
coverage of events. As such it provides means to add *updates* and show these 
in (reversed) chronological order with timestamps. 

On the public front end, a live ticker is displayed on an mobile-optimized 
page that automatically loads new updates at top using JavaScript/AJAX. If a 
*Live Ticker* is finished, the representation is different in that the 
updates are shown in chonological order. 

It is possible to put the *Live Ticker* on the front page (showing the latest 
k updates) and also show it as breaking, i.e. always on the top of the page 
on *Bericht*, unless the user decides to hide it (clicking on an 'x'). 

On the back end, an interface is provided that is tailored to quick data 
entry, setting the time to the current time as default and providing 
autocomplete for the optional metadata of the updates (based on previous 
updates). It is also well usable from mobile devices. 

A *Live Ticker* can be created by everyone with a certain trust level 
(either editors or trusted users) and the creator can add any users as 
contributors. This information is not shown publicly.

A *Live Ticker* constists of the following content types:

* **LiveTicker** provides a description of the event covered and optional 
  information that is always visible at top as long as the ticker is active. 
  It also holds information about who created the ticker and who is allowed 
  to post updates. 
* **Update** is an individual update and provides a timestamp, the update 
  content and a field for optional additional data that can be used for 
  location information.


Bookmarks
---------

*Bookmarks* provides the possibility for users to post links that they think 
are of interest to the community. 

For every *Bookmark* it is required that the user states, with a comment, why 
this link is interesting. Users are encouraged to add tags to a Bookmark. 
Bookmarks are subject to voting and the link's HTML is fetched for archival 
purposes and article extraction is run on the HTML. This extracted article 
is not shown in full (mainly due to copyright issues), but used for search 
and the start of the article is used as a teaser. 

The content type is thus as follows:

* **Bookmark** holds the link, user comment, HTML, extracted article and 
  metadata. 


Content Handling
================

Content on *Bericht* is often imported from external sources and much of the 
content needs approval from trusted users. A few words on how imported content 
is handled and how the workflow for user-interaction is currently designed. 


Aggregator
----------

Aggregator takes care of importing content from news feeds. This should be as 
much separated from *ImportedArticle* as possible: Aggregator models store the 
"original" data from the news feed, while *ImportedArticle* (which is created 
from *FeedItem*) fetches the link's HTML and runs the article extraction. 
*ImportedArticle* is what is being displayed and maybe edited/augmented (with 
additional tags, better teaser, fixed content, etc.)

* **FeedFile** stores the feed file and archives it, time-stamped
* **Feed** stores the parsed feed
* **FeedItem** holds individual feed items


Artex: Article Extraction
-------------------------

*Artex* extracts articles from HTML pages. It is based on readability-lxml_ 
which itself is based on the readability library from arc90_. Because many 
news feeds provide only teasers, we decided to use article extraction for 
all news feed items. Article extraction is done when creating an 
*ImportedArticle* from a *FeedItem*: The linked website's HTML is fetched, 
stored and then *artex* is run on the HTML. 

*Artex* wraps around the readability-lxml library and adds parameters that 
proved useful during our tests. First are additional 'negative' keywords 
that can are stored in ``settings.ARTEX_NEGATIVE_KEYWORDS`` and are used to 
identify non-article HTML elements. Another are the 
``settings.ARTEX_METADATA_TERMS`` that are used to identify HTML elements at 
the start and end of an article that contain article metadata (or ads). 

.. _readability-lxml: https://github.com/buriy/python-readability/
.. _arc90: http://lab.arc90.com/2009/03/02/readability/


Source Re-Check
---------------

Often it happens that blog posts, articles, etc. get modified (shortly) after 
their first publishing. Often these changes are meaningful, e.g. correction 
of facts, additional relevant information, etc. 

The goal for bericht is, on the one hand, to quickly show new content. On the 
other hand, we want to reflect these changes. To accomplish this, we re-run 
the article extraction *n* hours after the first import. 

As editors can manually edit an *ImportedArticle*, these manual changes could 
get lost if the content was simply overridden. To prevent this, the editors 
get a notification if there is an update at the source for a manually edited 
article. The changes are then shown in a diff-like view (highlighting 
additions and deletions between the current local article and the updated 
source article). 
