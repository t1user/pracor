from reviews.models import Position
from django.urls import reverse

def drop_username(*args, **kwargs):
    """Fix for a problem with username, which social_auth tries to save to user model,
    usermodel has no username (users are identified by email)"""
    if 'username' in kwargs:
        kwargs.pop('username')


def save_data(**kwargs):
    """Saves data retrived from linkedinin into the database."""
    new_user = kwargs['is_new']
    new_association = kwargs['new_association']
    params = kwargs['response']
    positions = params['positions']['values']
    user = kwargs['user']
    session =  kwargs['strategy'].session

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
        for item in positions:
            for existing in existing_positions:
                if item['id'] == existing.linkedin_id:
                    new.remove(item)
    else:
        for item in positions:
            new.append(item)

    # create new position for every linkedin position not yet in the database
    for position in new:
        if position:
            new_position = Position(user=user,
                                    company_name=position['company']['name'],
                                    linkedin_id=position['id'],
                                    company_linkedin_id=position['company'].get('id'),
                                    location=trans_location(position['location'].get('name')),
                                    position=position['title'],
                                    start_date_month=position[
                                        'startDate']['month'],
                                    start_date_year=position[
                                        'startDate']['year'],
            )
            # linkedin doesn't provide this field in standard api call
            # unless a way is found to access this field, this should
            # be removed (together with associate_by_email function)
            web_site = position['company'].get('website-url')
            if web_site:
                # try to match the company in the db by website
                company =  associate_by_email(web_site)
                if company:
                    new_position.company = company
            new_position.save()


    #Do this to accounts newly associated with linkedin:
    if new_association:
        # add linkedin id and url to user profile (fuck knows why, but maybe useful one day)
        user.profile.linkedin_id = params['id']
        user.profile.linkedin_url = params['apiStandardProfileRequest']['url']
        user.profile.save(update_fields=['linkedin_id', 'linkedin_url'])

    #find unassociated positions
    try:
        # select Positions that don't have any associated Company
        unassociated = Position.objects.filter(user=user, company__isnull=True)
        # write unassociated company names to session and after pipeline
        # finishes redirect to association view
        companies= [(position.id, position.company_name) for position in unassociated]
        # redirect to association view only if there are any unassociated companies
        if companies:
            session['companies'] = companies
            session['next'] = reverse('linkedin_associate')
    except:
        # no unassociated Positions have been found so just proceed with standard
        # flow
        pass


    
    

    """
    #CHANGE REDIR THIS WAY
    redir=reverse('register_success')
    kwargs['strategy'].session['next']= redir
    kwargs['strategy'].session['linkedin_data'] = 'some data to be retrived'
    #THIS IS THE WAY TO GET ACCESS TO SESSION
    kwargs['strategy'].session
    """

def associate_by_email(web_site):
    """
    If a linkedin company has a website-url, try to associate it with the database by website.
    """
    try:
        company = Company.objects.get(website=web_site)
        return company
    except Company.DoesNotExist:
        pass


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
