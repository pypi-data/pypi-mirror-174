# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'IntegrationConnectorType',
    'IntegrationMarketoConnectorOperator',
    'IntegrationOperatorPropertiesKeys',
    'IntegrationS3ConnectorOperator',
    'IntegrationSalesforceConnectorOperator',
    'IntegrationScheduledTriggerPropertiesDataPullMode',
    'IntegrationServiceNowConnectorOperator',
    'IntegrationTaskType',
    'IntegrationTriggerType',
    'IntegrationZendeskConnectorOperator',
    'ObjectTypeFieldContentType',
    'ObjectTypeKeyStandardIdentifiersItem',
]


class IntegrationConnectorType(str, Enum):
    SALESFORCE = "Salesforce"
    MARKETO = "Marketo"
    SERVICE_NOW = "ServiceNow"
    ZENDESK = "Zendesk"
    S3 = "S3"


class IntegrationMarketoConnectorOperator(str, Enum):
    PROJECTION = "PROJECTION"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    BETWEEN = "BETWEEN"
    ADDITION = "ADDITION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION"
    SUBTRACTION = "SUBTRACTION"
    MASK_ALL = "MASK_ALL"
    MASK_FIRST_N = "MASK_FIRST_N"
    MASK_LAST_N = "MASK_LAST_N"
    VALIDATE_NON_NULL = "VALIDATE_NON_NULL"
    VALIDATE_NON_ZERO = "VALIDATE_NON_ZERO"
    VALIDATE_NON_NEGATIVE = "VALIDATE_NON_NEGATIVE"
    VALIDATE_NUMERIC = "VALIDATE_NUMERIC"
    NO_OP = "NO_OP"


class IntegrationOperatorPropertiesKeys(str, Enum):
    VALUE = "VALUE"
    VALUES = "VALUES"
    DATA_TYPE = "DATA_TYPE"
    UPPER_BOUND = "UPPER_BOUND"
    LOWER_BOUND = "LOWER_BOUND"
    SOURCE_DATA_TYPE = "SOURCE_DATA_TYPE"
    DESTINATION_DATA_TYPE = "DESTINATION_DATA_TYPE"
    VALIDATION_ACTION = "VALIDATION_ACTION"
    MASK_VALUE = "MASK_VALUE"
    MASK_LENGTH = "MASK_LENGTH"
    TRUNCATE_LENGTH = "TRUNCATE_LENGTH"
    MATH_OPERATION_FIELDS_ORDER = "MATH_OPERATION_FIELDS_ORDER"
    CONCAT_FORMAT = "CONCAT_FORMAT"
    SUBFIELD_CATEGORY_MAP = "SUBFIELD_CATEGORY_MAP"


class IntegrationS3ConnectorOperator(str, Enum):
    PROJECTION = "PROJECTION"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    BETWEEN = "BETWEEN"
    LESS_THAN_OR_EQUAL_TO = "LESS_THAN_OR_EQUAL_TO"
    GREATER_THAN_OR_EQUAL_TO = "GREATER_THAN_OR_EQUAL_TO"
    EQUAL_TO = "EQUAL_TO"
    NOT_EQUAL_TO = "NOT_EQUAL_TO"
    ADDITION = "ADDITION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION"
    SUBTRACTION = "SUBTRACTION"
    MASK_ALL = "MASK_ALL"
    MASK_FIRST_N = "MASK_FIRST_N"
    MASK_LAST_N = "MASK_LAST_N"
    VALIDATE_NON_NULL = "VALIDATE_NON_NULL"
    VALIDATE_NON_ZERO = "VALIDATE_NON_ZERO"
    VALIDATE_NON_NEGATIVE = "VALIDATE_NON_NEGATIVE"
    VALIDATE_NUMERIC = "VALIDATE_NUMERIC"
    NO_OP = "NO_OP"


