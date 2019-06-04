# Restaurant
Code for a backend web application for Orchard


## Design Decisions
For this project, I chose the following stack:
* Python 3.6
* Django Framework
* Django Rest Framework
* PostgreSQL
* Pytest + Tox

The decision on this stack was made mostly out of familiarity. While there may have been more appropriate tools
to accomplish the task, these are the tools that I could use to maximize my development efficiency.

_Note_: For more information on drawbacks on design decisions, please see the [Future Improvements](#Future-Improvements) section.

---

The schema for the database is as follows:
![Database Schema](docs/dbschema.png)

_Note_: This image was generated using graphviz v.2.40.1 and SchemaSpy v5.0.0

---

This is the SQL for the required query that will return all Thai Restaurants that have a minimum of a "B" grade:
```sql
SELECT "restaurant_restaurant"."id", "restaurant_restaurant"."restaurant_type_id", "restaurant_restaurant"."code", "restaurant_restaurant"."name", MAX("restaurant_grade"."slug") AS "minimum_grade"
FROM "restaurant_restaurant" INNER JOIN "restaurant_restauranttype" ON ("restaurant_restaurant"."restaurant_type_id" = "restaurant_restauranttype"."id") LEFT OUTER JOIN "restaurant_inspection" ON ("restaurant_restaurant"."id" = "restaurant_inspection"."restaurant_id") LEFT OUTER JOIN "restaurant_grade" ON ("restaurant_inspection"."grade_id" = "restaurant_grade"."id")
WHERE "restaurant_restauranttype"."slug" = thai GROUP BY "restaurant_restaurant"."id"
HAVING MAX("restaurant_grade"."slug") <= b
```



## Future Improvements
* Extract
  - Each data model extraction is dependent from the other extractions. This allows for an asynchronous extraction. However, in current implementation, the extraction is happening sequentially. With further time, the algorithm could see efficiency improvements by implementing concurrent extraction.
* Transform + Load
  - Due to the decision to use a relational database, this limited the efficiency of the transform + load algorithm. The relational dependency of the different data models forces an ordering on this algorithm. For instance, the Inspection models must be fully transformed and loaded into the database before beginning the same process for the Violation models, since the Violation model must know its associated Inspection at the time of transformation. A solution to this would be a structural change to the database. In this scenario, a non-relational database could allow for an asynchronous transformation of the extracted data.
* Data models
  - Under current implementation, the Restaurant model is only capable of handling a single RestaurantType. In reality, the data models would be better represented by allowing Restaurants to have multiple RestaurantType(s). For instance, in the provided CSV, some restaurants were labeled "Soups", some "Sandwiches", and some "Soups/Sandwiches". The combined version should be split into "Soups" and "Sandwiches" as two separate RestaurantTypes and both applied to the associated Restaurant. However, for the sake of time and ease of extraction + transformation, it was decided that RestaurantType would be represented by each individual value, making "Soups/Sandwiches" a completely different RestaurantType than "Soups" or "Sandwiches".
