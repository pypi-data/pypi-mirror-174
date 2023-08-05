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
from ._inputs import *

__all__ = ['RepositoryArgs', 'Repository']

@pulumi.input_type
class RepositoryArgs:
    def __init__(__self__, *,
                 encryption_configuration: Optional[pulumi.Input['RepositoryEncryptionConfigurationArgs']] = None,
                 image_scanning_configuration: Optional[pulumi.Input['RepositoryImageScanningConfigurationArgs']] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input['RepositoryLifecyclePolicyArgs']] = None,
                 repository_name: Optional[pulumi.Input[str]] = None,
                 repository_policy_text: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryTagArgs']]]] = None):
        """
        The set of arguments for constructing a Repository resource.
        :param pulumi.Input['RepositoryImageTagMutability'] image_tag_mutability: The image tag mutability setting for the repository.
        :param pulumi.Input[str] repository_name: The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
        :param Any repository_policy_text: The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html in the Amazon Elastic Container Registry User Guide. 
        :param pulumi.Input[Sequence[pulumi.Input['RepositoryTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        if encryption_configuration is not None:
            pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if image_scanning_configuration is not None:
            pulumi.set(__self__, "image_scanning_configuration", image_scanning_configuration)
        if image_tag_mutability is not None:
            pulumi.set(__self__, "image_tag_mutability", image_tag_mutability)
        if lifecycle_policy is not None:
            pulumi.set(__self__, "lifecycle_policy", lifecycle_policy)
        if repository_name is not None:
            pulumi.set(__self__, "repository_name", repository_name)
        if repository_policy_text is not None:
            pulumi.set(__self__, "repository_policy_text", repository_policy_text)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional[pulumi.Input['RepositoryEncryptionConfigurationArgs']]:
        return pulumi.get(self, "encryption_configuration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: Optional[pulumi.Input['RepositoryEncryptionConfigurationArgs']]):
        pulumi.set(self, "encryption_configuration", value)

    @property
    @pulumi.getter(name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> Optional[pulumi.Input['RepositoryImageScanningConfigurationArgs']]:
        return pulumi.get(self, "image_scanning_configuration")

    @image_scanning_configuration.setter
    def image_scanning_configuration(self, value: Optional[pulumi.Input['RepositoryImageScanningConfigurationArgs']]):
        pulumi.set(self, "image_scanning_configuration", value)

    @property
    @pulumi.getter(name="imageTagMutability")
    def image_tag_mutability(self) -> Optional[pulumi.Input['RepositoryImageTagMutability']]:
        """
        The image tag mutability setting for the repository.
        """
        return pulumi.get(self, "image_tag_mutability")

    @image_tag_mutability.setter
    def image_tag_mutability(self, value: Optional[pulumi.Input['RepositoryImageTagMutability']]):
        pulumi.set(self, "image_tag_mutability", value)

    @property
    @pulumi.getter(name="lifecyclePolicy")
    def lifecycle_policy(self) -> Optional[pulumi.Input['RepositoryLifecyclePolicyArgs']]:
        return pulumi.get(self, "lifecycle_policy")

    @lifecycle_policy.setter
    def lifecycle_policy(self, value: Optional[pulumi.Input['RepositoryLifecyclePolicyArgs']]):
        pulumi.set(self, "lifecycle_policy", value)

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
        """
        return pulumi.get(self, "repository_name")

    @repository_name.setter
    def repository_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_name", value)

    @property
    @pulumi.getter(name="repositoryPolicyText")
    def repository_policy_text(self) -> Optional[Any]:
        """
        The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html in the Amazon Elastic Container Registry User Guide. 
        """
        return pulumi.get(self, "repository_policy_text")

    @repository_policy_text.setter
    def repository_policy_text(self, value: Optional[Any]):
        pulumi.set(self, "repository_policy_text", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Repository(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 encryption_configuration: Optional[pulumi.Input[pulumi.InputType['RepositoryEncryptionConfigurationArgs']]] = None,
                 image_scanning_configuration: Optional[pulumi.Input[pulumi.InputType['RepositoryImageScanningConfigurationArgs']]] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input[pulumi.InputType['RepositoryLifecyclePolicyArgs']]] = None,
                 repository_name: Optional[pulumi.Input[str]] = None,
                 repository_policy_text: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RepositoryTagArgs']]]]] = None,
                 __props__=None):
        """
        The AWS::ECR::Repository resource specifies an Amazon Elastic Container Registry (Amazon ECR) repository, where users can push and pull Docker images. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['RepositoryImageTagMutability'] image_tag_mutability: The image tag mutability setting for the repository.
        :param pulumi.Input[str] repository_name: The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
        :param Any repository_policy_text: The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html in the Amazon Elastic Container Registry User Guide. 
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RepositoryTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RepositoryArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::ECR::Repository resource specifies an Amazon Elastic Container Registry (Amazon ECR) repository, where users can push and pull Docker images. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html

        :param str resource_name: The name of the resource.
        :param RepositoryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RepositoryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 encryption_configuration: Optional[pulumi.Input[pulumi.InputType['RepositoryEncryptionConfigurationArgs']]] = None,
                 image_scanning_configuration: Optional[pulumi.Input[pulumi.InputType['RepositoryImageScanningConfigurationArgs']]] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input[pulumi.InputType['RepositoryLifecyclePolicyArgs']]] = None,
                 repository_name: Optional[pulumi.Input[str]] = None,
                 repository_policy_text: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RepositoryTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RepositoryArgs.__new__(RepositoryArgs)

            __props__.__dict__["encryption_configuration"] = encryption_configuration
            __props__.__dict__["image_scanning_configuration"] = image_scanning_configuration
            __props__.__dict__["image_tag_mutability"] = image_tag_mutability
            __props__.__dict__["lifecycle_policy"] = lifecycle_policy
            __props__.__dict__["repository_name"] = repository_name
            __props__.__dict__["repository_policy_text"] = repository_policy_text
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["repository_uri"] = None
        super(Repository, __self__).__init__(
            'aws-native:ecr:Repository',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Repository':
        """
        Get an existing Repository resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RepositoryArgs.__new__(RepositoryArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["encryption_configuration"] = None
        __props__.__dict__["image_scanning_configuration"] = None
        __props__.__dict__["image_tag_mutability"] = None
        __props__.__dict__["lifecycle_policy"] = None
        __props__.__dict__["repository_name"] = None
        __props__.__dict__["repository_policy_text"] = None
        __props__.__dict__["repository_uri"] = None
        __props__.__dict__["tags"] = None
        return Repository(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> pulumi.Output[Optional['outputs.RepositoryEncryptionConfiguration']]:
        return pulumi.get(self, "encryption_configuration")

    @property
    @pulumi.getter(name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> pulumi.Output[Optional['outputs.RepositoryImageScanningConfiguration']]:
        return pulumi.get(self, "image_scanning_configuration")

    @property
    @pulumi.getter(name="imageTagMutability")
    def image_tag_mutability(self) -> pulumi.Output[Optional['RepositoryImageTagMutability']]:
        """
        The image tag mutability setting for the repository.
        """
        return pulumi.get(self, "image_tag_mutability")

    @property
    @pulumi.getter(name="lifecyclePolicy")
    def lifecycle_policy(self) -> pulumi.Output[Optional['outputs.RepositoryLifecyclePolicy']]:
        return pulumi.get(self, "lifecycle_policy")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name to use for the repository. The repository name may be specified on its own (such as nginx-web-app) or it can be prepended with a namespace to group the repository into a category (such as project-a/nginx-web-app). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html.
        """
        return pulumi.get(self, "repository_name")

    @property
    @pulumi.getter(name="repositoryPolicyText")
    def repository_policy_text(self) -> pulumi.Output[Optional[Any]]:
        """
        The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html in the Amazon Elastic Container Registry User Guide. 
        """
        return pulumi.get(self, "repository_policy_text")

    @property
    @pulumi.getter(name="repositoryUri")
    def repository_uri(self) -> pulumi.Output[str]:
        return pulumi.get(self, "repository_uri")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.RepositoryTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

