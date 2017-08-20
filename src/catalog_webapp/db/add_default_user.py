"""Script to add a default user to the database."""

from sqlalchemy.exc import SQLAlchemyError
from catalog_webapp.db.default_engine import SESSION_FACTORY
from catalog_webapp.model.user import User


def add_default_user():
    """Adds the default user to the database.

    Returns the User added or None if unable to add the user.

    Exceptions:
    LookupError -- if the user already exists
    sqlalchemy.exc.SQLAlchemyError -- if an error occurs accessing the database
    """
    user = None
    session = SESSION_FACTORY()
    try:
        user = session.query(User).\
            filter(User.username == "default").one_or_none()
        if not user:
            user = User(username="default",
                        email="default@nowhere.no.where")
            session.add(user)
            session.commit()
            session.refresh(user)  # refresh so contains data added on insert
            session.expunge(user)  # detatch user from the session
        else:
            session.expunge(user)
            raise LookupError(user)
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()

    return user


def main():
    """Entry point for this script."""
    try:
        user = add_default_user()
        if user:
            print("Added user '{}'".format(user.username))
        else:
            print("Unable to add user.")
    except LookupError as lu_err:
        # pylint:disable=no-member
        lu_user = lu_err.args[0]
        print("Default user already exists in the database.")
        print("Was added at: {} UTC".format(lu_user.joined_at_utc))
        print("Username: {}".format(lu_user.username))
        print("Provider: {}".format(lu_user.provider.name))
        print("Email: {}".format(lu_user.email))
        print("Active: {}".format(lu_user.active))
        print("Admin: {}".format(lu_user.admin))
    except SQLAlchemyError as sql_err:
        print("Error accessing the database." +
              " Please ensure the database exists." +
              " Details below.")
        print()
        print(sql_err)
        raise


if __name__ == "__main__":
    main()
