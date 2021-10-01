from django import template
register = template.Library()

periods = [
    {'num': 1, 'long_name': 'January', 'short_name': 'Jan'},
    {'num': 2, 'long_name': 'February', 'short_name': 'Feb'},
    {'num': 3, 'long_name': 'March', 'short_name': 'Mar'},
    {'num': 4, 'long_name': 'April', 'short_name': 'Apr'},
    {'num': 5, 'long_name': 'May', 'short_name': 'May'},
    {'num': 6, 'long_name': 'June', 'short_name': 'Jun'},
    {'num': 7, 'long_name': 'July', 'short_name': 'Jul'},
    {'num': 8, 'long_name': 'August', 'short_name': 'Aug'},
    {'num': 9, 'long_name': 'September', 'short_name': 'Sep'},
    {'num': 10, 'long_name': 'October', 'short_name': 'Oct'},
    {'num': 11, 'long_name': 'November', 'short_name': 'Nov'},
    {'num': 12, 'long_name': 'December', 'short_name': 'Dec'}
]

@register.filter
def month_long(i):
    return periods[i-1]['long_name']


@register.filter
def month_short(i):
    return periods[i-1]['short_name']


@register.filter
def index(indexable, i):
    return indexable[i-1]
# Thanks to https://stackoverflow.com/a/29664945/17019859