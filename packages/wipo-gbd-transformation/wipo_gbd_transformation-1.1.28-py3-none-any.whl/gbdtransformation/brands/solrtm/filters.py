import re

# create synonyms for application/registration numbers
def create_synonyms(value):
    if not value: return []

    value = str(value)
    synonyms = [value]

    # remove special characters
    special_chars = re.compile(r'\W')
    value = special_chars.sub('', value)
    synonyms.append(value)

    # remove non-numeric
    non_numeric = re.compile(r'\D')
    value = non_numeric.sub('', value)
    synonyms.append(value)

    # remove leading zeros
    while(value[0:1] == '0'):
        value = value[1:]
    synonyms.append(value)

    return set(synonyms)

# expand multi-national applications
def expand_territories(territory):
    if territory.upper() == 'EM':
        return [ 'EM', 'AT', 'BE', 'BG', 'HR',
                 'CY', 'CZ', 'DK', 'EE', 'EM',
                 'FI', 'FR', 'DE', 'GR', 'HU',
                 'IE', 'IT', 'LV', 'LT', 'LU',
                 'MT', 'NL', 'PL', 'PT', 'RO',
                 'SK', 'SI', 'ES', 'SE', 'GB' ]
    else:
        return [ territory.upper() ]


# if combined, then image type has Word and Device
def get_image_type(mark_feature):
    if mark_feature == 'Combined':
        return ['Word', 'Device']
    if mark_feature == 'Figurative':
        return ['Device']

    return [mark_feature]

# only top 2 for classification
# might be usefull for faceting
def cl_top2(classes):
    return ['.'.join(c.split('.')[:2]) for c in classes]

def validate_status(status):
    if status not in ['Ended', 'Expired', 'Registered', 'Pending']:
         raise Exception('Invalid Status: %s' % status)
    else:
        return status[0:3].upper()
