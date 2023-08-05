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
    'GetTransitGatewayMulticastGroupMemberResult',
    'AwaitableGetTransitGatewayMulticastGroupMemberResult',
    'get_transit_gateway_multicast_group_member',
    'get_transit_gateway_multicast_group_member_output',
]

@pulumi.output_type
class GetTransitGatewayMulticastGroupMemberResult:
    def __init__(__self__, group_member=None, group_source=None, member_type=None, resource_id=None, resource_type=None, source_type=None, subnet_id=None, transit_gateway_attachment_id=None):
        if group_member and not isinstance(group_member, bool):
            raise TypeError("Expected argument 'group_member' to be a bool")
        pulumi.set(__self__, "group_member", group_member)
        if group_source and not isinstance(group_source, bool):
            raise TypeError("Expected argument 'group_source' to be a bool")
        pulumi.set(__self__, "group_source", group_source)
        if member_type and not isinstance(member_type, str):
            raise TypeError("Expected argument 'member_type' to be a str")
        pulumi.set(__self__, "member_type", member_type)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if source_type and not isinstance(source_type, str):
            raise TypeError("Expected argument 'source_type' to be a str")
        pulumi.set(__self__, "source_type", source_type)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if transit_gateway_attachment_id and not isinstance(transit_gateway_attachment_id, str):
            raise TypeError("Expected argument 'transit_gateway_attachment_id' to be a str")
        pulumi.set(__self__, "transit_gateway_attachment_id", transit_gateway_attachment_id)

    @property
    @pulumi.getter(name="groupMember")
    def group_member(self) -> Optional[bool]:
        """
        Indicates that the resource is a transit gateway multicast group member.
        """
        return pulumi.get(self, "group_member")

    @property
    @pulumi.getter(name="groupSource")
    def group_source(self) -> Optional[bool]:
        """
        Indicates that the resource is a transit gateway multicast group member.
        """
        return pulumi.get(self, "group_source")

    @property
    @pulumi.getter(name="memberType")
    def member_type(self) -> Optional[str]:
        """
        The member type (for example, static).
        """
        return pulumi.get(self, "member_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The type of resource, for example a VPC attachment.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> Optional[str]:
        """
        The source type.
        """
        return pulumi.get(self, "source_type")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The ID of the subnet.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> Optional[str]:
        """
        The ID of the transit gateway attachment.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")


class AwaitableGetTransitGatewayMulticastGroupMemberResult(GetTransitGatewayMulticastGroupMemberResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayMulticastGroupMemberResult(
            group_member=self.group_member,
            group_source=self.group_source,
            member_type=self.member_type,
            resource_id=self.resource_id,
            resource_type=self.resource_type,
            source_type=self.source_type,
            subnet_id=self.subnet_id,
            transit_gateway_attachment_id=self.transit_gateway_attachment_id)


def get_transit_gateway_multicast_group_member(group_ip_address: Optional[str] = None,
                                               network_interface_id: Optional[str] = None,
                                               transit_gateway_multicast_domain_id: Optional[str] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayMulticastGroupMemberResult:
    """
    The AWS::EC2::TransitGatewayMulticastGroupMember registers and deregisters members and sources (network interfaces) with the transit gateway multicast group


    :param str group_ip_address: The IP address assigned to the transit gateway multicast group.
    :param str network_interface_id: The ID of the transit gateway attachment.
    :param str transit_gateway_multicast_domain_id: The ID of the transit gateway multicast domain.
    """
    __args__ = dict()
    __args__['groupIpAddress'] = group_ip_address
    __args__['networkInterfaceId'] = network_interface_id
    __args__['transitGatewayMulticastDomainId'] = transit_gateway_multicast_domain_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getTransitGatewayMulticastGroupMember', __args__, opts=opts, typ=GetTransitGatewayMulticastGroupMemberResult).value

    return AwaitableGetTransitGatewayMulticastGroupMemberResult(
        group_member=__ret__.group_member,
        group_source=__ret__.group_source,
        member_type=__ret__.member_type,
        resource_id=__ret__.resource_id,
        resource_type=__ret__.resource_type,
        source_type=__ret__.source_type,
        subnet_id=__ret__.subnet_id,
        transit_gateway_attachment_id=__ret__.transit_gateway_attachment_id)


@_utilities.lift_output_func(get_transit_gateway_multicast_group_member)
def get_transit_gateway_multicast_group_member_output(group_ip_address: Optional[pulumi.Input[str]] = None,
                                                      network_interface_id: Optional[pulumi.Input[str]] = None,
                                                      transit_gateway_multicast_domain_id: Optional[pulumi.Input[str]] = None,
                                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayMulticastGroupMemberResult]:
    """
    The AWS::EC2::TransitGatewayMulticastGroupMember registers and deregisters members and sources (network interfaces) with the transit gateway multicast group


    :param str group_ip_address: The IP address assigned to the transit gateway multicast group.
    :param str network_interface_id: The ID of the transit gateway attachment.
    :param str transit_gateway_multicast_domain_id: The ID of the transit gateway multicast domain.
    """
    ...
