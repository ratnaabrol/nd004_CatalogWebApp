# Catalog Web Application - Design

## Entities
### User
* id - required - primary key, integer, auto increment
* username - required - string
* email - required - email address
* joined_at - required - UTC timestamp
* active - required - boolean

### Catalog
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* name - required - string
* created_at - required - UTC timestamp
* description - optional - string

### Category
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* name - required - string
* created_at - required - UTC timestamp
* description - optional - string

### Item
* id - required - primary key, integer, auto increment
* owner - required - foreign key, user.id
* name - required - string
* created_at - required - UTC timestamp
* description - optional - string

### Role (__stretch goal__)
Course grained and initially will impact whole application.

Fixed values: Admin, Edit, Delete
* id - required - primary key, integer, auto increment
* name - required - string
* description - optional - string
