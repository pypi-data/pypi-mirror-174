from enum import Enum

from wedeliver_core.helpers.service_config import ServiceConfig


class Service:
    CAPTAIN = ServiceConfig('CAPTAIN_SERVICE')
    FINANCE = ServiceConfig('FINANCE_SERVICE')
    SDD = ServiceConfig('SDD_SERVICE')
    SUPPLIER = ServiceConfig('SUPPLIER_SERVICE')
    PN = ServiceConfig('PN_SERVICE')
    FINTECH = ServiceConfig('FINTECH_SERVICE')
    STC = ServiceConfig('STC_SERVICE')
    AUTH = ServiceConfig('AUTH_SERVICE')
    MAIL = ServiceConfig('MAIL_SERVICE')
    SMS = ServiceConfig('SMS_SERVICE')
    APILAYER = ServiceConfig('APILAYER_SERVICE')
    INVOICE = ServiceConfig('INVOICE_SERVICE')
    ADDRESS = ServiceConfig('ADDRESS_SERVICE')
    PUBLIC = ServiceConfig('PUBLIC_SERVICE')
    INTERNAL_NOTIFICATION = ServiceConfig('INTERNAL_NOTIFICATION_SERVICE')


class QueryTypes(Enum):
    SIMPLE_TABLE = 1
    FUNCTION = 2
    SEARCH = 3
