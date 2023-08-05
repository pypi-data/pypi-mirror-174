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
    'GetGraphQLSchemaResult',
    'AwaitableGetGraphQLSchemaResult',
    'get_graph_ql_schema',
    'get_graph_ql_schema_output',
]

@pulumi.output_type
class GetGraphQLSchemaResult:
    def __init__(__self__, definition=None, definition_s3_location=None, id=None):
        if definition and not isinstance(definition, str):
            raise TypeError("Expected argument 'definition' to be a str")
        pulumi.set(__self__, "definition", definition)
        if definition_s3_location and not isinstance(definition_s3_location, str):
            raise TypeError("Expected argument 'definition_s3_location' to be a str")
        pulumi.set(__self__, "definition_s3_location", definition_s3_location)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def definition(self) -> Optional[str]:
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="definitionS3Location")
    def definition_s3_location(self) -> Optional[str]:
        return pulumi.get(self, "definition_s3_location")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")


class AwaitableGetGraphQLSchemaResult(GetGraphQLSchemaResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGraphQLSchemaResult(
            definition=self.definition,
            definition_s3_location=self.definition_s3_location,
            id=self.id)


def get_graph_ql_schema(id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGraphQLSchemaResult:
    """
    Resource Type definition for AWS::AppSync::GraphQLSchema
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appsync:getGraphQLSchema', __args__, opts=opts, typ=GetGraphQLSchemaResult).value

    return AwaitableGetGraphQLSchemaResult(
        definition=__ret__.definition,
        definition_s3_location=__ret__.definition_s3_location,
        id=__ret__.id)


@_utilities.lift_output_func(get_graph_ql_schema)
def get_graph_ql_schema_output(id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGraphQLSchemaResult]:
    """
    Resource Type definition for AWS::AppSync::GraphQLSchema
    """
    ...
