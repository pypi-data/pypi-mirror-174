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

__all__ = ['DataCatalogEncryptionSettingsInitArgs', 'DataCatalogEncryptionSettings']

@pulumi.input_type
class DataCatalogEncryptionSettingsInitArgs:
    def __init__(__self__, *,
                 catalog_id: pulumi.Input[str],
                 data_catalog_encryption_settings: pulumi.Input['DataCatalogEncryptionSettingsArgs']):
        """
        The set of arguments for constructing a DataCatalogEncryptionSettings resource.
        """
        pulumi.set(__self__, "catalog_id", catalog_id)
        pulumi.set(__self__, "data_catalog_encryption_settings", data_catalog_encryption_settings)

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "catalog_id")

    @catalog_id.setter
    def catalog_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "catalog_id", value)

    @property
    @pulumi.getter(name="dataCatalogEncryptionSettings")
    def data_catalog_encryption_settings(self) -> pulumi.Input['DataCatalogEncryptionSettingsArgs']:
        return pulumi.get(self, "data_catalog_encryption_settings")

    @data_catalog_encryption_settings.setter
    def data_catalog_encryption_settings(self, value: pulumi.Input['DataCatalogEncryptionSettingsArgs']):
        pulumi.set(self, "data_catalog_encryption_settings", value)


warnings.warn("""DataCatalogEncryptionSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class DataCatalogEncryptionSettings(pulumi.CustomResource):
    warnings.warn("""DataCatalogEncryptionSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 data_catalog_encryption_settings: Optional[pulumi.Input[pulumi.InputType['DataCatalogEncryptionSettingsArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Glue::DataCatalogEncryptionSettings

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataCatalogEncryptionSettingsInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Glue::DataCatalogEncryptionSettings

        :param str resource_name: The name of the resource.
        :param DataCatalogEncryptionSettingsInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataCatalogEncryptionSettingsInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 data_catalog_encryption_settings: Optional[pulumi.Input[pulumi.InputType['DataCatalogEncryptionSettingsArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""DataCatalogEncryptionSettings is deprecated: DataCatalogEncryptionSettings is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataCatalogEncryptionSettingsInitArgs.__new__(DataCatalogEncryptionSettingsInitArgs)

            if catalog_id is None and not opts.urn:
                raise TypeError("Missing required property 'catalog_id'")
            __props__.__dict__["catalog_id"] = catalog_id
            if data_catalog_encryption_settings is None and not opts.urn:
                raise TypeError("Missing required property 'data_catalog_encryption_settings'")
            __props__.__dict__["data_catalog_encryption_settings"] = data_catalog_encryption_settings
        super(DataCatalogEncryptionSettings, __self__).__init__(
            'aws-native:glue:DataCatalogEncryptionSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DataCatalogEncryptionSettings':
        """
        Get an existing DataCatalogEncryptionSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DataCatalogEncryptionSettingsInitArgs.__new__(DataCatalogEncryptionSettingsInitArgs)

        __props__.__dict__["catalog_id"] = None
        __props__.__dict__["data_catalog_encryption_settings"] = None
        return DataCatalogEncryptionSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "catalog_id")

    @property
    @pulumi.getter(name="dataCatalogEncryptionSettings")
    def data_catalog_encryption_settings(self) -> pulumi.Output['outputs.DataCatalogEncryptionSettings']:
        return pulumi.get(self, "data_catalog_encryption_settings")

