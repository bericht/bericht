Feature: Using the backend

Scenario: Browse new articles
Given we have some test data loaded from "feed_items.json"
When the user accesses the url "/backend/articles"
Then she should see 10 articles in the sidebar
Then the 1. article should have the title "Rename the Nobel for Economics"
Then the 10. article should have the title "Voting for the right"

When the user clicks on the link "Older"
Then she should see 10 articles in the sidebar
Then the 1. article should have the title "Western Sahara resources"
Then the 10. article should have the title "DjangoCon Europe 2014 Call For Papers"
