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
    'ComponentTypeStatus',
    'ComponentTypeStatusErrorProperties',
    'EntityStatus',
    'EntityStatusErrorProperties',
]

@pulumi.output_type
class ComponentTypeStatus(dict):
    def __init__(__self__, *,
                 error: Optional['outputs.ComponentTypeStatusErrorProperties'] = None,
                 state: Optional['ComponentTypeStatusState'] = None):
        if error is not None:
            pulumi.set(__self__, "error", error)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.ComponentTypeStatusErrorProperties']:
        return pulumi.get(self, "error")

    @property
    @pulumi.getter
    def state(self) -> Optional['ComponentTypeStatusState']:
        return pulumi.get(self, "state")


@pulumi.output_type
class ComponentTypeStatusErrorProperties(dict):
    def __init__(__self__, *,
                 code: Optional['ComponentTypeStatusErrorPropertiesCode'] = None,
                 message: Optional[str] = None):
        if code is not None:
            pulumi.set(__self__, "code", code)
        if message is not None:
            pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def code(self) -> Optional['ComponentTypeStatusErrorPropertiesCode']:
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        return pulumi.get(self, "message")


@pulumi.output_type
class EntityStatus(dict):
    def __init__(__self__, *,
                 error: Optional['outputs.EntityStatusErrorProperties'] = None,
                 state: Optional['EntityStatusState'] = None):
        if error is not None:
            pulumi.set(__self__, "error", error)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.EntityStatusErrorProperties']:
        return pulumi.get(self, "error")

    @property
    @pulumi.getter
    def state(self) -> Optional['EntityStatusState']:
        return pulumi.get(self, "state")


@pulumi.output_type
class EntityStatusErrorProperties(dict):
    def __init__(__self__, *,
                 code: Optional['EntityStatusErrorPropertiesCode'] = None,
                 message: Optional[str] = None):
        if code is not None:
            pulumi.set(__self__, "code", code)
        if message is not None:
            pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def code(self) -> Optional['EntityStatusErrorPropertiesCode']:
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        return pulumi.get(self, "message")


