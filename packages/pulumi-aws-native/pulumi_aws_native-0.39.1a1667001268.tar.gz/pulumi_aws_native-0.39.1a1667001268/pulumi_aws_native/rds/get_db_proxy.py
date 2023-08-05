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

__all__ = [
    'GetDBProxyResult',
    'AwaitableGetDBProxyResult',
    'get_db_proxy',
    'get_db_proxy_output',
]

@pulumi.output_type
class GetDBProxyResult:
    def __init__(__self__, auth=None, d_b_proxy_arn=None, debug_logging=None, endpoint=None, idle_client_timeout=None, require_tls=None, role_arn=None, tags=None, vpc_id=None, vpc_security_group_ids=None):
        if auth and not isinstance(auth, list):
            raise TypeError("Expected argument 'auth' to be a list")
        pulumi.set(__self__, "auth", auth)
        if d_b_proxy_arn and not isinstance(d_b_proxy_arn, str):
            raise TypeError("Expected argument 'd_b_proxy_arn' to be a str")
        pulumi.set(__self__, "d_b_proxy_arn", d_b_proxy_arn)
        if debug_logging and not isinstance(debug_logging, bool):
            raise TypeError("Expected argument 'debug_logging' to be a bool")
        pulumi.set(__self__, "debug_logging", debug_logging)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if idle_client_timeout and not isinstance(idle_client_timeout, int):
            raise TypeError("Expected argument 'idle_client_timeout' to be a int")
        pulumi.set(__self__, "idle_client_timeout", idle_client_timeout)
        if require_tls and not isinstance(require_tls, bool):
            raise TypeError("Expected argument 'require_tls' to be a bool")
        pulumi.set(__self__, "require_tls", require_tls)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter
    def auth(self) -> Optional[Sequence['outputs.DBProxyAuthFormat']]:
        """
        The authorization mechanism that the proxy uses.
        """
        return pulumi.get(self, "auth")

    @property
    @pulumi.getter(name="dBProxyArn")
    def d_b_proxy_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the proxy.
        """
        return pulumi.get(self, "d_b_proxy_arn")

    @property
    @pulumi.getter(name="debugLogging")
    def debug_logging(self) -> Optional[bool]:
        """
        Whether the proxy includes detailed information about SQL statements in its logs.
        """
        return pulumi.get(self, "debug_logging")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        The endpoint that you can use to connect to the proxy. You include the endpoint value in the connection string for a database client application.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="idleClientTimeout")
    def idle_client_timeout(self) -> Optional[int]:
        """
        The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it.
        """
        return pulumi.get(self, "idle_client_timeout")

    @property
    @pulumi.getter(name="requireTLS")
    def require_tls(self) -> Optional[bool]:
        """
        A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy.
        """
        return pulumi.get(self, "require_tls")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access secrets in AWS Secrets Manager.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.DBProxyTagFormat']]:
        """
        An optional set of key-value pairs to associate arbitrary data of your choosing with the proxy.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        VPC ID to associate with the new DB proxy.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Optional[Sequence[str]]:
        """
        VPC security group IDs to associate with the new proxy.
        """
        return pulumi.get(self, "vpc_security_group_ids")


class AwaitableGetDBProxyResult(GetDBProxyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDBProxyResult(
            auth=self.auth,
            d_b_proxy_arn=self.d_b_proxy_arn,
            debug_logging=self.debug_logging,
            endpoint=self.endpoint,
            idle_client_timeout=self.idle_client_timeout,
            require_tls=self.require_tls,
            role_arn=self.role_arn,
            tags=self.tags,
            vpc_id=self.vpc_id,
            vpc_security_group_ids=self.vpc_security_group_ids)


def get_db_proxy(d_b_proxy_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDBProxyResult:
    """
    Resource schema for AWS::RDS::DBProxy


    :param str d_b_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region.
    """
    __args__ = dict()
    __args__['dBProxyName'] = d_b_proxy_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rds:getDBProxy', __args__, opts=opts, typ=GetDBProxyResult).value

    return AwaitableGetDBProxyResult(
        auth=__ret__.auth,
        d_b_proxy_arn=__ret__.d_b_proxy_arn,
        debug_logging=__ret__.debug_logging,
        endpoint=__ret__.endpoint,
        idle_client_timeout=__ret__.idle_client_timeout,
        require_tls=__ret__.require_tls,
        role_arn=__ret__.role_arn,
        tags=__ret__.tags,
        vpc_id=__ret__.vpc_id,
        vpc_security_group_ids=__ret__.vpc_security_group_ids)


@_utilities.lift_output_func(get_db_proxy)
def get_db_proxy_output(d_b_proxy_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDBProxyResult]:
    """
    Resource schema for AWS::RDS::DBProxy


    :param str d_b_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region.
    """
    ...
