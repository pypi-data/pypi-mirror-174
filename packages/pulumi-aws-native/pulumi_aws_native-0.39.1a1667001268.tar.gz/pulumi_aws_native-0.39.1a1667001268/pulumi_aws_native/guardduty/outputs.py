# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'DetectorCFNDataSourceConfigurations',
    'DetectorCFNKubernetesAuditLogsConfiguration',
    'DetectorCFNKubernetesConfiguration',
    'DetectorCFNMalwareProtectionConfiguration',
    'DetectorCFNS3LogsConfiguration',
    'DetectorCFNScanEc2InstanceWithFindingsConfiguration',
    'DetectorTag',
    'FilterCondition',
    'FilterFindingCriteria',
    'FilterTag',
    'IPSetTag',
    'ThreatIntelSetTag',
]

@pulumi.output_type
class DetectorCFNDataSourceConfigurations(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "malwareProtection":
            suggest = "malware_protection"
        elif key == "s3Logs":
            suggest = "s3_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorCFNDataSourceConfigurations. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorCFNDataSourceConfigurations.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorCFNDataSourceConfigurations.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kubernetes: Optional['outputs.DetectorCFNKubernetesConfiguration'] = None,
                 malware_protection: Optional['outputs.DetectorCFNMalwareProtectionConfiguration'] = None,
                 s3_logs: Optional['outputs.DetectorCFNS3LogsConfiguration'] = None):
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional['outputs.DetectorCFNKubernetesConfiguration']:
        return pulumi.get(self, "kubernetes")

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional['outputs.DetectorCFNMalwareProtectionConfiguration']:
        return pulumi.get(self, "malware_protection")

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional['outputs.DetectorCFNS3LogsConfiguration']:
        return pulumi.get(self, "s3_logs")


@pulumi.output_type
class DetectorCFNKubernetesAuditLogsConfiguration(dict):
    def __init__(__self__, *,
                 enable: Optional[bool] = None):
        if enable is not None:
            pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> Optional[bool]:
        return pulumi.get(self, "enable")


@pulumi.output_type
class DetectorCFNKubernetesConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "auditLogs":
            suggest = "audit_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorCFNKubernetesConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorCFNKubernetesConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorCFNKubernetesConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 audit_logs: Optional['outputs.DetectorCFNKubernetesAuditLogsConfiguration'] = None):
        if audit_logs is not None:
            pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> Optional['outputs.DetectorCFNKubernetesAuditLogsConfiguration']:
        return pulumi.get(self, "audit_logs")


@pulumi.output_type
class DetectorCFNMalwareProtectionConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "scanEc2InstanceWithFindings":
            suggest = "scan_ec2_instance_with_findings"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorCFNMalwareProtectionConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorCFNMalwareProtectionConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorCFNMalwareProtectionConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: Optional['outputs.DetectorCFNScanEc2InstanceWithFindingsConfiguration'] = None):
        if scan_ec2_instance_with_findings is not None:
            pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> Optional['outputs.DetectorCFNScanEc2InstanceWithFindingsConfiguration']:
        return pulumi.get(self, "scan_ec2_instance_with_findings")


@pulumi.output_type
class DetectorCFNS3LogsConfiguration(dict):
    def __init__(__self__, *,
                 enable: Optional[bool] = None):
        if enable is not None:
            pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> Optional[bool]:
        return pulumi.get(self, "enable")


@pulumi.output_type
class DetectorCFNScanEc2InstanceWithFindingsConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ebsVolumes":
            suggest = "ebs_volumes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorCFNScanEc2InstanceWithFindingsConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorCFNScanEc2InstanceWithFindingsConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorCFNScanEc2InstanceWithFindingsConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ebs_volumes: Optional[bool] = None):
        if ebs_volumes is not None:
            pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> Optional[bool]:
        return pulumi.get(self, "ebs_volumes")


