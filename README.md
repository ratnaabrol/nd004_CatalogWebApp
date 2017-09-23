# Udacity project - Catalog Web Application

## Activating a user
```
$> python3 -m catalog_webapp.db.grant <email> <provider> --active
```

## Making a user an administrator
```
$> python3 -m catalog_webapp.db.grant <email> <provider> --active --admin
```

## Testing
The integration tests require an sqllite database to be created with name `test_catalog.db`. To create test this database, in the code root:
```
$> python3 -m catalog_webapp.db.create_db --dbstr sqlite:///test_catalog.db
```

## Background
[Design](DESIGN.md)
