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
from ._inputs import *

__all__ = ['BucketArgs', 'Bucket']

@pulumi.input_type
class BucketArgs:
    def __init__(__self__, *,
                 bundle_id: pulumi.Input[str],
                 access_rules: Optional[pulumi.Input['BucketAccessRulesArgs']] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 object_versioning: Optional[pulumi.Input[bool]] = None,
                 read_only_access_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resources_receiving_access: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['BucketTagArgs']]]] = None):
        """
        The set of arguments for constructing a Bucket resource.
        :param pulumi.Input[str] bundle_id: The ID of the bundle to use for the bucket.
        :param pulumi.Input[str] bucket_name: The name for the bucket.
        :param pulumi.Input[bool] object_versioning: Specifies whether to enable or disable versioning of objects in the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] read_only_access_accounts: An array of strings to specify the AWS account IDs that can access the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources_receiving_access: The names of the Lightsail resources for which to set bucket access.
        :param pulumi.Input[Sequence[pulumi.Input['BucketTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "bundle_id", bundle_id)
        if access_rules is not None:
            pulumi.set(__self__, "access_rules", access_rules)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if object_versioning is not None:
            pulumi.set(__self__, "object_versioning", object_versioning)
        if read_only_access_accounts is not None:
            pulumi.set(__self__, "read_only_access_accounts", read_only_access_accounts)
        if resources_receiving_access is not None:
            pulumi.set(__self__, "resources_receiving_access", resources_receiving_access)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> pulumi.Input[str]:
        """
        The ID of the bundle to use for the bucket.
        """
        return pulumi.get(self, "bundle_id")

    @bundle_id.setter
    def bundle_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "bundle_id", value)

    @property
    @pulumi.getter(name="accessRules")
    def access_rules(self) -> Optional[pulumi.Input['BucketAccessRulesArgs']]:
        return pulumi.get(self, "access_rules")

    @access_rules.setter
    def access_rules(self, value: Optional[pulumi.Input['BucketAccessRulesArgs']]):
        pulumi.set(self, "access_rules", value)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the bucket.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="objectVersioning")
    def object_versioning(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable or disable versioning of objects in the bucket.
        """
        return pulumi.get(self, "object_versioning")

    @object_versioning.setter
    def object_versioning(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "object_versioning", value)

    @property
    @pulumi.getter(name="readOnlyAccessAccounts")
    def read_only_access_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of strings to specify the AWS account IDs that can access the bucket.
        """
        return pulumi.get(self, "read_only_access_accounts")

    @read_only_access_accounts.setter
    def read_only_access_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "read_only_access_accounts", value)

    @property
    @pulumi.getter(name="resourcesReceivingAccess")
    def resources_receiving_access(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The names of the Lightsail resources for which to set bucket access.
        """
        return pulumi.get(self, "resources_receiving_access")

    @resources_receiving_access.setter
    def resources_receiving_access(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources_receiving_access", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Bucket(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_rules: Optional[pulumi.Input[pulumi.InputType['BucketAccessRulesArgs']]] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 object_versioning: Optional[pulumi.Input[bool]] = None,
                 read_only_access_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resources_receiving_access: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Lightsail::Bucket

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket_name: The name for the bucket.
        :param pulumi.Input[str] bundle_id: The ID of the bundle to use for the bucket.
        :param pulumi.Input[bool] object_versioning: Specifies whether to enable or disable versioning of objects in the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] read_only_access_accounts: An array of strings to specify the AWS account IDs that can access the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources_receiving_access: The names of the Lightsail resources for which to set bucket access.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Lightsail::Bucket

        :param str resource_name: The name of the resource.
        :param BucketArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_rules: Optional[pulumi.Input[pulumi.InputType['BucketAccessRulesArgs']]] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 object_versioning: Optional[pulumi.Input[bool]] = None,
                 read_only_access_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resources_receiving_access: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketArgs.__new__(BucketArgs)

            __props__.__dict__["access_rules"] = access_rules
            __props__.__dict__["bucket_name"] = bucket_name
            if bundle_id is None and not opts.urn:
                raise TypeError("Missing required property 'bundle_id'")
            __props__.__dict__["bundle_id"] = bundle_id
            __props__.__dict__["object_versioning"] = object_versioning
            __props__.__dict__["read_only_access_accounts"] = read_only_access_accounts
            __props__.__dict__["resources_receiving_access"] = resources_receiving_access
            __props__.__dict__["tags"] = tags
            __props__.__dict__["able_to_update_bundle"] = None
            __props__.__dict__["bucket_arn"] = None
            __props__.__dict__["url"] = None
        super(Bucket, __self__).__init__(
            'aws-native:lightsail:Bucket',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Bucket':
        """
        Get an existing Bucket resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BucketArgs.__new__(BucketArgs)

        __props__.__dict__["able_to_update_bundle"] = None
        __props__.__dict__["access_rules"] = None
        __props__.__dict__["bucket_arn"] = None
        __props__.__dict__["bucket_name"] = None
        __props__.__dict__["bundle_id"] = None
        __props__.__dict__["object_versioning"] = None
        __props__.__dict__["read_only_access_accounts"] = None
        __props__.__dict__["resources_receiving_access"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["url"] = None
        return Bucket(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="ableToUpdateBundle")
    def able_to_update_bundle(self) -> pulumi.Output[bool]:
        """
        Indicates whether the bundle that is currently applied to a bucket can be changed to another bundle. You can update a bucket's bundle only one time within a monthly AWS billing cycle.
        """
        return pulumi.get(self, "able_to_update_bundle")

    @property
    @pulumi.getter(name="accessRules")
    def access_rules(self) -> pulumi.Output[Optional['outputs.BucketAccessRules']]:
        return pulumi.get(self, "access_rules")

    @property
    @pulumi.getter(name="bucketArn")
    def bucket_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bucket_arn")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Output[str]:
        """
        The name for the bucket.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> pulumi.Output[str]:
        """
        The ID of the bundle to use for the bucket.
        """
        return pulumi.get(self, "bundle_id")

    @property
    @pulumi.getter(name="objectVersioning")
    def object_versioning(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to enable or disable versioning of objects in the bucket.
        """
        return pulumi.get(self, "object_versioning")

    @property
    @pulumi.getter(name="readOnlyAccessAccounts")
    def read_only_access_accounts(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        An array of strings to specify the AWS account IDs that can access the bucket.
        """
        return pulumi.get(self, "read_only_access_accounts")

    @property
    @pulumi.getter(name="resourcesReceivingAccess")
    def resources_receiving_access(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The names of the Lightsail resources for which to set bucket access.
        """
        return pulumi.get(self, "resources_receiving_access")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.BucketTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The URL of the bucket.
        """
        return pulumi.get(self, "url")

