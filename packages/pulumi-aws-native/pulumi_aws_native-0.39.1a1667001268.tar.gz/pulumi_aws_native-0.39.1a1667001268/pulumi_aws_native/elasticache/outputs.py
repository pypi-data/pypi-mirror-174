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
from ._enums import *

__all__ = [
    'CacheClusterCloudWatchLogsDestinationDetails',
    'CacheClusterDestinationDetails',
    'CacheClusterKinesisFirehoseDestinationDetails',
    'CacheClusterLogDeliveryConfigurationRequest',
    'CacheClusterTag',
    'GlobalReplicationGroupMember',
    'GlobalReplicationGroupRegionalConfiguration',
    'GlobalReplicationGroupReshardingConfiguration',
    'ParameterGroupTag',
    'ReplicationGroupCloudWatchLogsDestinationDetails',
    'ReplicationGroupDestinationDetails',
    'ReplicationGroupKinesisFirehoseDestinationDetails',
    'ReplicationGroupLogDeliveryConfigurationRequest',
    'ReplicationGroupNodeGroupConfiguration',
    'ReplicationGroupTag',
    'SecurityGroupTag',
    'SubnetGroupTag',
]

@pulumi.output_type
class CacheClusterCloudWatchLogsDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CacheClusterCloudWatchLogsDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CacheClusterCloudWatchLogsDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CacheClusterCloudWatchLogsDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group: str):
        pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> str:
        return pulumi.get(self, "log_group")


@pulumi.output_type
class CacheClusterDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudWatchLogsDetails":
            suggest = "cloud_watch_logs_details"
        elif key == "kinesisFirehoseDetails":
            suggest = "kinesis_firehose_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CacheClusterDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CacheClusterDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CacheClusterDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_watch_logs_details: Optional['outputs.CacheClusterCloudWatchLogsDestinationDetails'] = None,
                 kinesis_firehose_details: Optional['outputs.CacheClusterKinesisFirehoseDestinationDetails'] = None):
        if cloud_watch_logs_details is not None:
            pulumi.set(__self__, "cloud_watch_logs_details", cloud_watch_logs_details)
        if kinesis_firehose_details is not None:
            pulumi.set(__self__, "kinesis_firehose_details", kinesis_firehose_details)

    @property
    @pulumi.getter(name="cloudWatchLogsDetails")
    def cloud_watch_logs_details(self) -> Optional['outputs.CacheClusterCloudWatchLogsDestinationDetails']:
        return pulumi.get(self, "cloud_watch_logs_details")

    @property
    @pulumi.getter(name="kinesisFirehoseDetails")
    def kinesis_firehose_details(self) -> Optional['outputs.CacheClusterKinesisFirehoseDestinationDetails']:
        return pulumi.get(self, "kinesis_firehose_details")


@pulumi.output_type
class CacheClusterKinesisFirehoseDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deliveryStream":
            suggest = "delivery_stream"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CacheClusterKinesisFirehoseDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CacheClusterKinesisFirehoseDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CacheClusterKinesisFirehoseDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 delivery_stream: str):
        pulumi.set(__self__, "delivery_stream", delivery_stream)

    @property
    @pulumi.getter(name="deliveryStream")
    def delivery_stream(self) -> str:
        return pulumi.get(self, "delivery_stream")


