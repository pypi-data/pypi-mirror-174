# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GrantArgs', 'Grant']

@pulumi.input_type
class GrantArgs:
    def __init__(__self__, *,
                 allowed_operations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 grant_name: Optional[pulumi.Input[str]] = None,
                 home_region: Optional[pulumi.Input[str]] = None,
                 license_arn: Optional[pulumi.Input[str]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Grant resource.
        :param pulumi.Input[str] grant_name: Name for the created Grant.
        :param pulumi.Input[str] home_region: Home region for the created grant.
        :param pulumi.Input[str] license_arn: License Arn for the grant.
        """
        if allowed_operations is not None:
            pulumi.set(__self__, "allowed_operations", allowed_operations)
        if grant_name is not None:
            pulumi.set(__self__, "grant_name", grant_name)
        if home_region is not None:
            pulumi.set(__self__, "home_region", home_region)
        if license_arn is not None:
            pulumi.set(__self__, "license_arn", license_arn)
        if principals is not None:
            pulumi.set(__self__, "principals", principals)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="allowedOperations")
    def allowed_operations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "allowed_operations")

    @allowed_operations.setter
    def allowed_operations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_operations", value)

    @property
    @pulumi.getter(name="grantName")
    def grant_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for the created Grant.
        """
        return pulumi.get(self, "grant_name")

    @grant_name.setter
    def grant_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "grant_name", value)

    @property
    @pulumi.getter(name="homeRegion")
    def home_region(self) -> Optional[pulumi.Input[str]]:
        """
        Home region for the created grant.
        """
        return pulumi.get(self, "home_region")

    @home_region.setter
    def home_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "home_region", value)

    @property
    @pulumi.getter(name="licenseArn")
    def license_arn(self) -> Optional[pulumi.Input[str]]:
        """
        License Arn for the grant.
        """
        return pulumi.get(self, "license_arn")

    @license_arn.setter
    def license_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "license_arn", value)

    @property
    @pulumi.getter
    def principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "principals")

    @principals.setter
    def principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "principals", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class Grant(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_operations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 grant_name: Optional[pulumi.Input[str]] = None,
                 home_region: Optional[pulumi.Input[str]] = None,
                 license_arn: Optional[pulumi.Input[str]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An example resource schema demonstrating some basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] grant_name: Name for the created Grant.
        :param pulumi.Input[str] home_region: Home region for the created grant.
        :param pulumi.Input[str] license_arn: License Arn for the grant.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GrantArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An example resource schema demonstrating some basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param GrantArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GrantArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_operations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 grant_name: Optional[pulumi.Input[str]] = None,
                 home_region: Optional[pulumi.Input[str]] = None,
                 license_arn: Optional[pulumi.Input[str]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GrantArgs.__new__(GrantArgs)

            __props__.__dict__["allowed_operations"] = allowed_operations
            __props__.__dict__["grant_name"] = grant_name
            __props__.__dict__["home_region"] = home_region
            __props__.__dict__["license_arn"] = license_arn
            __props__.__dict__["principals"] = principals
            __props__.__dict__["status"] = status
            __props__.__dict__["grant_arn"] = None
            __props__.__dict__["version"] = None
        super(Grant, __self__).__init__(
            'aws-native:licensemanager:Grant',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Grant':
        """
        Get an existing Grant resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GrantArgs.__new__(GrantArgs)

        __props__.__dict__["allowed_operations"] = None
        __props__.__dict__["grant_arn"] = None
        __props__.__dict__["grant_name"] = None
        __props__.__dict__["home_region"] = None
        __props__.__dict__["license_arn"] = None
        __props__.__dict__["principals"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["version"] = None
        return Grant(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedOperations")
    def allowed_operations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "allowed_operations")

    @property
    @pulumi.getter(name="grantArn")
    def grant_arn(self) -> pulumi.Output[str]:
        """
        Arn of the grant.
        """
        return pulumi.get(self, "grant_arn")

    @property
    @pulumi.getter(name="grantName")
    def grant_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name for the created Grant.
        """
        return pulumi.get(self, "grant_name")

    @property
    @pulumi.getter(name="homeRegion")
    def home_region(self) -> pulumi.Output[Optional[str]]:
        """
        Home region for the created grant.
        """
        return pulumi.get(self, "home_region")

    @property
    @pulumi.getter(name="licenseArn")
    def license_arn(self) -> pulumi.Output[Optional[str]]:
        """
        License Arn for the grant.
        """
        return pulumi.get(self, "license_arn")

    @property
    @pulumi.getter
    def principals(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "principals")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version of the grant.
        """
        return pulumi.get(self, "version")

