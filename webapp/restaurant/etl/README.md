#ETL
Currently the ETL runs the following pseudo code:
* Extracts and separates the data from the CSV file based on the database model structure
* Transforms the extracted data into the associate model class
* Loads this transformed data into the database

The extraction phase happens with no dependency on the extraction of other models. The transform + load portion
is dependent upon the database model relationships. The order of the dependency is as follows:
- RestaurantType
- Restaurant
- RestaurantContact
- Grade
- InspectionType
- Inspection
- Violation