class IntegrationSalesforceConnectorOperator(str, Enum):
    PROJECTION = "PROJECTION"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    CONTAINS = "CONTAINS"
    BETWEEN = "BETWEEN"
    LESS_THAN_OR_EQUAL_TO = "LESS_THAN_OR_EQUAL_TO"
    GREATER_THAN_OR_EQUAL_TO = "GREATER_THAN_OR_EQUAL_TO"
    EQUAL_TO = "EQUAL_TO"
    NOT_EQUAL_TO = "NOT_EQUAL_TO"
    ADDITION = "ADDITION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION"
    SUBTRACTION = "SUBTRACTION"
    MASK_ALL = "MASK_ALL"
    MASK_FIRST_N = "MASK_FIRST_N"
    MASK_LAST_N = "MASK_LAST_N"
    VALIDATE_NON_NULL = "VALIDATE_NON_NULL"
    VALIDATE_NON_ZERO = "VALIDATE_NON_ZERO"
    VALIDATE_NON_NEGATIVE = "VALIDATE_NON_NEGATIVE"
    VALIDATE_NUMERIC = "VALIDATE_NUMERIC"
    NO_OP = "NO_OP"


class IntegrationScheduledTriggerPropertiesDataPullMode(str, Enum):
    INCREMENTAL = "Incremental"
    COMPLETE = "Complete"


class IntegrationServiceNowConnectorOperator(str, Enum):
    PROJECTION = "PROJECTION"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    CONTAINS = "CONTAINS"
    BETWEEN = "BETWEEN"
    LESS_THAN_OR_EQUAL_TO = "LESS_THAN_OR_EQUAL_TO"
    GREATER_THAN_OR_EQUAL_TO = "GREATER_THAN_OR_EQUAL_TO"
    EQUAL_TO = "EQUAL_TO"
    NOT_EQUAL_TO = "NOT_EQUAL_TO"
    ADDITION = "ADDITION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION"
    SUBTRACTION = "SUBTRACTION"
    MASK_ALL = "MASK_ALL"
    MASK_FIRST_N = "MASK_FIRST_N"
    MASK_LAST_N = "MASK_LAST_N"
    VALIDATE_NON_NULL = "VALIDATE_NON_NULL"
    VALIDATE_NON_ZERO = "VALIDATE_NON_ZERO"
    VALIDATE_NON_NEGATIVE = "VALIDATE_NON_NEGATIVE"
    VALIDATE_NUMERIC = "VALIDATE_NUMERIC"
    NO_OP = "NO_OP"


class IntegrationTaskType(str, Enum):
    ARITHMETIC = "Arithmetic"
    FILTER = "Filter"
    MAP = "Map"
    MASK = "Mask"
    MERGE = "Merge"
    TRUNCATE = "Truncate"
    VALIDATE = "Validate"


class IntegrationTriggerType(str, Enum):
    SCHEDULED = "Scheduled"
    EVENT = "Event"
    ON_DEMAND = "OnDemand"


class IntegrationZendeskConnectorOperator(str, Enum):
    PROJECTION = "PROJECTION"
    GREATER_THAN = "GREATER_THAN"
    ADDITION = "ADDITION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION"
    SUBTRACTION = "SUBTRACTION"
    MASK_ALL = "MASK_ALL"
    MASK_FIRST_N = "MASK_FIRST_N"
    MASK_LAST_N = "MASK_LAST_N"
    VALIDATE_NON_NULL = "VALIDATE_NON_NULL"
    VALIDATE_NON_ZERO = "VALIDATE_NON_ZERO"
    VALIDATE_NON_NEGATIVE = "VALIDATE_NON_NEGATIVE"
    VALIDATE_NUMERIC = "VALIDATE_NUMERIC"
    NO_OP = "NO_OP"


class ObjectTypeFieldContentType(str, Enum):
    """
    The content type of the field. Used for determining equality when searching.
    """
    STRING = "STRING"
    NUMBER = "NUMBER"
    PHONE_NUMBER = "PHONE_NUMBER"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    NAME = "NAME"


class ObjectTypeKeyStandardIdentifiersItem(str, Enum):
    PROFILE = "PROFILE"
    UNIQUE = "UNIQUE"
    SECONDARY = "SECONDARY"
    LOOKUP_ONLY = "LOOKUP_ONLY"
    NEW_ONLY = "NEW_ONLY"
