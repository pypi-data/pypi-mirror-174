from gbdtransformation.common.filters import remove_leading
from gbdtransformation.brands.filters import st13 as std_st13
from gbdtransformation.brands import features as std_features
from gbdtransformation.brands import status as std_status
from gbdtransformation.brands import events as std_events
from gbdtransformation.brands import kinds as std_kinds

# -------------------
# Per Office helpers
# -------------------
class DocType:
    def bntm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'
        if code == 'Trademark-Madrid': return 'TRADEMARK'

    def zmtm(self, code, subcode, trademark):
        if code == 'National Mark': return 'TRADEMARK'
        if code == 'Madrid Mark': return 'TRADEMARK'

    def aetm(self, code, subcode, trademark):
        if code == 'العلامات': return 'TRADEMARK'
        if code == 'طلب علامات وطني': return 'TRADEMARK'
        if code == 'علامات خدمة': return 'TRADEMARK'

    def altm(self, code, subcode, trademark):
        if code == 'Trademarks': return 'TRADEMARK'
        if code == 'National Mark Division': return 'TRADEMARK'
        if code == 'G. Indications': return 'AOP'

    def bhtm(self, code, subcode, trademark):
        if code == 'طلب علامات وطني': return 'TRADEMARK'
        if code == 'علامات خدمة': return 'TRADEMARK'

    def bttm(self, code, subcode, trademark):
        if code == 'National Marks': return 'TRADEMARK'
        if code == 'Madrid Marks': return 'TRADEMARK'
        if code == 'Prohibited Marks': return 'TRADEMARK'

    def bwtm(self, code, subcode, trademark):
        if code == 'National Marks': return 'TRADEMARK'
        if code == 'Madrid Marks': return 'TRADEMARK'
        if code == 'Banjul Protocol Marks': return 'TRADEMARK'

    def cltm(self, code, subcode, trademark):
        if code == 'Marca': return 'TRADEMARK'
        if code == 'Frase de propaganda': return 'TRADEMARK'
        if code == 'Marca colectiva': return 'TRADEMARK'
        if code == 'Marca de certificación': return 'TRADEMARK'
        if code == 'Indicación geográfica': return 'AOP'

    def crtm(self, code, subcode, trademark):
        if subcode == 'Emblema': return 'EMBLEM'
        if subcode == 'Denominación de origen': return 'AOP'
        if subcode == 'Indicaciones geográficas': return 'AOP'
        if code == 'Signo Distintivo': return 'TRADEMARK'

    def egtm(self, code, subcode, trademark):
        if code == 'علامة تجارية وطنية': return 'TRADEMARK'

    def jotm(self, code, subcode, trademark):
        if code == 'علامة تجارية': return 'TRADEMARK'

    def omtm(self, code, subcode, trademark):
        if code == 'علامة وطنية': return 'TRADEMARK'

    def dztm(self, code, subcode, trademark):
        if code == 'Marque Nationale': return 'TRADEMARK'
        if code == 'Marque Divisionelle': return 'TRADEMARK'

    def ghtm(self, code, subcode, trademark):
        if code == 'Marks': return 'TRADEMARK'
        if code == 'Madrid Marks': return 'TRADEMARK'

    def gmtm(self, code, subcode, trademark):
        if code == 'National Mark': return 'TRADEMARK'

    def idtm(self, code, subcode, trademark):
        if code == 'Merek Dagang': return 'TRADEMARK'
        if code == 'Merek Jasa': return 'TRADEMARK'
        if code == 'Merek Perpanjangan (R)': return 'TRADEMARK'
        if code == 'Merek Perpanjangan (V)': return 'TRADEMARK'
        if code == 'Trademark - Madrid (DCP)': return 'TRADEMARK'
        if code == 'Merek Kolektif': return 'TRADEMARK'

    def ketm(self, code, subcode, trademark):
        if code == 'Trade Marks': return 'TRADEMARK'
        if code == 'Madrid Marks': return 'TRADEMARK'
        if code == 'Service Marks': return 'TRADEMARK'

    def khtm(self, code, subcode, trademark):
        if code == 'Madrid Designated': return 'TRADEMARK'
        if subcode == 'Domestic Trademark': return 'TRADEMARK'
        if subcode == 'Domestic Service Mark': return 'TRADEMARK'
        if subcode == 'Foreign Trademark': return 'TRADEMARK'
        if subcode == 'Foreign Service Mark': return 'TRADEMARK'
        # a safe guess
        return 'TRADEMARK'

    def kwtm(self, code, subcode, trademark):
        if code == 'علامة تجارية': return 'TRADEMARK'

    def latm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'
        if code == 'Trademark - Madrid': return 'TRADEMARK'

    def mgtm(self, code, subcode, trademark):
        if code == 'Marques Nationales': return 'TRADEMARK'
        if code == 'Marques Madrid': return 'TRADEMARK'
        if code == 'Noms Commerciaux': return 'TRADEMARK'

    def mntm(self, code, subcode, trademark):
        if subcode == 'Гэрчлэх тэмдэг': return 'AOP'
        if code == 'Trademark': return 'TRADEMARK'
        if code == 'Trademark - Madrid': return 'TRADEMARK'

    def mwtm(self, code, subcode, trademark):
        if code == 'National Trademarks': return 'TRADEMARK'

    def mytm(self, code, subcode, trademark):
        if code == 'TRADE MARK': return 'TRADEMARK'
        if code == 'CERTIFICATION': return 'TRADEMARK'
        if code == 'DEFENSIVE': return 'TRADEMARK'

    def mztm(self, code, subcode, trademark):
        if code == 'Insignia': return 'EMBLEM'
        if code == 'Indicacao Geografica': return 'AOP'
        if code == 'Marca Nacional': return 'TRADEMARK'
        if code == 'Marca Madrid': return 'TRADEMARK'
        if code == 'Logotipo': return 'TRADEMARK'
        if code == 'Nome Comercial': return 'TRADEMARK'

    def natm(self, code, subcode, trademark):
        if code == 'National Trademarks': return 'TRADEMARK'
        if code == 'Madrid Marks': return 'TRADEMARK'
        if code == 'Banjul Trademark': return 'TRADEMARK'
        if code == 'DEFENSIVE MARK': return 'TRADEMARK'

    def pgtm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'

    def rstm(self, code, subcode, trademark):
        if code == 'Trademark Individual': return 'TRADEMARK'
        if code == 'Trademark Collective': return 'TRADEMARK'
        if code == 'Trademark Certification': return 'TRADEMARK'

    def sdtm(self, code, subcode, trademark):
        if code == 'علامة تجارية': return 'TRADEMARK'

    def smtm(self, code, subcode, trademark):
        if subcode == 'Marchi Prodotti e Servizi': return 'TRADEMARK'
        if subcode == 'Marchi Collettivi': return 'TRADEMARK'

    def sztm(self, code, subcode, trademark):
        if code == 'National TradeMarks': return 'TRADEMARK'
        if code == 'Madrid': return 'TRADEMARK'

    def thtm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'
        if code == 'Service mark': return 'TRADEMARK'
        if code == 'Certificate mark': return 'TRADEMARK'
        if code == 'Collective mark': return 'TRADEMARK'

    def tntm(self, code, subcode, trademark):
        if code == 'Marque Madrid': return 'TRADEMARK'
        if code == 'Marque Nationale': return 'TRADEMARK'
        if code == 'Marque Nationale Online': return 'TRADEMARK'
        if code == 'Marque Etrangere': return 'TRADEMARK'
        if code == 'Marque Divisionelle': return 'TRADEMARK'

    def totm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'

    def vntm(self, code, subcode, trademark):
        if code == 'TradeMark': return 'TRADEMARK'
        # sometimes they miss it, but otherwise data is complete
        kind = trademark.KindMark
        if kind: return 'TRADEMARK'

    def wstm(self, code, subcode, trademark):
        if code == 'Trademark': return 'TRADEMARK'
        if code == 'Trademark - Madrid': return 'TRADEMARK'

    def zwtm(self, code, subcode, trademark):
        if code == 'National TradeMarks': return 'TRADEMARK'
        if code == 'Zimbabwe': return 'TRADEMARK'
        if code == 'Madrid': return 'TRADEMARK'
        if code == 'Banjul Protocol Marks': return 'TRADEMARK'

    def cutm(self, code, subcode, trademark):
        if code == 'M': return 'TRADEMARK'
        if code == 'L': return 'TRADEMARK'
        if code == 'N': return 'TRADEMARK'
        if code == 'R': return 'TRADEMARK'
        if code == 'D': return 'AOP'
        if code == 'E': return 'EMBLEM'

    def dflt(self, code, subcode, trademark):

        office = trademark.RegistrationOfficeCode

        # none of the standard one matches
        # => see in a specific one
        coll_helper_value = getattr(self, '%stm' % office.lower())(code, subcode, trademark)

        if not coll_helper_value:
            raise Exception('DocType not mapped for Collection [%s][code: %s][subcode: %s]' %
                    (office, code, subcode))

        return coll_helper_value

