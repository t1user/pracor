from reviews.models import Position, Profile
from django.urls import reverse

def drop_username(*args, **kwargs):
    """Fix for a problem with username, which social_auth tries to save to user model,
    usermodel has no username (users are identified by email)"""
    if 'username' in kwargs:
        kwargs.pop('username')


def save_data(**kwargs):
    """Saves data retrived from linkedinin into the database"""
    redir=reverse('register_success')
    print(kwargs)
    print()
    print('Strategy: ', kwargs['strategy'].__dict__)
    print('Storage: ', kwargs['storage'].__dict__)
    print('Session: ', kwargs['strategy'].__dict__['session'].__dict__)
    print()
    #print(request.session)
    print()
    kwargs['strategy'].session['next']= redir
    kwargs['strategy'].session['linkedin_data'] = 'some data to be retrived'
    params = kwargs['response']
    print(params)
    print()
    positions = params['positions']['values']
    user = kwargs['user']
    #retrive existing positions for the user and add anyting new from
    # linkedin
    existing_positions = Position.objects.filter(user=user)
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
            new_position = Position(user=user,
                                    company_name=position['company']['name'],
                                    linkedin_id=position['id'],
                                    location=position['location']['name'],
                                    position=position['title'],
                                    start_date_month=position[
                                        'startDate']['month'],
                                    start_date_year=position[
                                        'startDate']['year'],
            )
            new_position.save()

    #add linkedin id and url to user profile (fuck knows why, but maybe useful one day)
    try:
        profile = Profile.objects.get(user=user)
        profile.linkedin_id = params['id']
        profile.linkedin_url = params['apiStandardProfileRequest']['url']
        profile.save(update_fields=['linkedin_id', 'linkedin_url'])
    except:
        profile = Profile(user=user,
                          linkedin_id = params['id'],
                          linkedin_url = params['apiStandardProfileRequest']['url'])
        profile.save()
    
