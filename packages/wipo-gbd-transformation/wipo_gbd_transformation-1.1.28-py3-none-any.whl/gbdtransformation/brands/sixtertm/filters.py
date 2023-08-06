# standard gbd definitions
from gbdtransformation.brands import kinds as std_kinds
from gbdtransformation.brands import status as std_status
from gbdtransformation.brands import features as std_features
from gbdtransformation.brands import events as std_events

# namespaces defined in XML and to be ignored in procecssing
ignore_namespace = []


# -------------------------------------------------------------
# data translation helpers:
# translate values from office interpretation to gbd equivalent
# -------------------------------------------------------------

def translate_kind(kind):
    """translation of the kind of trademark to a
        multivalue gbd interpretation"""
    # out-of-the-box match

    if kind.lower().replace('_', ' ') == 'armorial bearings': return 'Armorial bearings'
    if kind.lower().replace('_', ' ') == 'flag': return 'Flag'
    if kind.lower().replace('_', ' ') == 'state emblem': return 'State Emblem'
    if kind.lower().replace('_', ' ') == 'emblem': return 'Emblem'
    if kind.lower().replace('_', ' ') == 'official sign': return 'Official sign / Hallmark'
    if kind.lower().replace('_', ' ') == 'abbreviation': return 'Abbreviation'
    if kind.lower().replace('_', ' ') == 'name': return 'Name'

    raise Exception('kind "%s" is not mapped.' % kind.lower().replace('_', ' '))

def get_status_and_date(sixter):
    status = "Registered"
    gbd_status = "Registered"
    status_date = None
    if sixter.STATUS:
        status = sixter.STATUS.TEXT.lower().capitalize()
        if status == 'Withdrawn':
            gbd_status = 'Ended'
        else:
            gbd_status = 'Unknown'
        data = sixter.STATUS.DATE
        if data:
            status_date = "%s-%s-%s" % (data[0:4], data[4:6], data[6:])
    return status, gbd_status, status_date

def st13_sixter(sixter):
    # remove special characters
    appdate = sixter['_DATE']
    appnum = sixter['_NUMBER']
    if not appnum:
        raise Exception("No appnumber provided")
    if not appdate:
        appdate = '0000'
    office = sixter.STATE_ORG or 'WO'
    return 'WO80%s%s%s' % (appdate[:4], office.upper(), appnum.zfill(7))

def get_addr(addr):
    return "%s %s %s" % (addr.ADDRESS, addr.CITY, addr.ZIP)

def split_vienna(data):
   return '%s.%s.%s' % (data[0:2], data[2:4], data[4:])

def reg_number(sixter):
    # remove special characters
    appnum = sixter.get('_NUMBER', '0')
    office = sixter.STATE_ORG or 'QO'
    return '%s%s' % (office.upper(), appnum)

def translate_status(status):
    """translation of mark status"""
    # a required data from office. if not present and no way to guess,
    # return Unknown
    if not status: return 'Unknown'

    # out-of-the-box match
    if status.capitalize() in std_status:
        return status.capitalize()

    # __insert here__ : translation logic

    # raise Exception to recognize unmapped values
    raise Exception('Status "%s" unmapped' % status)


def translate_feature(feature):
    """translation of mark feature"""

    # needed information from office
    # if office cannot provide information, then agree on a way to guess (uatm)
    if not feature: return 'Undefined'

    # out-of-the-box match
    if feature.capitalize() in std_features:
        return feature.capitalize()

    # __insert here__ : translation logic

    # raise Exception to recognize unmapped values
    raise Exception('Feature "%s" unmapped' % feature)

