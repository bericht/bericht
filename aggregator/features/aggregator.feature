Feature: showing off behave

Scenario: run a simple test
Given we have some test data loaded from "articles.json"
Given the user accesses the url "/backend/articles"
Then she should see 9 articles in the sidebar