class MarkKind:
    def bntm(self, code, subcode, trademark):
        if subcode == 'Normal Mark': return ['Individual']
        if subcode == 'Trademark-Madrid': return  ['Individual']
        if subcode == 'Merger Mark': return  ['Individual']

    def aetm(self, code, subcode, trademark):
        if subcode == 'سلع أو خدمات': return ['Individual']
        if subcode == 'فحص ومراقبة': return ['Individual']
        if subcode == 'علامة جماعية': return ['Collective']

    #TODO: verify with office
    def altm(self, code, subcode, trademark):
        subcode = subcode.lower()

        if subcode == 'goods mark': return ['Individual']
        if subcode == 'goods and services mark': return ['Individual']
        if subcode == 'marke individuale': return ['Individual']
        if subcode == 'service mark': return ['Individual']

        if subcode == 'marke kolektive': return ['Collective']
        if subcode == 'marke certifikuese': return ['Certificate']

        # designation of origin
        if subcode == 'tregues gjeografik': return ['Other']
        if subcode == 'emertim origjine': return ['Other']

        # application-brand division
        if subcode == 'ndarje e aplikimit-marke': return ['Other']
        # partial-brand transfer
        if subcode == 'transferim i pjesshem-marke': return ['Other']
        # transformation - national marker
        if subcode == 'transformim-markenderkombetare': return ['Other']

    def bhtm(self, code, subcode, trademark):
        if subcode == 'سلع وخدمات': return ['Individual']
        if subcode == 'سلع وخدمات - خدمة': return ['Individual']
        if subcode == 'علامة جماعية': return ['Collective']

    def bttm(self, code, subcode, trademark):
        if code == 'National Marks': return ['Individual']
        if code == 'Madrid Marks': return ['Individual']
        if code == 'Prohibited Marks': return ['Individual']

    def bwtm(self, code, subcode, trademark):
        if code == 'National Marks': return ['Individual']
        if code == 'Madrid Marks': return ['Individual']
        if code == 'Banjul Protocol Marks': return ['Individual']

    def cltm(self, code, subcode, trademark):
        if code == 'Marca': return ['Individual']
        if code == 'Marca colectiva': return ['Collective']
        if code == 'Marca de certificación': return ['Certificate']
        if code == 'Indicación geográfica': return ['Other']
        if code == 'Frase de propaganda': return ['Other']

    def crtm(self, code, subcode, trademark):
        subcode = subcode.lower()
        if subcode == 'marca de fábrica y servicios': return ['Individual']
        if subcode == 'marca de fábrica y comercio': return ['Individual']
        if subcode == 'marca de comercio y servicios': return ['Individual']
        if subcode == 'marca de fábrica': return ['Individual']
        if subcode == 'marca de servicios': return ['Individual']
        if subcode == 'marca de comercio': return ['Individual']
        if subcode == 'nombre comercial': return ['Individual']
        if subcode == 'señal de publicidad comercial': return ['Individual']

        if subcode == 'marca colectiva': return ['Collective']
        if subcode == 'marca de certificación': return ['Certificate']

        if subcode == 'señal de propaganda': return ['Other']
        if subcode == 'denominación de origen': return ['Other']
        if subcode == 'emblema': return ['Other']
        if subcode == 'indicaciones geográficas': return ['Other']


    def egtm(self, code, subcode, trademark):
        if subcode == 'طلب علامات وطني': return ['Individual']
        if subcode == 'طلب وطني مودع بالادارة': return ['Individual']

    def jotm(self, code, subcode, trademark):
        if subcode == 'طلب علامات': return ['Individual']

    def omtm(self, code, subcode, trademark):
        if subcode == 'علامة وطنية': return ['Individual']

    def dztm(self, code, subcode, trademark):
        if subcode == 'Nationale Prod & Services': return ['Individual']
        if subcode == 'Nationale Collective': return ['Collective']
        if code == 'Marque Divisionelle': return ['Other']

    def ghtm(self, code, subcode, trademark):
        if subcode == 'Trademarks': return ['Individual']
        if subcode == 'Service Marks': return ['Individual']
        if subcode == 'Madrid Protocol': return ['Individual']
        if subcode == 'Defensive Marks': return ['Defensive']

    def gmtm(self, code, subcode, trademark):
        if subcode == 'Trademark': return ['Individual']
        if subcode == 'Certification Mark': return ['Certificate']

    def idtm(self, code, subcode, trademark):
        kind = trademark.KindMark
        # out-of-the-box match
        if kind.capitalize() in std_kinds:
            return [kind.capitalize()]

    def ketm(self, code, subcode, trademark):
        if code == 'Trade Marks': return ['Individual']
        if code == 'Madrid Marks': return ['Individual']
        if code == 'Service Marks': return ['Individual']

    def khtm(self, code, subcode, trademark):
        if code == 'Madrid Designated': return ['Individual']
        if subcode == 'Domestic Trademark': return ['Individual']
        if subcode == 'Domestic Service Mark': return ['Individual']
        if subcode == 'Foreign Trademark': return ['Individual']
        if subcode == 'Foreign Service Mark': return ['Individual']
        return ['Other']

    def kwtm(self, code, subcode, trademark):
        if subcode == 'طلب علامة سلع وخدمات': return ['Individual']
        if subcode == 'علامة جماعية': return ['Collective']
        if subcode == 'طلب علامة مراقبة': return ['Certificate']

    def latm(self, code, subcode, trademark):
        if code == 'Trademark': return ['Individual']
        if subcode == 'Trademark - Madrid': return ['Individual']

    def mgtm(self, code, subcode, trademark):
        if subcode == 'Marque Nationale Individuelle': return ['Individual']
        if subcode == 'Marque Nationale Collective': return ['Collective']
        if subcode == 'Protocole Madrid': return ['Individual']
        if subcode == 'Noms Commerciaux': return ['Certificate']

    def mntm(self, code, subcode, trademark):
        if subcode == 'Trademark - Madrid': return ['Individual']
        if subcode == 'Барааны тэмдэг': return ['Individual']
        # Testimony
        if subcode == 'Гэрчлэх тэмдэг': return ['Certificate']
        # Geographical indication
        if subcode == 'Газар зүйн заалт': return ['Other']
        # Collective Symbol
        if subcode == 'Хамтын тэмдэг': return ['Collective']

        return ['Other']

    def mwtm(self, code, subcode, trademark):
        if subcode == 'Trade Mark': return ['Individual']
        if subcode == 'Service Mark': return ['Individual']
        if subcode == 'Part A': return ['Individual']

    def mytm(self, code, subcode, trademark):
        if code == 'TRADE MARK': return ['Individual']
        if code == 'CERTIFICATION': return ['Certificate']
        if code == 'DEFENSIVE': return ['Defensive']

    def mztm(self, code, subcode, trademark):
        if subcode == 'Marca': return ['Individual']
        if subcode == 'Madrid Protocol': return ['Individual']
        if subcode == 'Madrid Agreement': return ['Individual']
        if subcode == 'Marca Colectiva': return ['Collective']
        if subcode == 'Marca de Certificacao': return ['Certificate']

        if subcode == 'Nomes': return ['Certificate']
        if subcode == 'Logotipo': return ['Other']
        if subcode == 'Indicacao Geografica': return ['Other']
        if subcode == 'Insignia': return ['Other']

    def natm(self, code, subcode, trademark):
        if subcode == 'PART A': return ['Individual']
        if subcode == 'PART B': return ['Individual']
        if subcode == 'Banjul Trademark': return ['Individual']
        if subcode == 'Madrid Protocol': return ['Individual']
        if subcode == 'Madrid Agreement': return ['Individual']
        if subcode == 'DEFENSIVE MARK': return ['Defensive']

    def pgtm(self, code, subcode, trademark):
        if subcode == 'Part A': return ['Individual']
        if subcode == 'Part B': return ['Individual']

    def rstm(self, code, subcode, trademark):
        if code == 'Trademark Individual': return ['Individual']
        if code == 'Trademark Collective': return ['Collective']
        if code == 'Trademark Certification': return ['Certificate']

    def sdtm(self, code, subcode, trademark):
        if subcode == 'طلب علامات وطني': return ['Individual']

    def smtm(self, code, subcode, trademark):
        if subcode == 'Marchi Prodotti e Servizi': return ['Individual']
        if subcode == 'Marchi Collettivi': return ['Collective']

    def sztm(self, code, subcode, trademark):
        if subcode == 'National Marks': return ['Individual']
        if subcode == 'Madrid Protocol': return ['Individual']
        if subcode == 'Madrid Agreement': return ['Individual']

    def thtm(self, code, subcode, trademark):
        kind = trademark.KindMark
        # out-of-the-box match
        if kind.capitalize() in std_kinds:
            return [kind.capitalize()]

        if code == 'Collective mark': return ['Collective']

    def tntm(self, code, subcode, trademark):
        if subcode == 'Protocole Madrid': return ['Individual']
        if subcode == 'Nationale Prod & Services': return ['Individual']
        if subcode == 'Nationale Collective': return ['Collective']
        if subcode == 'Nationale Collective Online': return ['Collective']
        if subcode == 'Etrangere Prod & Services': return ['Individual']
        if subcode == 'Etrangere Collective': return ['Collective']
        if subcode == 'Divisionelle Produit/Service': return ['Other']

    def totm(self, code, subcode, trademark):
        kind = trademark.KindMark
        # out-of-the-box match
        if kind.capitalize() in std_kinds:
            return [kind.capitalize()]

    def vntm(self, code, subcode, trademark):
        kind = trademark.KindMark
        # out-of-the-box match
        if kind.capitalize() in std_kinds:
            return [kind.capitalize()]

    def wstm(self, code, subcode, trademark):
        kind = trademark.KindMark
        # out-of-the-box match
        if kind.capitalize() in std_kinds:
            return [kind.capitalize()]

    def zmtm(self, code, subcode, trademark):
        if subcode == 'Trademark': return ['Individual']
        if subcode == 'Servicemark': return ['Individual']
        if subcode == 'Certification Mark': return ['Certificate']

    def zwtm(self, code, subcode, trademark):
        if subcode == 'Part A': return ['Individual']
        if subcode == 'Part B': return ['Individual']
        if subcode == 'Part C': return ['Individual']
        if subcode == 'Part D': return ['Individual']
        if subcode == 'National Trademarks': return ['Individual']
        if subcode == 'Madrid Protocol': return ['Individual']
        if subcode == 'Banjul Protocol Marks': return ['Individual']

    def cutm(self, code, subcode, trademark):
        if code == 'M': return ['Individual']
        if code == 'L': return ['Individual'] # commercial phrase
        if code == 'N': return ['Certificate'] # commercial certificate
        if code == 'R': return ['Certificate'] # Establishement label
        if code == 'E': return ['Other'] # Emblem
        if code == 'D': return ['Other'] # AOP

    def dflt(self, code, subcode, trademark):
        office = trademark.RegistrationOfficeCode

        coll_helper_value = getattr(self, '%stm' % office.lower())(code, subcode, trademark)

        if not coll_helper_value:
            raise Exception('MarkKind not mapped for Collection [%s][code: %s][subcode: %s]'
                    % (office, code, subcode))
        return coll_helper_value

