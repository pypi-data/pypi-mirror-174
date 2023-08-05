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

__all__ = ['CanaryArgs', 'Canary']

@pulumi.input_type
class CanaryArgs:
    def __init__(__self__, *,
                 artifact_s3_location: pulumi.Input[str],
                 code: pulumi.Input['CanaryCodeArgs'],
                 execution_role_arn: pulumi.Input[str],
                 runtime_version: pulumi.Input[str],
                 schedule: pulumi.Input['CanaryScheduleArgs'],
                 start_canary_after_creation: pulumi.Input[bool],
                 artifact_config: Optional[pulumi.Input['CanaryArtifactConfigArgs']] = None,
                 delete_lambda_resources_on_canary_deletion: Optional[pulumi.Input[bool]] = None,
                 failure_retention_period: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 run_config: Optional[pulumi.Input['CanaryRunConfigArgs']] = None,
                 success_retention_period: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['CanaryTagArgs']]]] = None,
                 v_pc_config: Optional[pulumi.Input['CanaryVPCConfigArgs']] = None,
                 visual_reference: Optional[pulumi.Input['CanaryVisualReferenceArgs']] = None):
        """
        The set of arguments for constructing a Canary resource.
        :param pulumi.Input[str] artifact_s3_location: Provide the s3 bucket output location for test results
        :param pulumi.Input['CanaryCodeArgs'] code: Provide the canary script source
        :param pulumi.Input[str] execution_role_arn: Lambda Execution role used to run your canaries
        :param pulumi.Input[str] runtime_version: Runtime version of Synthetics Library
        :param pulumi.Input['CanaryScheduleArgs'] schedule: Frequency to run your canaries
        :param pulumi.Input[bool] start_canary_after_creation: Runs canary if set to True. Default is False
        :param pulumi.Input['CanaryArtifactConfigArgs'] artifact_config: Provide artifact configuration
        :param pulumi.Input[bool] delete_lambda_resources_on_canary_deletion: Deletes associated lambda resources created by Synthetics if set to True. Default is False
        :param pulumi.Input[int] failure_retention_period: Retention period of failed canary runs represented in number of days
        :param pulumi.Input[str] name: Name of the canary.
        :param pulumi.Input['CanaryRunConfigArgs'] run_config: Provide canary run configuration
        :param pulumi.Input[int] success_retention_period: Retention period of successful canary runs represented in number of days
        :param pulumi.Input['CanaryVPCConfigArgs'] v_pc_config: Provide VPC Configuration if enabled.
        :param pulumi.Input['CanaryVisualReferenceArgs'] visual_reference: Visual reference configuration for visual testing
        """
        pulumi.set(__self__, "artifact_s3_location", artifact_s3_location)
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "execution_role_arn", execution_role_arn)
        pulumi.set(__self__, "runtime_version", runtime_version)
        pulumi.set(__self__, "schedule", schedule)
        pulumi.set(__self__, "start_canary_after_creation", start_canary_after_creation)
        if artifact_config is not None:
            pulumi.set(__self__, "artifact_config", artifact_config)
        if delete_lambda_resources_on_canary_deletion is not None:
            pulumi.set(__self__, "delete_lambda_resources_on_canary_deletion", delete_lambda_resources_on_canary_deletion)
        if failure_retention_period is not None:
            pulumi.set(__self__, "failure_retention_period", failure_retention_period)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if run_config is not None:
            pulumi.set(__self__, "run_config", run_config)
        if success_retention_period is not None:
            pulumi.set(__self__, "success_retention_period", success_retention_period)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if v_pc_config is not None:
            pulumi.set(__self__, "v_pc_config", v_pc_config)
        if visual_reference is not None:
            pulumi.set(__self__, "visual_reference", visual_reference)

    @property
    @pulumi.getter(name="artifactS3Location")
    def artifact_s3_location(self) -> pulumi.Input[str]:
        """
        Provide the s3 bucket output location for test results
        """
        return pulumi.get(self, "artifact_s3_location")

    @artifact_s3_location.setter
    def artifact_s3_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "artifact_s3_location", value)

    @property
    @pulumi.getter
    def code(self) -> pulumi.Input['CanaryCodeArgs']:
        """
        Provide the canary script source
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: pulumi.Input['CanaryCodeArgs']):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> pulumi.Input[str]:
        """
        Lambda Execution role used to run your canaries
        """
        return pulumi.get(self, "execution_role_arn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "execution_role_arn", value)

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> pulumi.Input[str]:
        """
        Runtime version of Synthetics Library
        """
        return pulumi.get(self, "runtime_version")

    @runtime_version.setter
    def runtime_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "runtime_version", value)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input['CanaryScheduleArgs']:
        """
        Frequency to run your canaries
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: pulumi.Input['CanaryScheduleArgs']):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="startCanaryAfterCreation")
    def start_canary_after_creation(self) -> pulumi.Input[bool]:
        """
        Runs canary if set to True. Default is False
        """
        return pulumi.get(self, "start_canary_after_creation")

    @start_canary_after_creation.setter
    def start_canary_after_creation(self, value: pulumi.Input[bool]):
        pulumi.set(self, "start_canary_after_creation", value)

    @property
    @pulumi.getter(name="artifactConfig")
    def artifact_config(self) -> Optional[pulumi.Input['CanaryArtifactConfigArgs']]:
        """
        Provide artifact configuration
        """
        return pulumi.get(self, "artifact_config")

    @artifact_config.setter
    def artifact_config(self, value: Optional[pulumi.Input['CanaryArtifactConfigArgs']]):
        pulumi.set(self, "artifact_config", value)

    @property
    @pulumi.getter(name="deleteLambdaResourcesOnCanaryDeletion")
    def delete_lambda_resources_on_canary_deletion(self) -> Optional[pulumi.Input[bool]]:
        """
        Deletes associated lambda resources created by Synthetics if set to True. Default is False
        """
        return pulumi.get(self, "delete_lambda_resources_on_canary_deletion")

    @delete_lambda_resources_on_canary_deletion.setter
    def delete_lambda_resources_on_canary_deletion(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_lambda_resources_on_canary_deletion", value)

    @property
    @pulumi.getter(name="failureRetentionPeriod")
    def failure_retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        Retention period of failed canary runs represented in number of days
        """
        return pulumi.get(self, "failure_retention_period")

    @failure_retention_period.setter
    def failure_retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_retention_period", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the canary.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="runConfig")
    def run_config(self) -> Optional[pulumi.Input['CanaryRunConfigArgs']]:
        """
        Provide canary run configuration
        """
        return pulumi.get(self, "run_config")

    @run_config.setter
    def run_config(self, value: Optional[pulumi.Input['CanaryRunConfigArgs']]):
        pulumi.set(self, "run_config", value)

    @property
    @pulumi.getter(name="successRetentionPeriod")
    def success_retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        Retention period of successful canary runs represented in number of days
        """
        return pulumi.get(self, "success_retention_period")

    @success_retention_period.setter
    def success_retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "success_retention_period", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CanaryTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CanaryTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vPCConfig")
    def v_pc_config(self) -> Optional[pulumi.Input['CanaryVPCConfigArgs']]:
        """
        Provide VPC Configuration if enabled.
        """
        return pulumi.get(self, "v_pc_config")

    @v_pc_config.setter
    def v_pc_config(self, value: Optional[pulumi.Input['CanaryVPCConfigArgs']]):
        pulumi.set(self, "v_pc_config", value)

    @property
    @pulumi.getter(name="visualReference")
    def visual_reference(self) -> Optional[pulumi.Input['CanaryVisualReferenceArgs']]:
        """
        Visual reference configuration for visual testing
        """
        return pulumi.get(self, "visual_reference")

    @visual_reference.setter
    def visual_reference(self, value: Optional[pulumi.Input['CanaryVisualReferenceArgs']]):
        pulumi.set(self, "visual_reference", value)


class Canary(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_config: Optional[pulumi.Input[pulumi.InputType['CanaryArtifactConfigArgs']]] = None,
                 artifact_s3_location: Optional[pulumi.Input[str]] = None,
                 code: Optional[pulumi.Input[pulumi.InputType['CanaryCodeArgs']]] = None,
                 delete_lambda_resources_on_canary_deletion: Optional[pulumi.Input[bool]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 failure_retention_period: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 run_config: Optional[pulumi.Input[pulumi.InputType['CanaryRunConfigArgs']]] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['CanaryScheduleArgs']]] = None,
                 start_canary_after_creation: Optional[pulumi.Input[bool]] = None,
                 success_retention_period: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CanaryTagArgs']]]]] = None,
                 v_pc_config: Optional[pulumi.Input[pulumi.InputType['CanaryVPCConfigArgs']]] = None,
                 visual_reference: Optional[pulumi.Input[pulumi.InputType['CanaryVisualReferenceArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Synthetics::Canary

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CanaryArtifactConfigArgs']] artifact_config: Provide artifact configuration
        :param pulumi.Input[str] artifact_s3_location: Provide the s3 bucket output location for test results
        :param pulumi.Input[pulumi.InputType['CanaryCodeArgs']] code: Provide the canary script source
        :param pulumi.Input[bool] delete_lambda_resources_on_canary_deletion: Deletes associated lambda resources created by Synthetics if set to True. Default is False
        :param pulumi.Input[str] execution_role_arn: Lambda Execution role used to run your canaries
        :param pulumi.Input[int] failure_retention_period: Retention period of failed canary runs represented in number of days
        :param pulumi.Input[str] name: Name of the canary.
        :param pulumi.Input[pulumi.InputType['CanaryRunConfigArgs']] run_config: Provide canary run configuration
        :param pulumi.Input[str] runtime_version: Runtime version of Synthetics Library
        :param pulumi.Input[pulumi.InputType['CanaryScheduleArgs']] schedule: Frequency to run your canaries
        :param pulumi.Input[bool] start_canary_after_creation: Runs canary if set to True. Default is False
        :param pulumi.Input[int] success_retention_period: Retention period of successful canary runs represented in number of days
        :param pulumi.Input[pulumi.InputType['CanaryVPCConfigArgs']] v_pc_config: Provide VPC Configuration if enabled.
        :param pulumi.Input[pulumi.InputType['CanaryVisualReferenceArgs']] visual_reference: Visual reference configuration for visual testing
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CanaryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Synthetics::Canary

        :param str resource_name: The name of the resource.
        :param CanaryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CanaryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_config: Optional[pulumi.Input[pulumi.InputType['CanaryArtifactConfigArgs']]] = None,
                 artifact_s3_location: Optional[pulumi.Input[str]] = None,
                 code: Optional[pulumi.Input[pulumi.InputType['CanaryCodeArgs']]] = None,
                 delete_lambda_resources_on_canary_deletion: Optional[pulumi.Input[bool]] = None,
                 execution_role_arn: Optional[pulumi.Input[str]] = None,
                 failure_retention_period: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 run_config: Optional[pulumi.Input[pulumi.InputType['CanaryRunConfigArgs']]] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['CanaryScheduleArgs']]] = None,
                 start_canary_after_creation: Optional[pulumi.Input[bool]] = None,
                 success_retention_period: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CanaryTagArgs']]]]] = None,
                 v_pc_config: Optional[pulumi.Input[pulumi.InputType['CanaryVPCConfigArgs']]] = None,
                 visual_reference: Optional[pulumi.Input[pulumi.InputType['CanaryVisualReferenceArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CanaryArgs.__new__(CanaryArgs)

            __props__.__dict__["artifact_config"] = artifact_config
            if artifact_s3_location is None and not opts.urn:
                raise TypeError("Missing required property 'artifact_s3_location'")
            __props__.__dict__["artifact_s3_location"] = artifact_s3_location
            if code is None and not opts.urn:
                raise TypeError("Missing required property 'code'")
            __props__.__dict__["code"] = code
            __props__.__dict__["delete_lambda_resources_on_canary_deletion"] = delete_lambda_resources_on_canary_deletion
            if execution_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'execution_role_arn'")
            __props__.__dict__["execution_role_arn"] = execution_role_arn
            __props__.__dict__["failure_retention_period"] = failure_retention_period
            __props__.__dict__["name"] = name
            __props__.__dict__["run_config"] = run_config
            if runtime_version is None and not opts.urn:
                raise TypeError("Missing required property 'runtime_version'")
            __props__.__dict__["runtime_version"] = runtime_version
            if schedule is None and not opts.urn:
                raise TypeError("Missing required property 'schedule'")
            __props__.__dict__["schedule"] = schedule
            if start_canary_after_creation is None and not opts.urn:
                raise TypeError("Missing required property 'start_canary_after_creation'")
            __props__.__dict__["start_canary_after_creation"] = start_canary_after_creation
            __props__.__dict__["success_retention_period"] = success_retention_period
            __props__.__dict__["tags"] = tags
            __props__.__dict__["v_pc_config"] = v_pc_config
            __props__.__dict__["visual_reference"] = visual_reference
            __props__.__dict__["state"] = None
        super(Canary, __self__).__init__(
            'aws-native:synthetics:Canary',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Canary':
        """
        Get an existing Canary resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CanaryArgs.__new__(CanaryArgs)

        __props__.__dict__["artifact_config"] = None
        __props__.__dict__["artifact_s3_location"] = None
        __props__.__dict__["code"] = None
        __props__.__dict__["delete_lambda_resources_on_canary_deletion"] = None
        __props__.__dict__["execution_role_arn"] = None
        __props__.__dict__["failure_retention_period"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["run_config"] = None
        __props__.__dict__["runtime_version"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["start_canary_after_creation"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["success_retention_period"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["v_pc_config"] = None
        __props__.__dict__["visual_reference"] = None
        return Canary(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="artifactConfig")
    def artifact_config(self) -> pulumi.Output[Optional['outputs.CanaryArtifactConfig']]:
        """
        Provide artifact configuration
        """
        return pulumi.get(self, "artifact_config")

    @property
    @pulumi.getter(name="artifactS3Location")
    def artifact_s3_location(self) -> pulumi.Output[str]:
        """
        Provide the s3 bucket output location for test results
        """
        return pulumi.get(self, "artifact_s3_location")

    @property
    @pulumi.getter
    def code(self) -> pulumi.Output['outputs.CanaryCode']:
        """
        Provide the canary script source
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="deleteLambdaResourcesOnCanaryDeletion")
    def delete_lambda_resources_on_canary_deletion(self) -> pulumi.Output[Optional[bool]]:
        """
        Deletes associated lambda resources created by Synthetics if set to True. Default is False
        """
        return pulumi.get(self, "delete_lambda_resources_on_canary_deletion")

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> pulumi.Output[str]:
        """
        Lambda Execution role used to run your canaries
        """
        return pulumi.get(self, "execution_role_arn")

    @property
    @pulumi.getter(name="failureRetentionPeriod")
    def failure_retention_period(self) -> pulumi.Output[Optional[int]]:
        """
        Retention period of failed canary runs represented in number of days
        """
        return pulumi.get(self, "failure_retention_period")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the canary.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="runConfig")
    def run_config(self) -> pulumi.Output[Optional['outputs.CanaryRunConfig']]:
        """
        Provide canary run configuration
        """
        return pulumi.get(self, "run_config")

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> pulumi.Output[str]:
        """
        Runtime version of Synthetics Library
        """
        return pulumi.get(self, "runtime_version")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output['outputs.CanarySchedule']:
        """
        Frequency to run your canaries
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="startCanaryAfterCreation")
    def start_canary_after_creation(self) -> pulumi.Output[bool]:
        """
        Runs canary if set to True. Default is False
        """
        return pulumi.get(self, "start_canary_after_creation")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the canary
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="successRetentionPeriod")
    def success_retention_period(self) -> pulumi.Output[Optional[int]]:
        """
        Retention period of successful canary runs represented in number of days
        """
        return pulumi.get(self, "success_retention_period")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.CanaryTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vPCConfig")
    def v_pc_config(self) -> pulumi.Output[Optional['outputs.CanaryVPCConfig']]:
        """
        Provide VPC Configuration if enabled.
        """
        return pulumi.get(self, "v_pc_config")

    @property
    @pulumi.getter(name="visualReference")
    def visual_reference(self) -> pulumi.Output[Optional['outputs.CanaryVisualReference']]:
        """
        Visual reference configuration for visual testing
        """
        return pulumi.get(self, "visual_reference")