@pulumi.output_type
class DetectorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class FilterCondition(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "greaterThan":
            suggest = "greater_than"
        elif key == "greaterThanOrEqual":
            suggest = "greater_than_or_equal"
        elif key == "lessThan":
            suggest = "less_than"
        elif key == "lessThanOrEqual":
            suggest = "less_than_or_equal"
        elif key == "notEquals":
            suggest = "not_equals"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FilterCondition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FilterCondition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FilterCondition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 eq: Optional[Sequence[str]] = None,
                 equals: Optional[Sequence[str]] = None,
                 greater_than: Optional[int] = None,
                 greater_than_or_equal: Optional[int] = None,
                 gt: Optional[int] = None,
                 gte: Optional[int] = None,
                 less_than: Optional[int] = None,
                 less_than_or_equal: Optional[int] = None,
                 lt: Optional[int] = None,
                 lte: Optional[int] = None,
                 neq: Optional[Sequence[str]] = None,
                 not_equals: Optional[Sequence[str]] = None):
        if eq is not None:
            pulumi.set(__self__, "eq", eq)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if greater_than is not None:
            pulumi.set(__self__, "greater_than", greater_than)
        if greater_than_or_equal is not None:
            pulumi.set(__self__, "greater_than_or_equal", greater_than_or_equal)
        if gt is not None:
            pulumi.set(__self__, "gt", gt)
        if gte is not None:
            pulumi.set(__self__, "gte", gte)
        if less_than is not None:
            pulumi.set(__self__, "less_than", less_than)
        if less_than_or_equal is not None:
            pulumi.set(__self__, "less_than_or_equal", less_than_or_equal)
        if lt is not None:
            pulumi.set(__self__, "lt", lt)
        if lte is not None:
            pulumi.set(__self__, "lte", lte)
        if neq is not None:
            pulumi.set(__self__, "neq", neq)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)

    @property
    @pulumi.getter
    def eq(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "eq")

    @property
    @pulumi.getter
    def equals(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "equals")

    @property
    @pulumi.getter(name="greaterThan")
    def greater_than(self) -> Optional[int]:
        return pulumi.get(self, "greater_than")

    @property
    @pulumi.getter(name="greaterThanOrEqual")
    def greater_than_or_equal(self) -> Optional[int]:
        return pulumi.get(self, "greater_than_or_equal")

    @property
    @pulumi.getter
    def gt(self) -> Optional[int]:
        return pulumi.get(self, "gt")

    @property
    @pulumi.getter
    def gte(self) -> Optional[int]:
        return pulumi.get(self, "gte")

    @property
    @pulumi.getter(name="lessThan")
    def less_than(self) -> Optional[int]:
        return pulumi.get(self, "less_than")

    @property
    @pulumi.getter(name="lessThanOrEqual")
    def less_than_or_equal(self) -> Optional[int]:
        return pulumi.get(self, "less_than_or_equal")

    @property
    @pulumi.getter
    def lt(self) -> Optional[int]:
        return pulumi.get(self, "lt")

    @property
    @pulumi.getter
    def lte(self) -> Optional[int]:
        return pulumi.get(self, "lte")

    @property
    @pulumi.getter
    def neq(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "neq")

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "not_equals")


@pulumi.output_type
class FilterFindingCriteria(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "itemType":
            suggest = "item_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FilterFindingCriteria. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FilterFindingCriteria.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FilterFindingCriteria.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 criterion: Optional[Any] = None,
                 item_type: Optional['outputs.FilterCondition'] = None):
        if criterion is not None:
            pulumi.set(__self__, "criterion", criterion)
        if item_type is not None:
            pulumi.set(__self__, "item_type", item_type)

    @property
    @pulumi.getter
    def criterion(self) -> Optional[Any]:
        return pulumi.get(self, "criterion")

    @property
    @pulumi.getter(name="itemType")
    def item_type(self) -> Optional['outputs.FilterCondition']:
        return pulumi.get(self, "item_type")


@pulumi.output_type
class FilterTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class IPSetTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ThreatIntelSetTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


