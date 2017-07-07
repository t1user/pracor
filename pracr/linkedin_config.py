
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '77eo269xhh3u7q'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'ywsnbntpB92vHsec'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
#SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
#FIELD_SELECTORS = ['email-address',]
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
#SOCIAL_AUTH_LOGIN_URL = '/'
#SOCIAL_AUTH_USER_MODEL = ''

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
    'social_core.pipeline.social_auth.associate_by_email', #not included in standard pipeline
    'pracr.social_pipeline_override.drop_username', #required because of change in user model
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
