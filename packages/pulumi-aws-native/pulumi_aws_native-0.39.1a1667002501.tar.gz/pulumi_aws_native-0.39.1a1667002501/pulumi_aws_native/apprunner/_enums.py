# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ObservabilityConfigurationTraceConfigurationVendor',
    'ServiceCodeConfigurationConfigurationSource',
    'ServiceCodeConfigurationValuesRuntime',
    'ServiceEgressConfigurationEgressType',
    'ServiceHealthCheckConfigurationProtocol',
    'ServiceImageRepositoryImageRepositoryType',
    'ServiceSourceCodeVersionType',
]


class ObservabilityConfigurationTraceConfigurationVendor(str, Enum):
    """
    The implementation provider chosen for tracing App Runner services.
    """
    AWSXRAY = "AWSXRAY"


class ServiceCodeConfigurationConfigurationSource(str, Enum):
    """
    Configuration Source
    """
    REPOSITORY = "REPOSITORY"
    API = "API"


class ServiceCodeConfigurationValuesRuntime(str, Enum):
    """
    Runtime
    """
    PYTHON3 = "PYTHON_3"
    NODEJS12 = "NODEJS_12"
    NODEJS14 = "NODEJS_14"
    CORRETTO8 = "CORRETTO_8"
    CORRETTO11 = "CORRETTO_11"
    NODEJS16 = "NODEJS_16"


class ServiceEgressConfigurationEgressType(str, Enum):
    """
    Network egress type.
    """
    DEFAULT = "DEFAULT"
    VPC = "VPC"


class ServiceHealthCheckConfigurationProtocol(str, Enum):
    """
    Health Check Protocol
    """
    TCP = "TCP"
    HTTP = "HTTP"


class ServiceImageRepositoryImageRepositoryType(str, Enum):
    """
    Image Repository Type
    """
    ECR = "ECR"
    ECR_PUBLIC = "ECR_PUBLIC"


class ServiceSourceCodeVersionType(str, Enum):
    """
    Source Code Version Type
    """
    BRANCH = "BRANCH"
