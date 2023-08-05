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

__all__ = ['ClusterArgs', 'Cluster']

@pulumi.input_type
class ClusterArgs:
    def __init__(__self__, *,
                 instances: pulumi.Input['ClusterJobFlowInstancesConfigArgs'],
                 job_flow_role: pulumi.Input[str],
                 service_role: pulumi.Input[str],
                 additional_info: Optional[Any] = None,
                 applications: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterApplicationArgs']]]] = None,
                 auto_scaling_role: Optional[pulumi.Input[str]] = None,
                 auto_termination_policy: Optional[pulumi.Input['ClusterAutoTerminationPolicyArgs']] = None,
                 bootstrap_actions: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterBootstrapActionConfigArgs']]]] = None,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterConfigurationArgs']]]] = None,
                 custom_ami_id: Optional[pulumi.Input[str]] = None,
                 ebs_root_volume_size: Optional[pulumi.Input[int]] = None,
                 kerberos_attributes: Optional[pulumi.Input['ClusterKerberosAttributesArgs']] = None,
                 log_encryption_kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_uri: Optional[pulumi.Input[str]] = None,
                 managed_scaling_policy: Optional[pulumi.Input['ClusterManagedScalingPolicyArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 release_label: Optional[pulumi.Input[str]] = None,
                 scale_down_behavior: Optional[pulumi.Input[str]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 step_concurrency_level: Optional[pulumi.Input[int]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterStepConfigArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterTagArgs']]]] = None,
                 visible_to_all_users: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Cluster resource.
        """
        pulumi.set(__self__, "instances", instances)
        pulumi.set(__self__, "job_flow_role", job_flow_role)
        pulumi.set(__self__, "service_role", service_role)
        if additional_info is not None:
            pulumi.set(__self__, "additional_info", additional_info)
        if applications is not None:
            pulumi.set(__self__, "applications", applications)
        if auto_scaling_role is not None:
            pulumi.set(__self__, "auto_scaling_role", auto_scaling_role)
        if auto_termination_policy is not None:
            pulumi.set(__self__, "auto_termination_policy", auto_termination_policy)
        if bootstrap_actions is not None:
            pulumi.set(__self__, "bootstrap_actions", bootstrap_actions)
        if configurations is not None:
            pulumi.set(__self__, "configurations", configurations)
        if custom_ami_id is not None:
            pulumi.set(__self__, "custom_ami_id", custom_ami_id)
        if ebs_root_volume_size is not None:
            pulumi.set(__self__, "ebs_root_volume_size", ebs_root_volume_size)
        if kerberos_attributes is not None:
            pulumi.set(__self__, "kerberos_attributes", kerberos_attributes)
        if log_encryption_kms_key_id is not None:
            pulumi.set(__self__, "log_encryption_kms_key_id", log_encryption_kms_key_id)
        if log_uri is not None:
            pulumi.set(__self__, "log_uri", log_uri)
        if managed_scaling_policy is not None:
            pulumi.set(__self__, "managed_scaling_policy", managed_scaling_policy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if release_label is not None:
            pulumi.set(__self__, "release_label", release_label)
        if scale_down_behavior is not None:
            pulumi.set(__self__, "scale_down_behavior", scale_down_behavior)
        if security_configuration is not None:
            pulumi.set(__self__, "security_configuration", security_configuration)
        if step_concurrency_level is not None:
            pulumi.set(__self__, "step_concurrency_level", step_concurrency_level)
        if steps is not None:
            pulumi.set(__self__, "steps", steps)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if visible_to_all_users is not None:
            pulumi.set(__self__, "visible_to_all_users", visible_to_all_users)

    @property
    @pulumi.getter
    def instances(self) -> pulumi.Input['ClusterJobFlowInstancesConfigArgs']:
        return pulumi.get(self, "instances")

    @instances.setter
    def instances(self, value: pulumi.Input['ClusterJobFlowInstancesConfigArgs']):
        pulumi.set(self, "instances", value)

    @property
    @pulumi.getter(name="jobFlowRole")
    def job_flow_role(self) -> pulumi.Input[str]:
        return pulumi.get(self, "job_flow_role")

    @job_flow_role.setter
    def job_flow_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "job_flow_role", value)

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Input[str]:
        return pulumi.get(self, "service_role")

    @service_role.setter
    def service_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_role", value)

    @property
    @pulumi.getter(name="additionalInfo")
    def additional_info(self) -> Optional[Any]:
        return pulumi.get(self, "additional_info")

    @additional_info.setter
    def additional_info(self, value: Optional[Any]):
        pulumi.set(self, "additional_info", value)

    @property
    @pulumi.getter
    def applications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterApplicationArgs']]]]:
        return pulumi.get(self, "applications")

    @applications.setter
    def applications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterApplicationArgs']]]]):
        pulumi.set(self, "applications", value)

    @property
    @pulumi.getter(name="autoScalingRole")
    def auto_scaling_role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "auto_scaling_role")

    @auto_scaling_role.setter
    def auto_scaling_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_scaling_role", value)

    @property
    @pulumi.getter(name="autoTerminationPolicy")
    def auto_termination_policy(self) -> Optional[pulumi.Input['ClusterAutoTerminationPolicyArgs']]:
        return pulumi.get(self, "auto_termination_policy")

    @auto_termination_policy.setter
    def auto_termination_policy(self, value: Optional[pulumi.Input['ClusterAutoTerminationPolicyArgs']]):
        pulumi.set(self, "auto_termination_policy", value)

    @property
    @pulumi.getter(name="bootstrapActions")
    def bootstrap_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterBootstrapActionConfigArgs']]]]:
        return pulumi.get(self, "bootstrap_actions")

    @bootstrap_actions.setter
    def bootstrap_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterBootstrapActionConfigArgs']]]]):
        pulumi.set(self, "bootstrap_actions", value)

    @property
    @pulumi.getter
    def configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterConfigurationArgs']]]]:
        return pulumi.get(self, "configurations")

    @configurations.setter
    def configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterConfigurationArgs']]]]):
        pulumi.set(self, "configurations", value)

    @property
    @pulumi.getter(name="customAmiId")
    def custom_ami_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "custom_ami_id")

    @custom_ami_id.setter
    def custom_ami_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_ami_id", value)

    @property
    @pulumi.getter(name="ebsRootVolumeSize")
    def ebs_root_volume_size(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "ebs_root_volume_size")

    @ebs_root_volume_size.setter
    def ebs_root_volume_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ebs_root_volume_size", value)

    @property
    @pulumi.getter(name="kerberosAttributes")
    def kerberos_attributes(self) -> Optional[pulumi.Input['ClusterKerberosAttributesArgs']]:
        return pulumi.get(self, "kerberos_attributes")

    @kerberos_attributes.setter
    def kerberos_attributes(self, value: Optional[pulumi.Input['ClusterKerberosAttributesArgs']]):
        pulumi.set(self, "kerberos_attributes", value)

    @property
    @pulumi.getter(name="logEncryptionKmsKeyId")
    def log_encryption_kms_key_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "log_encryption_kms_key_id")

    @log_encryption_kms_key_id.setter
    def log_encryption_kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_encryption_kms_key_id", value)

    @property
    @pulumi.getter(name="logUri")
    def log_uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "log_uri")

    @log_uri.setter
    def log_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_uri", value)

    @property
    @pulumi.getter(name="managedScalingPolicy")
    def managed_scaling_policy(self) -> Optional[pulumi.Input['ClusterManagedScalingPolicyArgs']]:
        return pulumi.get(self, "managed_scaling_policy")

    @managed_scaling_policy.setter
    def managed_scaling_policy(self, value: Optional[pulumi.Input['ClusterManagedScalingPolicyArgs']]):
        pulumi.set(self, "managed_scaling_policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="releaseLabel")
    def release_label(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "release_label")

    @release_label.setter
    def release_label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "release_label", value)

    @property
    @pulumi.getter(name="scaleDownBehavior")
    def scale_down_behavior(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "scale_down_behavior")

    @scale_down_behavior.setter
    def scale_down_behavior(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scale_down_behavior", value)

    @property
    @pulumi.getter(name="securityConfiguration")
    def security_configuration(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "security_configuration")

    @security_configuration.setter
    def security_configuration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_configuration", value)

    @property
    @pulumi.getter(name="stepConcurrencyLevel")
    def step_concurrency_level(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "step_concurrency_level")

    @step_concurrency_level.setter
    def step_concurrency_level(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "step_concurrency_level", value)

    @property
    @pulumi.getter
    def steps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterStepConfigArgs']]]]:
        return pulumi.get(self, "steps")

    @steps.setter
    def steps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterStepConfigArgs']]]]):
        pulumi.set(self, "steps", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="visibleToAllUsers")
    def visible_to_all_users(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "visible_to_all_users")

    @visible_to_all_users.setter
    def visible_to_all_users(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "visible_to_all_users", value)


warnings.warn("""Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Cluster(pulumi.CustomResource):
    warnings.warn("""Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_info: Optional[Any] = None,
                 applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterApplicationArgs']]]]] = None,
                 auto_scaling_role: Optional[pulumi.Input[str]] = None,
                 auto_termination_policy: Optional[pulumi.Input[pulumi.InputType['ClusterAutoTerminationPolicyArgs']]] = None,
                 bootstrap_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterBootstrapActionConfigArgs']]]]] = None,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterConfigurationArgs']]]]] = None,
                 custom_ami_id: Optional[pulumi.Input[str]] = None,
                 ebs_root_volume_size: Optional[pulumi.Input[int]] = None,
                 instances: Optional[pulumi.Input[pulumi.InputType['ClusterJobFlowInstancesConfigArgs']]] = None,
                 job_flow_role: Optional[pulumi.Input[str]] = None,
                 kerberos_attributes: Optional[pulumi.Input[pulumi.InputType['ClusterKerberosAttributesArgs']]] = None,
                 log_encryption_kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_uri: Optional[pulumi.Input[str]] = None,
                 managed_scaling_policy: Optional[pulumi.Input[pulumi.InputType['ClusterManagedScalingPolicyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 release_label: Optional[pulumi.Input[str]] = None,
                 scale_down_behavior: Optional[pulumi.Input[str]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 step_concurrency_level: Optional[pulumi.Input[int]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterStepConfigArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterTagArgs']]]]] = None,
                 visible_to_all_users: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::EMR::Cluster

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::EMR::Cluster

        :param str resource_name: The name of the resource.
        :param ClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_info: Optional[Any] = None,
                 applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterApplicationArgs']]]]] = None,
                 auto_scaling_role: Optional[pulumi.Input[str]] = None,
                 auto_termination_policy: Optional[pulumi.Input[pulumi.InputType['ClusterAutoTerminationPolicyArgs']]] = None,
                 bootstrap_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterBootstrapActionConfigArgs']]]]] = None,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterConfigurationArgs']]]]] = None,
                 custom_ami_id: Optional[pulumi.Input[str]] = None,
                 ebs_root_volume_size: Optional[pulumi.Input[int]] = None,
                 instances: Optional[pulumi.Input[pulumi.InputType['ClusterJobFlowInstancesConfigArgs']]] = None,
                 job_flow_role: Optional[pulumi.Input[str]] = None,
                 kerberos_attributes: Optional[pulumi.Input[pulumi.InputType['ClusterKerberosAttributesArgs']]] = None,
                 log_encryption_kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_uri: Optional[pulumi.Input[str]] = None,
                 managed_scaling_policy: Optional[pulumi.Input[pulumi.InputType['ClusterManagedScalingPolicyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 release_label: Optional[pulumi.Input[str]] = None,
                 scale_down_behavior: Optional[pulumi.Input[str]] = None,
                 security_configuration: Optional[pulumi.Input[str]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 step_concurrency_level: Optional[pulumi.Input[int]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterStepConfigArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterTagArgs']]]]] = None,
                 visible_to_all_users: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        pulumi.log.warn("""Cluster is deprecated: Cluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterArgs.__new__(ClusterArgs)

            __props__.__dict__["additional_info"] = additional_info
            __props__.__dict__["applications"] = applications
            __props__.__dict__["auto_scaling_role"] = auto_scaling_role
            __props__.__dict__["auto_termination_policy"] = auto_termination_policy
            __props__.__dict__["bootstrap_actions"] = bootstrap_actions
            __props__.__dict__["configurations"] = configurations
            __props__.__dict__["custom_ami_id"] = custom_ami_id
            __props__.__dict__["ebs_root_volume_size"] = ebs_root_volume_size
            if instances is None and not opts.urn:
                raise TypeError("Missing required property 'instances'")
            __props__.__dict__["instances"] = instances
            if job_flow_role is None and not opts.urn:
                raise TypeError("Missing required property 'job_flow_role'")
            __props__.__dict__["job_flow_role"] = job_flow_role
            __props__.__dict__["kerberos_attributes"] = kerberos_attributes
            __props__.__dict__["log_encryption_kms_key_id"] = log_encryption_kms_key_id
            __props__.__dict__["log_uri"] = log_uri
            __props__.__dict__["managed_scaling_policy"] = managed_scaling_policy
            __props__.__dict__["name"] = name
            __props__.__dict__["release_label"] = release_label
            __props__.__dict__["scale_down_behavior"] = scale_down_behavior
            __props__.__dict__["security_configuration"] = security_configuration
            if service_role is None and not opts.urn:
                raise TypeError("Missing required property 'service_role'")
            __props__.__dict__["service_role"] = service_role
            __props__.__dict__["step_concurrency_level"] = step_concurrency_level
            __props__.__dict__["steps"] = steps
            __props__.__dict__["tags"] = tags
            __props__.__dict__["visible_to_all_users"] = visible_to_all_users
            __props__.__dict__["master_public_dns"] = None
        super(Cluster, __self__).__init__(
            'aws-native:emr:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterArgs.__new__(ClusterArgs)

        __props__.__dict__["additional_info"] = None
        __props__.__dict__["applications"] = None
        __props__.__dict__["auto_scaling_role"] = None
        __props__.__dict__["auto_termination_policy"] = None
        __props__.__dict__["bootstrap_actions"] = None
        __props__.__dict__["configurations"] = None
        __props__.__dict__["custom_ami_id"] = None
        __props__.__dict__["ebs_root_volume_size"] = None
        __props__.__dict__["instances"] = None
        __props__.__dict__["job_flow_role"] = None
        __props__.__dict__["kerberos_attributes"] = None
        __props__.__dict__["log_encryption_kms_key_id"] = None
        __props__.__dict__["log_uri"] = None
        __props__.__dict__["managed_scaling_policy"] = None
        __props__.__dict__["master_public_dns"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["release_label"] = None
        __props__.__dict__["scale_down_behavior"] = None
        __props__.__dict__["security_configuration"] = None
        __props__.__dict__["service_role"] = None
        __props__.__dict__["step_concurrency_level"] = None
        __props__.__dict__["steps"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["visible_to_all_users"] = None
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="additionalInfo")
    def additional_info(self) -> pulumi.Output[Optional[Any]]:
        return pulumi.get(self, "additional_info")

    @property
    @pulumi.getter
    def applications(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterApplication']]]:
        return pulumi.get(self, "applications")

    @property
    @pulumi.getter(name="autoScalingRole")
    def auto_scaling_role(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "auto_scaling_role")

    @property
    @pulumi.getter(name="autoTerminationPolicy")
    def auto_termination_policy(self) -> pulumi.Output[Optional['outputs.ClusterAutoTerminationPolicy']]:
        return pulumi.get(self, "auto_termination_policy")

    @property
    @pulumi.getter(name="bootstrapActions")
    def bootstrap_actions(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterBootstrapActionConfig']]]:
        return pulumi.get(self, "bootstrap_actions")

    @property
    @pulumi.getter
    def configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterConfiguration']]]:
        return pulumi.get(self, "configurations")

    @property
    @pulumi.getter(name="customAmiId")
    def custom_ami_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "custom_ami_id")

    @property
    @pulumi.getter(name="ebsRootVolumeSize")
    def ebs_root_volume_size(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "ebs_root_volume_size")

    @property
    @pulumi.getter
    def instances(self) -> pulumi.Output['outputs.ClusterJobFlowInstancesConfig']:
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="jobFlowRole")
    def job_flow_role(self) -> pulumi.Output[str]:
        return pulumi.get(self, "job_flow_role")

    @property
    @pulumi.getter(name="kerberosAttributes")
    def kerberos_attributes(self) -> pulumi.Output[Optional['outputs.ClusterKerberosAttributes']]:
        return pulumi.get(self, "kerberos_attributes")

    @property
    @pulumi.getter(name="logEncryptionKmsKeyId")
    def log_encryption_kms_key_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "log_encryption_kms_key_id")

    @property
    @pulumi.getter(name="logUri")
    def log_uri(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "log_uri")

    @property
    @pulumi.getter(name="managedScalingPolicy")
    def managed_scaling_policy(self) -> pulumi.Output[Optional['outputs.ClusterManagedScalingPolicy']]:
        return pulumi.get(self, "managed_scaling_policy")

    @property
    @pulumi.getter(name="masterPublicDNS")
    def master_public_dns(self) -> pulumi.Output[str]:
        return pulumi.get(self, "master_public_dns")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="releaseLabel")
    def release_label(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "release_label")

    @property
    @pulumi.getter(name="scaleDownBehavior")
    def scale_down_behavior(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "scale_down_behavior")

    @property
    @pulumi.getter(name="securityConfiguration")
    def security_configuration(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "security_configuration")

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Output[str]:
        return pulumi.get(self, "service_role")

    @property
    @pulumi.getter(name="stepConcurrencyLevel")
    def step_concurrency_level(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "step_concurrency_level")

    @property
    @pulumi.getter
    def steps(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterStepConfig']]]:
        return pulumi.get(self, "steps")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="visibleToAllUsers")
    def visible_to_all_users(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "visible_to_all_users")

