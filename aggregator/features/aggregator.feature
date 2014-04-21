Feature: Using the backend

Scenario: Browse new articles
  Given we have some test data loaded from "feed_items.json"
  Given we have some test data loaded from "articles.json"
    When the user accesses the url "/backend/articles/"
    Then she should see 10 articles in the sidebar, for example
      | title                          | position |
      | A short history of spam        |        1 |
      | Rename the Nobel for Economics |       10 |

    When the user clicks on the link "Older"
    Then she should see 10 articles in the sidebar, for example
      | title                                 | position |
      | DjangoCon Europe 2014 Call For Papers |        1 |
      | Announcing DjangoCon AU 2014          |       10 |


Scenario: Browse explicitly hidden articles
    When the user accesses the url "/backend/articles/hidden/"

    Then she should see 10 articles in the sidebar, for example
      | title                          | position |
      | A short history of spam        |        1 |
      | Rename the Nobel for Economics |       10 |

    When the user clicks on the link "Older"
    Then she should see 10 articles in the sidebar, for example
      | title                                 | position |
      | DjangoCon Europe 2014 Call For Papers |        1 |
      | Announcing DjangoCon AU 2014          |       10 |


Scenario: Browse published articles
    When the user accesses the url "/backend/articles/public/"
    Then she should see 0 articles in the sidebar
