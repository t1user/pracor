from reviews.models import Positions


def drop_username(*args, **kwargs):
    if 'username' in kwargs:
        kwargs.pop('username')


def test_pipeline(**kwargs):
    params = kwargs['response']
    positions = params['positions']['values']
    user = kwargs['user']
    existing_positions = Job.objects.filter(user=user)
    print(existing_positions)
    new = []
    if existing_positions:
        for item in positions:
            print('checking item: ', item)
            for existing in existing_positions:
                print('matching existing: ', existing)
                if not item['id'] == existing.linkedin_id:
                    new.append(item)
    else:
        for item in positions:
            new.append(item)
    print(new)
    for position in new:
        print(position['company']['name'],
              position['id'],
              position['location']['name'],
              position['title'],
              position['startDate']['month'],
              position['startDate']['year'])
        if position:
            new_position = Positions(user=user,
                                     company_name=position['company']['name'],
                                     linkedin_id=position['id'],
                                     location=position['location']['name'],
                                     title=position['title'],
                                     start_date_month=position[
                                         'startDate']['month'],
                                     start_date_year=position[
                                         'startDate']['year'],
                                     )
            new_position.save()