@pulumi.output_type
class CacheClusterLogDeliveryConfigurationRequest(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationDetails":
            suggest = "destination_details"
        elif key == "destinationType":
            suggest = "destination_type"
        elif key == "logFormat":
            suggest = "log_format"
        elif key == "logType":
            suggest = "log_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CacheClusterLogDeliveryConfigurationRequest. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CacheClusterLogDeliveryConfigurationRequest.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CacheClusterLogDeliveryConfigurationRequest.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_details: 'outputs.CacheClusterDestinationDetails',
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        pulumi.set(__self__, "destination_details", destination_details)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter(name="destinationDetails")
    def destination_details(self) -> 'outputs.CacheClusterDestinationDetails':
        return pulumi.get(self, "destination_details")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        return pulumi.get(self, "log_type")


@pulumi.output_type
class CacheClusterTag(dict):
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
class GlobalReplicationGroupMember(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "replicationGroupId":
            suggest = "replication_group_id"
        elif key == "replicationGroupRegion":
            suggest = "replication_group_region"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GlobalReplicationGroupMember. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GlobalReplicationGroupMember.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GlobalReplicationGroupMember.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 replication_group_id: Optional[str] = None,
                 replication_group_region: Optional[str] = None,
                 role: Optional['GlobalReplicationGroupMemberRole'] = None):
        """
        :param str replication_group_id: Regionally unique identifier for the member i.e. ReplicationGroupId.
        :param str replication_group_region: The AWS region of the Global Datastore member.
        :param 'GlobalReplicationGroupMemberRole' role: Indicates the role of the member, primary or secondary.
        """
        if replication_group_id is not None:
            pulumi.set(__self__, "replication_group_id", replication_group_id)
        if replication_group_region is not None:
            pulumi.set(__self__, "replication_group_region", replication_group_region)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter(name="replicationGroupId")
    def replication_group_id(self) -> Optional[str]:
        """
        Regionally unique identifier for the member i.e. ReplicationGroupId.
        """
        return pulumi.get(self, "replication_group_id")

    @property
    @pulumi.getter(name="replicationGroupRegion")
    def replication_group_region(self) -> Optional[str]:
        """
        The AWS region of the Global Datastore member.
        """
        return pulumi.get(self, "replication_group_region")

    @property
    @pulumi.getter
    def role(self) -> Optional['GlobalReplicationGroupMemberRole']:
        """
        Indicates the role of the member, primary or secondary.
        """
        return pulumi.get(self, "role")


@pulumi.output_type
class GlobalReplicationGroupRegionalConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "replicationGroupId":
            suggest = "replication_group_id"
        elif key == "replicationGroupRegion":
            suggest = "replication_group_region"
        elif key == "reshardingConfigurations":
            suggest = "resharding_configurations"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GlobalReplicationGroupRegionalConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GlobalReplicationGroupRegionalConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GlobalReplicationGroupRegionalConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 replication_group_id: Optional[str] = None,
                 replication_group_region: Optional[str] = None,
                 resharding_configurations: Optional[Sequence['outputs.GlobalReplicationGroupReshardingConfiguration']] = None):
        """
        :param str replication_group_id: The replication group id of the Global Datastore member.
        :param str replication_group_region: The AWS region of the Global Datastore member.
        :param Sequence['GlobalReplicationGroupReshardingConfiguration'] resharding_configurations: A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster. 
        """
        if replication_group_id is not None:
            pulumi.set(__self__, "replication_group_id", replication_group_id)
        if replication_group_region is not None:
            pulumi.set(__self__, "replication_group_region", replication_group_region)
        if resharding_configurations is not None:
            pulumi.set(__self__, "resharding_configurations", resharding_configurations)

    @property
    @pulumi.getter(name="replicationGroupId")
    def replication_group_id(self) -> Optional[str]:
        """
        The replication group id of the Global Datastore member.
        """
        return pulumi.get(self, "replication_group_id")

    @property
    @pulumi.getter(name="replicationGroupRegion")
    def replication_group_region(self) -> Optional[str]:
        """
        The AWS region of the Global Datastore member.
        """
        return pulumi.get(self, "replication_group_region")

    @property
    @pulumi.getter(name="reshardingConfigurations")
    def resharding_configurations(self) -> Optional[Sequence['outputs.GlobalReplicationGroupReshardingConfiguration']]:
        """
        A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster. 
        """
        return pulumi.get(self, "resharding_configurations")


@pulumi.output_type
class GlobalReplicationGroupReshardingConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nodeGroupId":
            suggest = "node_group_id"
        elif key == "preferredAvailabilityZones":
            suggest = "preferred_availability_zones"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GlobalReplicationGroupReshardingConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GlobalReplicationGroupReshardingConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GlobalReplicationGroupReshardingConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 node_group_id: Optional[str] = None,
                 preferred_availability_zones: Optional[Sequence[str]] = None):
        """
        :param str node_group_id: Unique identifier for the Node Group. This is either auto-generated by ElastiCache (4-digit id) or a user supplied id.
        :param Sequence[str] preferred_availability_zones: A list of preferred availability zones for the nodes of new node groups.
        """
        if node_group_id is not None:
            pulumi.set(__self__, "node_group_id", node_group_id)
        if preferred_availability_zones is not None:
            pulumi.set(__self__, "preferred_availability_zones", preferred_availability_zones)

    @property
    @pulumi.getter(name="nodeGroupId")
    def node_group_id(self) -> Optional[str]:
        """
        Unique identifier for the Node Group. This is either auto-generated by ElastiCache (4-digit id) or a user supplied id.
        """
        return pulumi.get(self, "node_group_id")

    @property
    @pulumi.getter(name="preferredAvailabilityZones")
    def preferred_availability_zones(self) -> Optional[Sequence[str]]:
        """
        A list of preferred availability zones for the nodes of new node groups.
        """
        return pulumi.get(self, "preferred_availability_zones")


@pulumi.output_type
class ParameterGroupTag(dict):
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
class ReplicationGroupCloudWatchLogsDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupCloudWatchLogsDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupCloudWatchLogsDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupCloudWatchLogsDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group: str):
        pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> str:
        return pulumi.get(self, "log_group")


