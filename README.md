# Udacity project - Catalog Web Application

## Testing
The integration tests require an sqllite database to be created with name `test_catalog.db`. To create test this database, in the code root:
```
$> python3 -m catalog_webapp.db.create_db --dbstr sqlite:///test_catalog.db
```

## Background
[Design](DESIGN.md)
