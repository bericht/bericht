Feature: Using the backend

@wip
Scenario: Set up the environment
  Given we have some test data loaded from "feed_items.json"
  Given we have some test data loaded from "articles.json"
  When the user logs in as "test"


Scenario: Browse new articles
    When the user accesses the url "/backend/articles/"
    Then they should see 10 articles in the sidebar, for example
      | title                          | position | public |
      | A short history of spam        |        1 | hidden |
      | Rename the Nobel for Economics |       10 | hidden |
    Then they should see an article with the following attributes
      | title                   | source                                  | updated   | public | tags |
      | A short history of spam | Le Monde diplomatique - English edition | 4/22/2014 | hidden | None |
    When the user clicks on the link "Western Sahara resources"
    Then they should see an article with the following attributes
      | title                    | public |
      | Western Sahara resources | public |

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
      | title                                 | position |
      | A short history of spam               |        1 |
      | DjangoCon Europe 2014 Call For Papers |       10 |

    When the user clicks on the link "Older"
    Then they should see 9 articles in the sidebar, for example
      | title                                       | position |
      | Django sprint in Amsterdam, The Netherlands |        1 |
      | Announcing DjangoCon AU 2014                |        9 |


@wip
Scenario: Browse published articles
    When the user accesses the url "/backend/articles/public/"
    Then they should see 1 articles in the sidebar, for example
      | title                    | position |
      | Western Sahara resources |        1 |
   When the user clicks on the link "Western Sahara resources"
   When the user votes "veto"