@pulumi.output_type
class ReplicationGroupDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudWatchLogsDetails":
            suggest = "cloud_watch_logs_details"
        elif key == "kinesisFirehoseDetails":
            suggest = "kinesis_firehose_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_watch_logs_details: Optional['outputs.ReplicationGroupCloudWatchLogsDestinationDetails'] = None,
                 kinesis_firehose_details: Optional['outputs.ReplicationGroupKinesisFirehoseDestinationDetails'] = None):
        if cloud_watch_logs_details is not None:
            pulumi.set(__self__, "cloud_watch_logs_details", cloud_watch_logs_details)
        if kinesis_firehose_details is not None:
            pulumi.set(__self__, "kinesis_firehose_details", kinesis_firehose_details)

    @property
    @pulumi.getter(name="cloudWatchLogsDetails")
    def cloud_watch_logs_details(self) -> Optional['outputs.ReplicationGroupCloudWatchLogsDestinationDetails']:
        return pulumi.get(self, "cloud_watch_logs_details")

    @property
    @pulumi.getter(name="kinesisFirehoseDetails")
    def kinesis_firehose_details(self) -> Optional['outputs.ReplicationGroupKinesisFirehoseDestinationDetails']:
        return pulumi.get(self, "kinesis_firehose_details")


@pulumi.output_type
class ReplicationGroupKinesisFirehoseDestinationDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deliveryStream":
            suggest = "delivery_stream"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupKinesisFirehoseDestinationDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupKinesisFirehoseDestinationDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupKinesisFirehoseDestinationDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 delivery_stream: str):
        pulumi.set(__self__, "delivery_stream", delivery_stream)

    @property
    @pulumi.getter(name="deliveryStream")
    def delivery_stream(self) -> str:
        return pulumi.get(self, "delivery_stream")


@pulumi.output_type
class ReplicationGroupLogDeliveryConfigurationRequest(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationDetails":
            suggest = "destination_details"
        elif key == "destinationType":
            suggest = "destination_type"
        elif key == "logFormat":
            suggest = "log_format"
        elif key == "logType":
            suggest = "log_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupLogDeliveryConfigurationRequest. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupLogDeliveryConfigurationRequest.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupLogDeliveryConfigurationRequest.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_details: 'outputs.ReplicationGroupDestinationDetails',
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        pulumi.set(__self__, "destination_details", destination_details)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter(name="destinationDetails")
    def destination_details(self) -> 'outputs.ReplicationGroupDestinationDetails':
        return pulumi.get(self, "destination_details")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        return pulumi.get(self, "log_type")


@pulumi.output_type
class ReplicationGroupNodeGroupConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nodeGroupId":
            suggest = "node_group_id"
        elif key == "primaryAvailabilityZone":
            suggest = "primary_availability_zone"
        elif key == "replicaAvailabilityZones":
            suggest = "replica_availability_zones"
        elif key == "replicaCount":
            suggest = "replica_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupNodeGroupConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupNodeGroupConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupNodeGroupConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 node_group_id: Optional[str] = None,
                 primary_availability_zone: Optional[str] = None,
                 replica_availability_zones: Optional[Sequence[str]] = None,
                 replica_count: Optional[int] = None,
                 slots: Optional[str] = None):
        if node_group_id is not None:
            pulumi.set(__self__, "node_group_id", node_group_id)
        if primary_availability_zone is not None:
            pulumi.set(__self__, "primary_availability_zone", primary_availability_zone)
        if replica_availability_zones is not None:
            pulumi.set(__self__, "replica_availability_zones", replica_availability_zones)
        if replica_count is not None:
            pulumi.set(__self__, "replica_count", replica_count)
        if slots is not None:
            pulumi.set(__self__, "slots", slots)

    @property
    @pulumi.getter(name="nodeGroupId")
    def node_group_id(self) -> Optional[str]:
        return pulumi.get(self, "node_group_id")

    @property
    @pulumi.getter(name="primaryAvailabilityZone")
    def primary_availability_zone(self) -> Optional[str]:
        return pulumi.get(self, "primary_availability_zone")

    @property
    @pulumi.getter(name="replicaAvailabilityZones")
    def replica_availability_zones(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "replica_availability_zones")

    @property
    @pulumi.getter(name="replicaCount")
    def replica_count(self) -> Optional[int]:
        return pulumi.get(self, "replica_count")

    @property
    @pulumi.getter
    def slots(self) -> Optional[str]:
        return pulumi.get(self, "slots")


@pulumi.output_type
class ReplicationGroupTag(dict):
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
class SecurityGroupTag(dict):
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
class SubnetGroupTag(dict):
    """
    A tag that can be added to an ElastiCache subnet group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A tag that can be added to an ElastiCache subnet group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.
        """
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


