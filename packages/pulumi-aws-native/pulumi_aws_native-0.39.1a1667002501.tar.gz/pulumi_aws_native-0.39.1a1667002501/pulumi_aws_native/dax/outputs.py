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
    'ClusterSSESpecification',
]

@pulumi.output_type
class ClusterSSESpecification(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sSEEnabled":
            suggest = "s_se_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterSSESpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterSSESpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterSSESpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s_se_enabled: Optional[bool] = None):
        if s_se_enabled is not None:
            pulumi.set(__self__, "s_se_enabled", s_se_enabled)

    @property
    @pulumi.getter(name="sSEEnabled")
    def s_se_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "s_se_enabled")


