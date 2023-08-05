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
    'GetSecurityGroupIngressResult',
    'AwaitableGetSecurityGroupIngressResult',
    'get_security_group_ingress',
    'get_security_group_ingress_output',
]

@pulumi.output_type
class GetSecurityGroupIngressResult:
    def __init__(__self__, description=None, id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")


class AwaitableGetSecurityGroupIngressResult(GetSecurityGroupIngressResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityGroupIngressResult(
            description=self.description,
            id=self.id)


def get_security_group_ingress(id: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityGroupIngressResult:
    """
    Resource Type definition for AWS::EC2::SecurityGroupIngress
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getSecurityGroupIngress', __args__, opts=opts, typ=GetSecurityGroupIngressResult).value

    return AwaitableGetSecurityGroupIngressResult(
        description=__ret__.description,
        id=__ret__.id)


@_utilities.lift_output_func(get_security_group_ingress)
def get_security_group_ingress_output(id: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecurityGroupIngressResult]:
    """
    Resource Type definition for AWS::EC2::SecurityGroupIngress
    """
    ...
