# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'DetectorCFNDataSourceConfigurationsArgs',
    'DetectorCFNKubernetesAuditLogsConfigurationArgs',
    'DetectorCFNKubernetesConfigurationArgs',
    'DetectorCFNMalwareProtectionConfigurationArgs',
    'DetectorCFNS3LogsConfigurationArgs',
    'DetectorCFNScanEc2InstanceWithFindingsConfigurationArgs',
    'DetectorTagArgs',
    'FilterConditionArgs',
    'FilterFindingCriteriaArgs',
    'FilterTagArgs',
    'IPSetTagArgs',
    'ThreatIntelSetTagArgs',
]

@pulumi.input_type
class DetectorCFNDataSourceConfigurationsArgs:
    def __init__(__self__, *,
                 kubernetes: Optional[pulumi.Input['DetectorCFNKubernetesConfigurationArgs']] = None,
                 malware_protection: Optional[pulumi.Input['DetectorCFNMalwareProtectionConfigurationArgs']] = None,
                 s3_logs: Optional[pulumi.Input['DetectorCFNS3LogsConfigurationArgs']] = None):
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional[pulumi.Input['DetectorCFNKubernetesConfigurationArgs']]:
        return pulumi.get(self, "kubernetes")

    @kubernetes.setter
    def kubernetes(self, value: Optional[pulumi.Input['DetectorCFNKubernetesConfigurationArgs']]):
        pulumi.set(self, "kubernetes", value)

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional[pulumi.Input['DetectorCFNMalwareProtectionConfigurationArgs']]:
        return pulumi.get(self, "malware_protection")

    @malware_protection.setter
    def malware_protection(self, value: Optional[pulumi.Input['DetectorCFNMalwareProtectionConfigurationArgs']]):
        pulumi.set(self, "malware_protection", value)

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional[pulumi.Input['DetectorCFNS3LogsConfigurationArgs']]:
        return pulumi.get(self, "s3_logs")

    @s3_logs.setter
    def s3_logs(self, value: Optional[pulumi.Input['DetectorCFNS3LogsConfigurationArgs']]):
        pulumi.set(self, "s3_logs", value)


@pulumi.input_type
class DetectorCFNKubernetesAuditLogsConfigurationArgs:
    def __init__(__self__, *,
                 enable: Optional[pulumi.Input[bool]] = None):
        if enable is not None:
            pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class DetectorCFNKubernetesConfigurationArgs:
    def __init__(__self__, *,
                 audit_logs: Optional[pulumi.Input['DetectorCFNKubernetesAuditLogsConfigurationArgs']] = None):
        if audit_logs is not None:
            pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> Optional[pulumi.Input['DetectorCFNKubernetesAuditLogsConfigurationArgs']]:
        return pulumi.get(self, "audit_logs")

    @audit_logs.setter
    def audit_logs(self, value: Optional[pulumi.Input['DetectorCFNKubernetesAuditLogsConfigurationArgs']]):
        pulumi.set(self, "audit_logs", value)


@pulumi.input_type
class DetectorCFNMalwareProtectionConfigurationArgs:
    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: Optional[pulumi.Input['DetectorCFNScanEc2InstanceWithFindingsConfigurationArgs']] = None):
        if scan_ec2_instance_with_findings is not None:
            pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> Optional[pulumi.Input['DetectorCFNScanEc2InstanceWithFindingsConfigurationArgs']]:
        return pulumi.get(self, "scan_ec2_instance_with_findings")

    @scan_ec2_instance_with_findings.setter
    def scan_ec2_instance_with_findings(self, value: Optional[pulumi.Input['DetectorCFNScanEc2InstanceWithFindingsConfigurationArgs']]):
        pulumi.set(self, "scan_ec2_instance_with_findings", value)


@pulumi.input_type
class DetectorCFNS3LogsConfigurationArgs:
    def __init__(__self__, *,
                 enable: Optional[pulumi.Input[bool]] = None):
        if enable is not None:
            pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class DetectorCFNScanEc2InstanceWithFindingsConfigurationArgs:
    def __init__(__self__, *,
                 ebs_volumes: Optional[pulumi.Input[bool]] = None):
        if ebs_volumes is not None:
            pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "ebs_volumes")

    @ebs_volumes.setter
    def ebs_volumes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ebs_volumes", value)


@pulumi.input_type
class DetectorTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class FilterConditionArgs:
    def __init__(__self__, *,
                 eq: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 greater_than: Optional[pulumi.Input[int]] = None,
                 greater_than_or_equal: Optional[pulumi.Input[int]] = None,
                 gt: Optional[pulumi.Input[int]] = None,
                 gte: Optional[pulumi.Input[int]] = None,
                 less_than: Optional[pulumi.Input[int]] = None,
                 less_than_or_equal: Optional[pulumi.Input[int]] = None,
                 lt: Optional[pulumi.Input[int]] = None,
                 lte: Optional[pulumi.Input[int]] = None,
                 neq: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
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
    def eq(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "eq")

    @eq.setter
    def eq(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "eq", value)

    @property
    @pulumi.getter
    def equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "equals")

    @equals.setter
    def equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "equals", value)

    @property
    @pulumi.getter(name="greaterThan")
    def greater_than(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "greater_than")

    @greater_than.setter
    def greater_than(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "greater_than", value)

    @property
    @pulumi.getter(name="greaterThanOrEqual")
    def greater_than_or_equal(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "greater_than_or_equal")

    @greater_than_or_equal.setter
    def greater_than_or_equal(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "greater_than_or_equal", value)

    @property
    @pulumi.getter
    def gt(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "gt")

    @gt.setter
    def gt(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "gt", value)

    @property
    @pulumi.getter
    def gte(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "gte")

    @gte.setter
    def gte(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "gte", value)

    @property
    @pulumi.getter(name="lessThan")
    def less_than(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "less_than")

    @less_than.setter
    def less_than(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "less_than", value)

    @property
    @pulumi.getter(name="lessThanOrEqual")
    def less_than_or_equal(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "less_than_or_equal")

    @less_than_or_equal.setter
    def less_than_or_equal(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "less_than_or_equal", value)

    @property
    @pulumi.getter
    def lt(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "lt")

    @lt.setter
    def lt(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lt", value)

    @property
    @pulumi.getter
    def lte(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "lte")

    @lte.setter
    def lte(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lte", value)

    @property
    @pulumi.getter
    def neq(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "neq")

    @neq.setter
    def neq(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "neq", value)

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "not_equals")

    @not_equals.setter
    def not_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_equals", value)


@pulumi.input_type
class FilterFindingCriteriaArgs:
    def __init__(__self__, *,
                 criterion: Optional[Any] = None,
                 item_type: Optional[pulumi.Input['FilterConditionArgs']] = None):
        if criterion is not None:
            pulumi.set(__self__, "criterion", criterion)
        if item_type is not None:
            pulumi.set(__self__, "item_type", item_type)

    @property
    @pulumi.getter
    def criterion(self) -> Optional[Any]:
        return pulumi.get(self, "criterion")

    @criterion.setter
    def criterion(self, value: Optional[Any]):
        pulumi.set(self, "criterion", value)

    @property
    @pulumi.getter(name="itemType")
    def item_type(self) -> Optional[pulumi.Input['FilterConditionArgs']]:
        return pulumi.get(self, "item_type")

    @item_type.setter
    def item_type(self, value: Optional[pulumi.Input['FilterConditionArgs']]):
        pulumi.set(self, "item_type", value)


@pulumi.input_type
class FilterTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class IPSetTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ThreatIntelSetTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


