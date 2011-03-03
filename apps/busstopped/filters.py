from tipfy.ext import jinja2

def date_filter(value, format):
    return value.strftime(format)

env = jinja2.get_env()
env['date'] = date_filter
