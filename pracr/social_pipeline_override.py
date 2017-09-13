from reviews.models import Position, Profile
from django.urls import reverse

import pprint

def drop_username(*args, **kwargs):
    """Fix for a problem with username, which social_auth tries to save to user model,
    usermodel has no username (users are identified by email)"""
    if 'username' in kwargs:
        kwargs.pop('username')


def save_data(**kwargs):
    """Saves data retrived from linkedinin into the database."""
    pprint.pprint(kwargs)
    print()
    print('Strategy: ', kwargs['strategy'].__dict__)
    print('Storage: ', kwargs['storage'].__dict__)
    print('Session: ', kwargs['strategy'].__dict__['session'].__dict__)
    print()

    
    new_user = kwargs['is_new']
    new_association = kwargs['new_association']
    params = kwargs['response']
    positions = params['positions']['values']
    user = kwargs['user']
    session =  kwargs['strategy'].session

    print('New user:', new_user)
    print('New association:', new_association)

    # retrive existing positions for the user, match them with their linkedin positions
    # and create new positions if there are any new linkedin positions
    try:
        existing_positions = Position.objects.filter(user=user)
    except:
        existing_positions = None

    # compare positions retrieved from linkedin with those in the database
    # find new ones
    new = []
    if existing_positions:
        new = list(positions)
        print(new)
        for item in positions:
            for existing in existing_positions:
                if item['id'] == existing.linkedin_id:
                    new.remove(item)
    else:
        for item in positions:
            new.append(item)
            print('nowa pozycja: ', item)

    # create new position for every linkedin position not yet in the database
    for position in new:
        """
        For testing only.
        print(position['company']['name'],
              position['id'],
              position['location']['name'],
              position['title'],
              position['startDate']['month'],
              position['startDate']['year'])
        """
        if position:
            new_position = Position(user=user,
                                    company_name=position['company']['name'],
                                    linkedin_id=position['id'],
                                    company_linkedin_id=position['company'].get('id'),
                                    location=trans_location(position['location']['name']),
                                    position=position['title'],
                                    start_date_month=position[
                                        'startDate']['month'],
                                    start_date_year=position[
                                        'startDate']['year'],
            )
            new_position.save()


    #Do this to accounts newly associated with linkedin:
    if new_association:
        # add linkedin id and url to user profile (fuck knows why, but maybe useful one day)
        try:
            profile = Profile.objects.get(user=user)
            profile.linkedin_id = params['id']
            profile.linkedin_url = params['apiStandardProfileRequest']['url']
            profile.save(update_fields=['linkedin_id', 'linkedin_url'])
        except:
            # this should never happen, but if the Position still doesn't exist, just create it
            profile = Profile(user=user,
                              linkedin_id = params['id'],
                              linkedin_url = params['apiStandardProfileRequest']['url'])
            profile.save()

    #find unassociated positions
    try:
        unassociated = Position.objects.filter(user=user, company__isnull=True)
        companies= [position.company_name for position in unassociated]
        session['companies'] = companies
        session['next'] = reverse('linkedin_associate')
    except:
        pass


    
    

    """
    #CHANGE REDIR THIS WAY
    redir=reverse('register_success')
    kwargs['strategy'].session['next']= redir
    kwargs['strategy'].session['linkedin_data'] = 'some data to be retrived'
    #THIS IS THE WAY TO GET ACCESS TO SESSION
    kwargs['strategy'].session
    """
 


def trans_location(location):
    """
    Helper function for 'save_data' to get rid of weird linkedin names of Polish locations.
    """
    translate = {'Bialystok, Podlaskie District, Poland': 'Białystok',
                 'Bialystok Area, Poland': 'Białystok',
                 'Bydgoszcz, Kuyavian-Pomeranian District, Poland': 'Bydgoszcz',
                 'Bydgoszcz Area, Poland': 'Bydgoszcz',
                 'Cracow, Lesser Poland District, Poland': 'Kraków',
                 'Cracow Area, Poland': 'Kraków',
                 'Gdansk, Pomeranian District, Poland': 'Gdańsk',
                 'Gdansk Area, Poland': 'Gdańsk',
                 'Gdynia, Pomeranian District, Poland': 'Gdynia',
                 'Gliwice, Silesian District, Poland': 'Gliwice',
                 'Greater Poland District, Poznan County, Poland': 'Poznań',
                 'Poznan Area, Poland': 'Poznań',
                 'Poznan, Greater Poland District, Poland': 'Poznań',
                 'Katowice, Silesian District, Poland': 'Katowice',
                 'Katowice Area, Poland': 'Katowice',
                 'Lodz, Lodz District, Poland': 'Łódź',
                 'Lodz Area, Poland': 'Łódź',
                 'Lublin, Lublin District, Poland': 'Lublin',
                 'Lublin Area, Poland': 'Lublin',
                 'Masovian District, Piaseczno County, Poland': 'Warszawa',
                 'Masovian District, Pruszkow County, Poland': 'Warszawa',
                 'Masovian District, Warsaw West County, Poland': 'Warszawa',
                 'Masovian District, Wolomin County, Poland': 'Warszawa',
                 'Poznan, Greater Poland District, Poland': 'Poznań',
                 'Poznan Area, Poland': 'Poznań',
                 'Szczecin, West Pomeranian District, Poland': 'Szczecin',
                 'Szczecin Area, Poland': 'Szczecin',
                 'Torun, Kuyavian-Pomeranian District, Poland': 'Toruń',
                 'Torun Area, Poland': 'Toruń',
                 'Warsaw, Masovian District, Poland': 'Warszawa',
                 'Warsaw Area, Poland': 'Warszawa',
                 'Wroclaw, Lower Silesian District, Poland': 'Wrocław',
                 'Wroclaw Area, Poland': 'Wroclaw',
                 'Olsztyn, Warmian-Masurian District, Poland': 'Olsztyn',
                 'Warmian-Masurian District, Olsztyn County, Poland': 'Olsztyn',
                 'Olsztyn Area, Poland': 'Olsztyn',
                 'Sopot, Pomeranian District, Poland': 'Sopot',
                 'Sopot Area, Poland': 'Sopot',
                 'Kielce, Swietokrzyskie District, Poland': 'Kielce',
                 'Kielce Area, Poland': 'Kielce',
}
    return translate.get(location, location)
