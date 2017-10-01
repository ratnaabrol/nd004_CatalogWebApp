# Catalog Web Application - Design

## Entities
### User
* id - required - primary key, integer, auto increment
* username - required - string
* provider - required - the provider used to register the user (enumeration "local", "google")
* email - required - email address
* joined_at_utc - required - UTC timestamp - default db current timestamp
* active - required - boolean - default false
* admin - required - boolean - default false
    * TODO: Move role assignments to separate tables

### Catalog
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* name - required - string
* created_at_utc - required - UTC timestamp
* description - optional - string

### Category
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* catalog - required - foreign key, catalog.id
* name - required - string
* created_at - required - UTC timestamp
* description - optional - string

### Item
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* category - required - foreign key, category.id
* name - required - string
* created_at - required - UTC timestamp
* description - optional - string

### Role (__stretch goal__)
Course grained and initially will impact whole application.

Fixed values: Admin, Edit, Delete
* id - required - primary key, integer, auto increment
* name - required - string
* description - optional - string