class MadRef:
    def wstm(self, trademark):
        # ex: WS/M/990411
        return trademark.ApplicationNumber.split('/')[-1]

    def natm(self, trademark):
        # ex: D/D/990411
        return trademark.ApplicationNumber.split('/')[-1]

    def ghtm(self, trademark):
        # ex: MD/M/1/1341864
        return trademark.ApplicationNumber.split('/')[-1]

    def mztm(self, trademark):
        # ex: MD/D/1/1341864
        return trademark.ApplicationNumber.split('/')[-1]

    def sztm(self, trademark):
        # ex: MD/D/1/1341864
        return trademark.ApplicationNumber.split('/')[-1]

    def cutm(self, trademark):
        # ex: CM/A/1/742990
        return trademark.ApplicationNumber.split('/')[-1]

    def khtm(self, trademark):
        # ex: KH/673426/M
        return trademark.ApplicationNumber.split('/')[1]

    def latm(self, trademark):
        # ex: M/1350065
        return trademark.ApplicationNumber.split('/')[-1]

    def mgtm(self, trademark):
        # ex: MG/D/1/1050968
        return trademark.ApplicationNumber.split('/')[-1]

    def bntm(self, trademark):
        # ex: 1411871
        return trademark.ApplicationNumber

    def bttm(self, trademark):
        # ex: BT/M/1010001
        return trademark.ApplicationNumber.split('/')[-1]

    def tntm(self, trademark):
        # ex: TN/M/100/673426
        return trademark.ApplicationNumber.split('/')[-1]

    def zwtm(self, trademark):
        # ex: MD/D/1/1380029
        return trademark.ApplicationNumber.split('/')[-1]

    def mntm(self, trademark):
        # ex: 40-M-0673426
        return remove_leading(trademark.ApplicationNumber.split('-')[-1], '0')

    def bwtm(self, trademark):
        # ex: MD/D/0/1151297
        return trademark.ApplicationNumber.split('/')[-1]

    def ketm(self, trademark):
        # ex: IB/D/1/1020123
        return trademark.ApplicationNumber.split('/')[-1]

    def idtm(self, trademark):
        # ex: M0020181390000
        return trademark.ApplicationNumber[7:]

    def thtm(self, trademark):
        # <wo:MarkEventCode>Madrid Designation</wo:MarkEventCode>
        # <wo:OfficeSpecificMarkEventName>IRN:1504436</wo:OfficeSpecificMarkEventName>
        events = trademark.MarkEventDetails.MarkEvent
        for event in events:
            event_name = event.OfficeSpecificMarkEventName
            if event_name.startswith('IRN:'):
                return event_name.replace('IRN:', '')

    def mytm(self, trademark):
        raise Exception('MY does not send information about being and international filing')

    def pgtm(self, trademark):
        raise Exception('PG is not a member of madrid protocol!')

    def totm(self, trademark):
        raise Exception('TO is not a member of madrid protocol!')

    def dflt(self, trademark):
        raise Exception('Need a MadRef helper for Collection. appnum [%s]' % trademark.ApplicationNumber)


