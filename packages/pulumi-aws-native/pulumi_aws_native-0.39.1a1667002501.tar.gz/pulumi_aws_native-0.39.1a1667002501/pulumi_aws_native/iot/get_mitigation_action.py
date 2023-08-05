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
    'GetMitigationActionResult',
    'AwaitableGetMitigationActionResult',
    'get_mitigation_action',
    'get_mitigation_action_output',
]

@pulumi.output_type
class GetMitigationActionResult:
    def __init__(__self__, action_params=None, mitigation_action_arn=None, mitigation_action_id=None, role_arn=None, tags=None):
        if action_params and not isinstance(action_params, dict):
            raise TypeError("Expected argument 'action_params' to be a dict")
        pulumi.set(__self__, "action_params", action_params)
        if mitigation_action_arn and not isinstance(mitigation_action_arn, str):
            raise TypeError("Expected argument 'mitigation_action_arn' to be a str")
        pulumi.set(__self__, "mitigation_action_arn", mitigation_action_arn)
        if mitigation_action_id and not isinstance(mitigation_action_id, str):
            raise TypeError("Expected argument 'mitigation_action_id' to be a str")
        pulumi.set(__self__, "mitigation_action_id", mitigation_action_id)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="actionParams")
    def action_params(self) -> Optional['outputs.MitigationActionActionParams']:
        return pulumi.get(self, "action_params")

    @property
    @pulumi.getter(name="mitigationActionArn")
    def mitigation_action_arn(self) -> Optional[str]:
        return pulumi.get(self, "mitigation_action_arn")

    @property
    @pulumi.getter(name="mitigationActionId")
    def mitigation_action_id(self) -> Optional[str]:
        return pulumi.get(self, "mitigation_action_id")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.MitigationActionTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetMitigationActionResult(GetMitigationActionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMitigationActionResult(
            action_params=self.action_params,
            mitigation_action_arn=self.mitigation_action_arn,
            mitigation_action_id=self.mitigation_action_id,
            role_arn=self.role_arn,
            tags=self.tags)


def get_mitigation_action(action_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMitigationActionResult:
    """
    Mitigation actions can be used to take actions to mitigate issues that were found in an Audit finding or Detect violation.


    :param str action_name: A unique identifier for the mitigation action.
    """
    __args__ = dict()
    __args__['actionName'] = action_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getMitigationAction', __args__, opts=opts, typ=GetMitigationActionResult).value

    return AwaitableGetMitigationActionResult(
        action_params=__ret__.action_params,
        mitigation_action_arn=__ret__.mitigation_action_arn,
        mitigation_action_id=__ret__.mitigation_action_id,
        role_arn=__ret__.role_arn,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_mitigation_action)
def get_mitigation_action_output(action_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMitigationActionResult]:
    """
    Mitigation actions can be used to take actions to mitigate issues that were found in an Audit finding or Detect violation.


    :param str action_name: A unique identifier for the mitigation action.
    """
    ...
