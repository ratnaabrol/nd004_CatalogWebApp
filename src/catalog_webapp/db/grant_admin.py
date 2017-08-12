"""Script to grant administation rights to a user."""

import argparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from catalog_webapp.db.default_engine import DEFAULT_ENGINE
from catalog_webapp.model.user import User


def get_email_from_args():
    """Retrieves the email address from the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Grant user admin privileges.")
    parser.add_argument("email", type=str,
                        help="the email address of the user")
    args = parser.parse_args()
    return args.email


def grant_admin_to(user_email):
    """Grants administration access to the user with the supplied email
    address.

    Returns True if the user privileges were updated.

    Keyword arguments:
    user_email -- string - The email address of the user. Required.

    Exceptions:
    LookupError -- if the user cannot be found within the database.
    SQLAlchemyError -- if an error occurs accessing the database
    """
    success = False
    make_session = sessionmaker(bind=DEFAULT_ENGINE)
    session = make_session()
    try:
        user = session.query(User).\
               filter(User.email == user_email).one_or_none()
        if user:
            user.admin = True
            session.commit()
            success = True
        else:
            raise LookupError
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()

    return success


def main():
    """Entry point for this script."""
    email = get_email_from_args()
    if email:
        success = False
        error_msg = None
        try:
            success = grant_admin_to(email)
        except LookupError:
            error_msg = "No such user"
        except SQLAlchemyError as sql_err:
            error_msg = "{}".format(sql_err)

        if not success:
            print("Unable to grant admin to '{}'".format(email))
        if error_msg:
            print("Error: {}".format(error_msg))


if __name__ == "__main__":
    main()
