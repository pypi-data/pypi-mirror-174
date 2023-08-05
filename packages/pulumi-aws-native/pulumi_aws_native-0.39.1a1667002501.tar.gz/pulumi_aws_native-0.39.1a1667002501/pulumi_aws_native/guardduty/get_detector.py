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
    'GetDetectorResult',
    'AwaitableGetDetectorResult',
    'get_detector',
    'get_detector_output',
]

@pulumi.output_type
class GetDetectorResult:
    def __init__(__self__, data_sources=None, enable=None, finding_publishing_frequency=None, id=None, tags=None):
        if data_sources and not isinstance(data_sources, dict):
            raise TypeError("Expected argument 'data_sources' to be a dict")
        pulumi.set(__self__, "data_sources", data_sources)
        if enable and not isinstance(enable, bool):
            raise TypeError("Expected argument 'enable' to be a bool")
        pulumi.set(__self__, "enable", enable)
        if finding_publishing_frequency and not isinstance(finding_publishing_frequency, str):
            raise TypeError("Expected argument 'finding_publishing_frequency' to be a str")
        pulumi.set(__self__, "finding_publishing_frequency", finding_publishing_frequency)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dataSources")
    def data_sources(self) -> Optional['outputs.DetectorCFNDataSourceConfigurations']:
        return pulumi.get(self, "data_sources")

    @property
    @pulumi.getter
    def enable(self) -> Optional[bool]:
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> Optional[str]:
        return pulumi.get(self, "finding_publishing_frequency")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.DetectorTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetDetectorResult(GetDetectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDetectorResult(
            data_sources=self.data_sources,
            enable=self.enable,
            finding_publishing_frequency=self.finding_publishing_frequency,
            id=self.id,
            tags=self.tags)


def get_detector(id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDetectorResult:
    """
    Resource Type definition for AWS::GuardDuty::Detector
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:guardduty:getDetector', __args__, opts=opts, typ=GetDetectorResult).value

    return AwaitableGetDetectorResult(
        data_sources=__ret__.data_sources,
        enable=__ret__.enable,
        finding_publishing_frequency=__ret__.finding_publishing_frequency,
        id=__ret__.id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_detector)
def get_detector_output(id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDetectorResult]:
    """
    Resource Type definition for AWS::GuardDuty::Detector
    """
    ...
