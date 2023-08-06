#############################################################################################################
###
### Conversions to human readable
###
############################################################################################################# 


def human_readable_number(inp):
    return inp



def human_readable_seconds(seconds):
    '''Converts seconds to human readable time'''
    TIME_DURATION_UNITS = (
        ('week', 60*60*24*7),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('min', 60),
        ('sec', 1)
    )

    if seconds < 60:
        return str(round(seconds, 1)) + ' secs'
    parts = []
    seconds = round(seconds, 0)
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)



def human_readable_bytes(num, suffix='B'):
    '''Converts Bytes to human readable size'''
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)   