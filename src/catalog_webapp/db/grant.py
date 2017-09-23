"""Script to grant administation rights to a user."""

import argparse
from sqlalchemy.exc import SQLAlchemyError
from catalog_webapp.db.default_engine import SESSION_FACTORY
from catalog_webapp.repository.user import UserRepo
from catalog_webapp.model.auth_provider import AuthProvider


_USER_REPO = UserRepo(SESSION_FACTORY)


def read_priviliges_to_apply():
    """Retrieves the email address, auth provider, active and admin privileges
    from the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Grant user privileges.")
    parser.add_argument("email", type=str,
                        help="the email address of the user")
    parser.add_argument("provider", type=str, default="local",
                        help="the auth provier of the user. "
                        "Defaults to 'local'")
    parser.add_argument("--active", action="store_true",
                        help="activate the user. Defaults to deactivate.")
    parser.add_argument("--admin", action="store_true",
                        help="grant the user administration privileges. "
                        "Defaults to not admin.")
    args = parser.parse_args()
    print(args)
    return (args.email, AuthProvider[args.provider], args.active, args.admin)


def grant_privileges_to(user_email, auth_provider, active, admin):
    """Grants administration access to the user with the supplied email
    address.

    Returns True if the user privileges were updated.

    Keyword arguments:
    user_email -- string - The email address of the user. Required.
    auth_provider -- AuthProvider - the provider that backs the user. Required.
    active -- boolean - whether the user is to be activated or deactivated.
                        Required.
    admin - boolean - whether the user is to be made admin or have admin
                      privileges removed. Required.

    Exceptions:
    LookupError -- if the user cannot be found within the database.
    """
    success = False
    user = _USER_REPO.get_by_email(user_email, auth_provider)
    if user:
        user.active = active
        user.admin = admin
        _USER_REPO.update_user(user)
        success = True
    else:
        raise LookupError
    return success


def main():
    """Entry point for this script."""
    privileges = read_priviliges_to_apply()
    email = privileges[0]
    auth_provider = privileges[1]
    if email:
        success = False
        error_msg = None
        try:
            success = grant_privileges_to(*privileges)
        except LookupError:
            error_msg = "No such user"
        except SQLAlchemyError as sql_err:
            error_msg = "{}".format(sql_err)

        if not success:
            print("Unable to grant admin to '{} ({})'"\
                  .format(email, auth_provider))
        if error_msg:
            print("Error: {}".format(error_msg))


if __name__ == "__main__":
    main()
