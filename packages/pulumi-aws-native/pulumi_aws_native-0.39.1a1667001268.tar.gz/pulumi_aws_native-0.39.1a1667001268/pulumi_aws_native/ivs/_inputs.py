# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ChannelTagArgs',
    'PlaybackKeyPairTagArgs',
    'RecordingConfigurationDestinationConfigurationArgs',
    'RecordingConfigurationS3DestinationConfigurationArgs',
    'RecordingConfigurationTagArgs',
    'RecordingConfigurationThumbnailConfigurationArgs',
    'StreamKeyTagArgs',
]

@pulumi.input_type
class ChannelTagArgs:
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
class PlaybackKeyPairTagArgs:
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
class RecordingConfigurationDestinationConfigurationArgs:
    def __init__(__self__, *,
                 s3: pulumi.Input['RecordingConfigurationS3DestinationConfigurationArgs']):
        """
        Recording Destination Configuration.
        """
        pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter
    def s3(self) -> pulumi.Input['RecordingConfigurationS3DestinationConfigurationArgs']:
        return pulumi.get(self, "s3")

    @s3.setter
    def s3(self, value: pulumi.Input['RecordingConfigurationS3DestinationConfigurationArgs']):
        pulumi.set(self, "s3", value)


@pulumi.input_type
class RecordingConfigurationS3DestinationConfigurationArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str]):
        """
        Recording S3 Destination Configuration.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)


@pulumi.input_type
class RecordingConfigurationTagArgs:
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
class RecordingConfigurationThumbnailConfigurationArgs:
    def __init__(__self__, *,
                 recording_mode: pulumi.Input['RecordingConfigurationThumbnailConfigurationRecordingMode'],
                 target_interval_seconds: Optional[pulumi.Input[int]] = None):
        """
        Recording Thumbnail Configuration.
        :param pulumi.Input['RecordingConfigurationThumbnailConfigurationRecordingMode'] recording_mode: Thumbnail Recording Mode, which determines whether thumbnails are recorded at an interval or are disabled.
        :param pulumi.Input[int] target_interval_seconds: Thumbnail recording Target Interval Seconds defines the interval at which thumbnails are recorded. This field is required if RecordingMode is INTERVAL.
        """
        pulumi.set(__self__, "recording_mode", recording_mode)
        if target_interval_seconds is not None:
            pulumi.set(__self__, "target_interval_seconds", target_interval_seconds)

    @property
    @pulumi.getter(name="recordingMode")
    def recording_mode(self) -> pulumi.Input['RecordingConfigurationThumbnailConfigurationRecordingMode']:
        """
        Thumbnail Recording Mode, which determines whether thumbnails are recorded at an interval or are disabled.
        """
        return pulumi.get(self, "recording_mode")

    @recording_mode.setter
    def recording_mode(self, value: pulumi.Input['RecordingConfigurationThumbnailConfigurationRecordingMode']):
        pulumi.set(self, "recording_mode", value)

    @property
    @pulumi.getter(name="targetIntervalSeconds")
    def target_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Thumbnail recording Target Interval Seconds defines the interval at which thumbnails are recorded. This field is required if RecordingMode is INTERVAL.
        """
        return pulumi.get(self, "target_interval_seconds")

    @target_interval_seconds.setter
    def target_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "target_interval_seconds", value)


@pulumi.input_type
class StreamKeyTagArgs:
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


