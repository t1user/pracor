def drop_username(*args, **kwargs):
    if 'username' in kwargs:
        kwargs.pop('username')
