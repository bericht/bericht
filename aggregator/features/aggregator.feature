Feature: Using the backend

Scenario: Browse new articles
  Given we have some test data loaded from "feed_items.json"
  Given we have some test data loaded from "articles.json"
    When the user accesses the url "/backend/articles/"
    Then they should see an article with the following attributes
      | title                   | source                                  | updated    | public | tags |
      | A short history of spam | Le Monde diplomatique - English edition | 04/18/2014 | hidden | None |
    Then they should see 10 articles in the sidebar, for example
      | title                          | position |
      | A short history of spam        |        1 |
      | Rename the Nobel for Economics |       10 |

    When the user clicks on the link "Older"
    Then they should see 10 articles in the sidebar, for example
      | title                                 | position |
      | DjangoCon Europe 2014 Call For Papers |        1 |
      | Announcing DjangoCon AU 2014          |       10 |
    When the user clicks on the link "Kickstarting Improved PostgreSQL support for Django"
    Then they should see an article with the following attributes
      | title                                               | source            | public |
      | Kickstarting Improved PostgreSQL support for Django | The Django weblog | hidden |

Scenario: Browse explicitly hidden articles
    When the user accesses the url "/backend/articles/hidden/"

    Then they should see 10 articles in the sidebar, for example
      | title                          | position |
      | A short history of spam        |        1 |
      | Rename the Nobel for Economics |       10 |

    When the user clicks on the link "Older"
    Then they should see 10 articles in the sidebar, for example
      | title                                 | position |
      | DjangoCon Europe 2014 Call For Papers |        1 |
      | Announcing DjangoCon AU 2014          |       10 |


Scenario: Browse published articles
    When the user accesses the url "/backend/articles/public/"
    Then they should see 0 articles in the sidebar
