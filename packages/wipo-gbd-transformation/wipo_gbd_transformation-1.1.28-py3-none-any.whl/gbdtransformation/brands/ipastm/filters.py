from gbdtransformation.brands import status as std_status
from gbdtransformation.brands import features as std_features
from gbdtransformation.brands import kinds as std_kinds

from .helpers import MadRef, MarkFeature, MarkStatus, MarkEvent, MarkKind, DocType

ignore_namespace = [
   'http://www.wipo.int/standards/XMLSchema/trademarks',
   'http://www.wipo.int/standards/XMLSchema/wo-trademarks']

def get_registration_nb(trademark, tmstatus):
    if trademark.RegistrationNumber:
        return trademark.RegistrationNumber

    # default registration number to application number
    # in case none is provided
    if tmstatus in ['Registered', 'Expired']:
        return trademark.ApplicationNumber

def get_expiry_date(trademark, tmstatus):
    if trademark.ExpiryDate:
        return trademark.ExpiryDate

    if not tmstatus == 'Expired':
        return None

    # find the MarkEvent Expired and get its date
    events = trademark.get('MarkEventDetails', {}).get('MarkEvent', [])
    for event in events:
        if(event.MarkEventCode == 'Expired'):
            return event.MarkEventDate

def get_registration_date(trademark, tmstatus):
    if trademark.RegistrationDate:
        return trademark.RegistrationDate

    if not tmstatus in ['Expired', 'Registered']:
        return None

    # find the MarkEvent Expired and get its date
    events = trademark.get('MarkEventDetails', {}).get('MarkEvent', [])

    # first priority is to get the Registered Event
    for event in events:
        if(event.MarkEventCode == 'Registered'):
            return event.MarkEventDate
    # second priority is to get the Published Event
    for event in events:
        if(event.MarkEventCode == 'Published'):
            return event.MarkEventDate

def is_international(transaction):
    # cannot know
    if not transaction:
        return False

    transaction_codes = [transaction.TransactionSubCode, transaction.TransactionCode]

    # if code has madrid => international
    # not => national
    for code in transaction_codes:
        try:
            if code and code.lower().index('madrid') >= 0:
                return True
            if code and code.lower().index('art9sexies') >= 0:
                return True
        except:
            pass

    return False

madref_helper = MadRef()
def get_international_ref(trademark):
    office = trademark.RegistrationOfficeCode
    # find the collection specific helper to deduce
    # application international reference from the application number
    # (every collection has its own naming convention)
    return getattr(madref_helper, '%stm' % office.lower(), madref_helper.dflt)(trademark)


type_helper = DocType()
kind_helper = MarkKind()
def get_type_and_kind(transaction):
    trans_content = transaction.TradeMarkTransactionBody.TransactionContentDetails
    code = trans_content.TransactionCode
    subcode = trans_content.TransactionSubCode
    trademark = trans_content.TransactionData.TradeMarkApplication.TradeMarkDetails.TradeMark

    office = trademark.RegistrationOfficeCode

    type = type_helper.dflt(code, subcode, trademark)
    kind = kind_helper.dflt(code, subcode, trademark)

    return (type, kind)

def translate_type(code, sub_code):

    if code == 'TRADE MARK': return 'TRADEMARK'

    # crtm
    # if code == 'Signo Distintivo':


    if code.startswith('Trademark'): return 'TRADEMARK'

    if sub_code.startswith('Marca'): return 'TRADEMARK'

    raise Exception('"%s/%s" type not mapped' % (code, sub_code))


def translate_kind(kind, office, trans_sub_code):
    if not kind:
        kind = trans_sub_code

    # out-of-the-box match
    if kind.capitalize() in std_kinds:
        return [kind.capitalize()]

    kind = kind.lower()
    # cutm
    if kind == 'trade mark': return ['Individual']
    if kind == 'certification': return ['Certificate']
    if kind == 'marca colectiva': return ['Collective']

    # crtm

    # cutm: the kind of mark is in the TransactionSubCode
      # <TransactionSubCode>Denom. de Origen (der. de uso)</TransactionSubC
      # <TransactionSubCode>Denom. de Origen (registro)</TransactionSubCode
      # <TransactionSubCode>Denominación de Origen Lisboa</TransactionSubCo
      # <TransactionSubCode>Emblema Empresarial</TransactionSubCode>
      # <TransactionSubCode>Lema Comercial</TransactionSubCode>
      # <TransactionSubCode>Marca Arreglo Madrid Des.Pos</TransactionSubCod
      # <TransactionSubCode>Marca Arreglo Madrid</TransactionSubCode>
      # <TransactionSubCode>Marca Art9Sexies Des.Pos.</TransactionSubCode>
      # <TransactionSubCode>Marca Art9Sexies</TransactionSubCode>
      # <TransactionSubCode>Marca Colectiva</TransactionSubCode>
      # <TransactionSubCode>Marca Protocolo Madrid Des.Pos</TransactionSubC
      # <TransactionSubCode>Marca Protocolo Madrid</TransactionSubCode>
      # <TransactionSubCode>Marca</TransactionSubCode>
      # <TransactionSubCode>Nombre Comercial</TransactionSubCode>
      # <TransactionSubCode>Rótulo de Establecimiento</TransactionSubCode>

    raise Exception('"%s" kind not mapped' % kind)

status_helper = MarkStatus()
def translate_status(trademark):
    return status_helper.dflt(trademark)

feature_helper = MarkFeature()
def translate_feature(feature, office):
    return feature_helper.dflt(feature, office)

events_helper = MarkEvent()
def translate_event(event, office):
    return events_helper.dflt(event, office)


