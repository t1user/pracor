from .linkedin_creds import (SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
                            SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET)


SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']

SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    'first-name',
    'last-name',
    'headline',
    'location',
    'industry',
    'positions',
    'picture-url',
    'site-standard-profile-request',
    'api-standard-profile-request',
    #'public-profile-url',
    'email-address'
]

SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('firstName', 'first_name'),
    ('lastName', 'last_name'),
    ('headline', 'headline'),
    ('location', 'location'),
    ('industry', 'industry'),
    ('positions', 'positions'),
    ('pictureUrl', 'picture_url'),
    ('siteStandardProfileRequest', 'site_standard_profile_request'),
    ('apiStandardProfileRequest', 'api_standard_profile_request'),
    #('publicProfileUrl', 'public_profile_url'),
    ('emailAddress', 'email_address')
]


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    #'social_core.pipeline.user.get_username',
    #not included in standard pipeline
    'social_core.pipeline.social_auth.associate_by_email',
    #required because of change in user model
    'pracr.social_pipeline_override.drop_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    #saves linkedin data in models
    'pracr.social_pipeline_override.save_data',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    # Overriden to handle exceptions.
    'pracr.social_pipeline_override.allowed_to_disconnect',

    # Collects the social associations to disconnect.
    'social_core.pipeline.disconnect.get_entries',

    # Revoke any access_token when possible.
    'social_core.pipeline.disconnect.revoke_tokens',

    # Removes the social associations.
    'social_core.pipeline.disconnect.disconnect',
)



SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/auth_error/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False


SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/profile/'