class MarkFeature:

    def crtm(self, feature):
        if feature == 'M' or feature == 'Mixta': return 'Combined'
        if feature == 'F' or feature == 'Figurativa': return 'Figurative'
        if feature == 'D' or feature == 'Denominativa': return 'Word'
        if feature == 'T' or feature == 'Tridimensional': return 'Three dimensional'
        if feature == 'O': return 'Other'
        if feature == 'S': return 'Sound'

    def rstm(self, feature):
        if feature == 'F': return 'Figurative'

    def egtm(self, feature):
        if feature == 'M': return 'Combined'

    def cutm(self, feature):
        if feature == 'Mixta': return 'Combined'
        if feature == 'Figurativa': return 'Figurative'
        if feature == 'Denominativa': return 'Word'
        if feature == 'Tridimensional': return 'Three dimensional'

    def smtm(self, feature):
        if feature == 'Marchi Nazionale (Name only)': return 'Word'
        if feature == 'Marchi Nazionale (Both Name and Logo)': return 'Combined'
        if feature == 'Marchi Nazionale (Logo only)': return 'Figurative'
        if feature == 'Marchi Nazionale (Tridimensional)': return 'Three dimensional'
        if feature == 'Marchi Nazionale (Sound)': return 'Sound'

    def idtm(self, feature):
        feature = feature.lower()
        if feature == 'both name and logo': return 'Combined'
        if feature == 'name only': return 'Word'

    def mytm(self, feature):
        feature = feature.lower()
        if feature == 'stylish': return 'Stylized characters'
        if feature == 'image': return 'Figurative'
        if feature == 'shape': return 'Figurative'
        if feature == 'not defined': return 'Undefined'
        if feature == 'anycombination': return 'Undefined'

    def dflt(self, feature, office):
        # we will not guess when the office
        # does not provide a value
        if not feature: return 'Undefined'

        if feature == '3-D': return 'Three dimensional'
        if feature == 'Three Dimensional': return 'Three dimensional'

        feature_c = feature.capitalize()

        if feature_c in std_features:
            return feature_c

        # none of the standard one matches
        # => see in a specific one
        try:
            coll_helper_value = getattr(self, '%stm' % office.lower())(feature)
            if coll_helper_value:
                return coll_helper_value
            else:
                raise Exception('MarkFeature not mapped for Collection [%s][feature: %s]' % (office, feature))
        except:
            raise Exception('Need a MarkFeature helper for Collection [%s][feature: %s]' % (office, feature))


