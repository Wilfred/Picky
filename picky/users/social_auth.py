

def new_users_inactive(backend, details, response, user, is_new,
                       *args, **kwargs):
    """Anyone may create an account, but an admin needs to activate it.

    """
    if user and is_new:
        user.is_active = False
        user.save()
