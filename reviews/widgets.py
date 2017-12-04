from django.forms import RadioSelect


class RadioSelectModified(RadioSelect):
    """Customized radio button for the star rating system. Modifications in the templates include: label after input (instead of wrapping in label) and reverse looping over every option (input) - to work with star rating in review template."""
    template_name = 'reviews/django_modified/radio_modified.html'
    option_template_name = 'reviews/django_modified/radio_option_modified.html'

class RadioReversed(RadioSelect):
    """
    Radio widget, which lists items in reverse order.
    """
    template_name = 'reviews/django_modified/radio_reversed.html'