class MarkStatus:
    # special cases for crtm
    def crtm(self, status, tm=None):
        status_map = {
            'Con plazo de gracia antes de caducidad': 'Registered',
            'Registered': 'Registered',
            'Registrada': 'Registered',
            'Con edicto publicado': 'Pending',
            'Con edicto para acumular': 'Pending',
            'Con edicto': 'Pending',
            'Con prevención (en examen)': 'Pending',
            'Con prevención (en inscripción)': 'Pending',
            'Con prevencion (en inscripción)': 'Pending',
            'Con prevención (en oposición)': 'Pending',
            'Con resolución de archivo': 'Pending',
            'Con resolución denegatoria': 'Pending',
            'Con resolución de oposición con lugar parcialmente': 'Pending',
            'Con resolución de oposición con lugar': 'Pending',
            'Con resolución de oposición sin lugar': 'Pending',
            'Con suspención de oficio': 'Pending',
            'Con suspensión de oficio (en examen)': 'Pending',
            'Con suspensión de oficio (en inscripción)': 'Pending',
            'Con suspensión de oficio (en oposición)': 'Pending',
            'Con gestoría de negocios': 'Pending',
            'Con prevención (para traslado)': 'Pending',
            'Con prevención de admisibilidad': 'Pending',
            'Con resolución denegatoria parcial': 'Pending',
            'Con suspenso a pedido de parte': 'Pending',
            'Denegada parcialmente': 'Pending',
            'Dividida': 'Pending',
            'En análisis de resolución anulada': 'Pending',
            'En examen': 'Pending',
            'En inscripción': 'Pending',
            'En oposición (con traslado)': 'Pending',
            'En oposición (examen fondo)': 'Pending',
            'En oposición (para traslado)': 'Pending',
            'Historia: anulada resol. reg. por tribunal': 'Pending',
            'Historia: con prevención': 'Pending',
            'Historia: con prevención art.14': 'Pending',
            'Historia: con suspenso': 'Pending',
            'Historia: continua trámite luego revoc/apel': 'Pending',
            'Historia: expediente con resolución': 'Pending',
            'Historia: pendiente de pago': 'Pending',
            'Historia: solicitud con edicto': 'Pending',
            'Historia: Edicto publicado': 'Pending',
            'Historia: En Tribunal': 'Pending',
            'Para abandonar por no publicación': 'Pending',
            'Para Denegar': 'Pending',
            'Para desistir': 'Pending',
            'Para repartir (oposición no recibida)': 'Pending',
            'Para repartir (oposición recibida)': 'Pending',
            'Para repartir (suspenso en exam.oposic finalizado)': 'Pending',
            'Para repartir (suspenso en inscripción finalizado)': 'Pending',
            'Para repartir': 'Pending',
            'Para repartir (edicto no publicado)': 'Pending',
            'Para repartir (nueva marca)': 'Pending',
            'Para repartir (suspenso en examen finalizado)': 'Pending',
            'Para validar rechazo de plano (historia)': 'Pending',
            'Status inicial': 'Pending',
            'Plazo vencido (edicto)': 'Pending',
            'Plazo vencido (gracia caducidad)': 'Pending',
            'Plazo vencido (oposiciones)': 'Pending',
            'Plazo vencido (suspenso a pedido de parte)': 'Pending',
            'Resolución oposición para firma': 'Pending',
            'Abandoned': 'Ended',
            'Anulada': 'Ended',
            'Archivada': 'Ended',
            'Cancelada': 'Ended',
            'Cancelado por error de recepción': 'Ended',
            'Denegada': 'Ended',
            'Desistida': 'Ended',
            'Historia: Status especial en Fox': 'Ended',
            'Historia: desistida por no pago': 'Ended',
            'Invalidated': 'Ended',
            'Rechazada': 'Ended',
            'Rechazada (historia)': 'Ended',
            'Rejected': 'Ended',
            'Withdrawn': 'Ended',
            'Expired': 'Expired'
        }

        return status_map.get(status, 'Unknown')

    def cutm(self, status, tm=None):
        if status in ['INI', 'MIGR', '236']:
            raise Exception('File should not be imported [cutm.%s]' % status)

    def jotm(self, status, tm=None):
        if status == '3923': return 'Unknown'

    def bntm(self, status, tm=None):
        if status == 'M009': return 'Unknown'

    def rstm(self, status, tm=None):
        if status == '2285': return 'Unknown'

    def mgtm(self, status, tm=None):
        if status == '1748': return 'Unknown'

    def dztm(self, status, tm=None):
        if status == '3860': return 'Unknown'

    # special cases for TOTM
    def totm(self, status, tm=None):
        if status == '1058': return 'Unknown'
        if status == '1014': return 'Unknown'

    def gmtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def zmtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def natm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def mztm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def ghtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def cltm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def zwtm(self, status, tm=None):
        return self.gmtm(status, tm=tm)
    def bwtm(self, status, tm=None):
        return self.gmtm(status, tm=tm)
    def ketm(self, status, tm=None):
        return self.gmtm(status, tm=tm)

    def thtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def mntm(self, status, tm=None):
        if status == 'T025': return 'Unknown'
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def latm(self, status, tm=None):
        if status == 'Inactive':
            if tm.ExpiryDate:
                return 'Expired'
            else:
                return 'Ended'

    def khtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def mwtm(self, status, tm=None):
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def wstm(self, status, tm=None):
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def mytm(self, status, tm=None):
        if status == '672': return 'Unknown'
        if status == '826': return 'Unknown'
        if status == 'Suspended': return 'Ended'
        if status == 'Inactive':
            if tm.RegistrationDate:
                return 'Expired'
            else:
                return 'Ended'

    def altm(self, status, tm=None):
        if status == '2295': return 'Unknown'
        if status == '2353': return 'Unknown'
        if status == 'Suspended': return 'Ended'

    def dflt(self, trademark):
        office = trademark.RegistrationOfficeCode
        status = trademark.MarkCurrentStatusCode
        if not status: return 'Unknown'

        status_c = status.capitalize()
        if status_c in std_status:
            return status_c

        status_l = status.lower()

        # Pending
        if status_l == 'pending': return 'Pending'
        if status_l == 'opposed': return 'Pending'
        if status_l == 'filed': return 'Pending'
        if status_l == 'published': return 'Pending'
        if status_l == 'application published': return 'Pending'
        if status_l == 'examined': return 'Pending'
        if status_l == 'appealed': return 'Pending'
        if status_l == 'awaiting court action': return 'Pending'

        # Ended
        if status_l == 'application cancelled': return 'Ended'
        if status_l == 'withdrawn': return 'Ended'
        if status_l == 'abandoned': return 'Ended'
        if status_l == 'rejected': return 'Ended'
        if status_l == 'invalidated': return 'Ended'
        if status_l == 'surrendered': return 'Ended'

        # Expired
        if status_l == 'expired': return 'Expired'

        # Registered
        if status_l == 'active': return 'Registered'
        if status_l == 'registered': return 'Registered'

        # none of the standard one matches
        # => see in a specitic one
        coll_helper_value = getattr(self, '%stm' % office.lower())(status, tm=trademark)
        if coll_helper_value:
            return coll_helper_value
        else:
            raise Exception('MarkStatus not mapped for Collection [%s][status: %s]' % (office, status))

