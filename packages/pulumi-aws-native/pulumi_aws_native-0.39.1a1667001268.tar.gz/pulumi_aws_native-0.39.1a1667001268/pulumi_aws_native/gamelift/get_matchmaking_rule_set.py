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
    'GetMatchmakingRuleSetResult',
    'AwaitableGetMatchmakingRuleSetResult',
    'get_matchmaking_rule_set',
    'get_matchmaking_rule_set_output',
]

@pulumi.output_type
class GetMatchmakingRuleSetResult:
    def __init__(__self__, arn=None, id=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.MatchmakingRuleSetTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetMatchmakingRuleSetResult(GetMatchmakingRuleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMatchmakingRuleSetResult(
            arn=self.arn,
            id=self.id,
            tags=self.tags)


def get_matchmaking_rule_set(id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMatchmakingRuleSetResult:
    """
    Resource Type definition for AWS::GameLift::MatchmakingRuleSet
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:gamelift:getMatchmakingRuleSet', __args__, opts=opts, typ=GetMatchmakingRuleSetResult).value

    return AwaitableGetMatchmakingRuleSetResult(
        arn=__ret__.arn,
        id=__ret__.id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_matchmaking_rule_set)
def get_matchmaking_rule_set_output(id: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMatchmakingRuleSetResult]:
    """
    Resource Type definition for AWS::GameLift::MatchmakingRuleSet
    """
    ...