class MarkEvent:
    def crtm(self, event):
        return 'Unknown'

    def bntm(self, event):
        if event == 'M009': return 'Unknown'

    def jotm(self, event):
        if event == '3923': return 'Unknown'

    def vntm(self, event):
        if event == 'Notificationd': return 'Notification'

    def mytm(self, event):
        if event == '672': return 'Unknown'

    def wstm(self, event):
        if event == 'M009': return 'Unknown'

    def mntm(self, event):
        if event == 'T025': return 'Unknown'

    def gmtm(self, event):
        if event == 'Active': return 'Registered'

    def zmtm(self, event):
        if event == 'Active': return 'Registered'

    def sztm(self, event):
        if event == 'Active': return 'Registered'

    def natm(self, event):
        if event == 'Active': return 'Registered'

    def mztm(self, event):
        if event == 'Active': return 'Registered'

    def mwtm(self, event):
        if event == 'Active': return 'Registered'

    def ghtm(self, event):
        if event == 'Active': return 'Registered'

    def cltm(self, event):
        if event == 'Active': return 'Registered'

    def zwtm(self, event):
        if event == 'Active': return 'Registered'

    def bwtm(self, event):
        if event == 'Active': return 'Registered'

    def ketm(self, event):
        if event == 'Active': return 'Registered'

    def mgtm(self, event):
        if event == 'Active': return 'Registered'
        if event == '1748': return 'Unknown'

    def rstm(self, event):
        if event == '255': return 'Unknown'
        if event == 'Поднет': return 'Filed'
        if event == 'Објављен': return 'Published'
        if event == 'Пред објавом': return 'Examined'
        if event == 'У поступку': return 'Pending'
        if event == 'Регистрован': return 'Registered'
        if event == 'Истекао': return 'Expired'
        if event == 'Одбијен': return 'Rejected'
        if event == 'Повучен': return 'Withdrawn'

    def dztm(self, status, tm=None):
        if status == '3860': return 'Unknown'

    def wstm(self, event):
        if event == 'M009': return 'Unknown'

    def cutm(self, event):
        if event == '236': return 'Unknown'
        if event == 'INI': return 'Unknown'
        if event == 'MIGR': return 'Unknown'


    def totm(self, event):
        if event == '1058': return 'Unknown'
        if event == '1014': return 'Unknown'

    def thtm(self, event):
        if event == 'Madrid Designation': return 'Registered'

    def dflt(self, event, office):
        if not event:
            return None

        event_c = event.capitalize()
        if event_c in std_events:
            return event_c

        event_l = event.lower()
        try:
            coll_helper_value = getattr(self, '%stm' % office.lower())(event)
            if coll_helper_value:
                return coll_helper_value
            else:
                raise Exception('MarkEvent not mapped for Collection [%s][event: %s]' % (office, event))
        except:
            raise Exception('Need a MarkEvent helper for Collection [%s][event: %s]' % (office, event))

