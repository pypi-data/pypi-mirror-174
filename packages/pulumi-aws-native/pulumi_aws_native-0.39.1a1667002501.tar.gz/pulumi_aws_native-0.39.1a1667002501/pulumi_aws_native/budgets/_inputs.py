# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'BudgetAutoAdjustDataArgs',
    'BudgetCostTypesArgs',
    'BudgetDataArgs',
    'BudgetHistoricalOptionsArgs',
    'BudgetNotificationWithSubscribersArgs',
    'BudgetNotificationArgs',
    'BudgetSpendArgs',
    'BudgetSubscriberArgs',
    'BudgetTimePeriodArgs',
    'BudgetsActionActionThresholdArgs',
    'BudgetsActionDefinitionArgs',
    'BudgetsActionIamActionDefinitionArgs',
    'BudgetsActionScpActionDefinitionArgs',
    'BudgetsActionSsmActionDefinitionArgs',
    'BudgetsActionSubscriberArgs',
]

@pulumi.input_type
class BudgetAutoAdjustDataArgs:
    def __init__(__self__, *,
                 auto_adjust_type: pulumi.Input[str],
                 historical_options: Optional[pulumi.Input['BudgetHistoricalOptionsArgs']] = None):
        pulumi.set(__self__, "auto_adjust_type", auto_adjust_type)
        if historical_options is not None:
            pulumi.set(__self__, "historical_options", historical_options)

    @property
    @pulumi.getter(name="autoAdjustType")
    def auto_adjust_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "auto_adjust_type")

    @auto_adjust_type.setter
    def auto_adjust_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "auto_adjust_type", value)

    @property
    @pulumi.getter(name="historicalOptions")
    def historical_options(self) -> Optional[pulumi.Input['BudgetHistoricalOptionsArgs']]:
        return pulumi.get(self, "historical_options")

    @historical_options.setter
    def historical_options(self, value: Optional[pulumi.Input['BudgetHistoricalOptionsArgs']]):
        pulumi.set(self, "historical_options", value)


@pulumi.input_type
class BudgetCostTypesArgs:
    def __init__(__self__, *,
                 include_credit: Optional[pulumi.Input[bool]] = None,
                 include_discount: Optional[pulumi.Input[bool]] = None,
                 include_other_subscription: Optional[pulumi.Input[bool]] = None,
                 include_recurring: Optional[pulumi.Input[bool]] = None,
                 include_refund: Optional[pulumi.Input[bool]] = None,
                 include_subscription: Optional[pulumi.Input[bool]] = None,
                 include_support: Optional[pulumi.Input[bool]] = None,
                 include_tax: Optional[pulumi.Input[bool]] = None,
                 include_upfront: Optional[pulumi.Input[bool]] = None,
                 use_amortized: Optional[pulumi.Input[bool]] = None,
                 use_blended: Optional[pulumi.Input[bool]] = None):
        if include_credit is not None:
            pulumi.set(__self__, "include_credit", include_credit)
        if include_discount is not None:
            pulumi.set(__self__, "include_discount", include_discount)
        if include_other_subscription is not None:
            pulumi.set(__self__, "include_other_subscription", include_other_subscription)
        if include_recurring is not None:
            pulumi.set(__self__, "include_recurring", include_recurring)
        if include_refund is not None:
            pulumi.set(__self__, "include_refund", include_refund)
        if include_subscription is not None:
            pulumi.set(__self__, "include_subscription", include_subscription)
        if include_support is not None:
            pulumi.set(__self__, "include_support", include_support)
        if include_tax is not None:
            pulumi.set(__self__, "include_tax", include_tax)
        if include_upfront is not None:
            pulumi.set(__self__, "include_upfront", include_upfront)
        if use_amortized is not None:
            pulumi.set(__self__, "use_amortized", use_amortized)
        if use_blended is not None:
            pulumi.set(__self__, "use_blended", use_blended)

    @property
    @pulumi.getter(name="includeCredit")
    def include_credit(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_credit")

    @include_credit.setter
    def include_credit(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_credit", value)

    @property
    @pulumi.getter(name="includeDiscount")
    def include_discount(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_discount")

    @include_discount.setter
    def include_discount(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_discount", value)

    @property
    @pulumi.getter(name="includeOtherSubscription")
    def include_other_subscription(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_other_subscription")

    @include_other_subscription.setter
    def include_other_subscription(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_other_subscription", value)

    @property
    @pulumi.getter(name="includeRecurring")
    def include_recurring(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_recurring")

    @include_recurring.setter
    def include_recurring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_recurring", value)

    @property
    @pulumi.getter(name="includeRefund")
    def include_refund(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_refund")

    @include_refund.setter
    def include_refund(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_refund", value)

    @property
    @pulumi.getter(name="includeSubscription")
    def include_subscription(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_subscription")

    @include_subscription.setter
    def include_subscription(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_subscription", value)

    @property
    @pulumi.getter(name="includeSupport")
    def include_support(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_support")

    @include_support.setter
    def include_support(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_support", value)

    @property
    @pulumi.getter(name="includeTax")
    def include_tax(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_tax")

    @include_tax.setter
    def include_tax(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_tax", value)

    @property
    @pulumi.getter(name="includeUpfront")
    def include_upfront(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "include_upfront")

    @include_upfront.setter
    def include_upfront(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_upfront", value)

    @property
    @pulumi.getter(name="useAmortized")
    def use_amortized(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "use_amortized")

    @use_amortized.setter
    def use_amortized(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_amortized", value)

    @property
    @pulumi.getter(name="useBlended")
    def use_blended(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "use_blended")

    @use_blended.setter
    def use_blended(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_blended", value)


@pulumi.input_type
class BudgetDataArgs:
    def __init__(__self__, *,
                 budget_type: pulumi.Input[str],
                 time_unit: pulumi.Input[str],
                 auto_adjust_data: Optional[pulumi.Input['BudgetAutoAdjustDataArgs']] = None,
                 budget_limit: Optional[pulumi.Input['BudgetSpendArgs']] = None,
                 budget_name: Optional[pulumi.Input[str]] = None,
                 cost_filters: Optional[Any] = None,
                 cost_types: Optional[pulumi.Input['BudgetCostTypesArgs']] = None,
                 planned_budget_limits: Optional[Any] = None,
                 time_period: Optional[pulumi.Input['BudgetTimePeriodArgs']] = None):
        pulumi.set(__self__, "budget_type", budget_type)
        pulumi.set(__self__, "time_unit", time_unit)
        if auto_adjust_data is not None:
            pulumi.set(__self__, "auto_adjust_data", auto_adjust_data)
        if budget_limit is not None:
            pulumi.set(__self__, "budget_limit", budget_limit)
        if budget_name is not None:
            pulumi.set(__self__, "budget_name", budget_name)
        if cost_filters is not None:
            pulumi.set(__self__, "cost_filters", cost_filters)
        if cost_types is not None:
            pulumi.set(__self__, "cost_types", cost_types)
        if planned_budget_limits is not None:
            pulumi.set(__self__, "planned_budget_limits", planned_budget_limits)
        if time_period is not None:
            pulumi.set(__self__, "time_period", time_period)

    @property
    @pulumi.getter(name="budgetType")
    def budget_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "budget_type")

    @budget_type.setter
    def budget_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "budget_type", value)

    @property
    @pulumi.getter(name="timeUnit")
    def time_unit(self) -> pulumi.Input[str]:
        return pulumi.get(self, "time_unit")

    @time_unit.setter
    def time_unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "time_unit", value)

    @property
    @pulumi.getter(name="autoAdjustData")
    def auto_adjust_data(self) -> Optional[pulumi.Input['BudgetAutoAdjustDataArgs']]:
        return pulumi.get(self, "auto_adjust_data")

    @auto_adjust_data.setter
    def auto_adjust_data(self, value: Optional[pulumi.Input['BudgetAutoAdjustDataArgs']]):
        pulumi.set(self, "auto_adjust_data", value)

    @property
    @pulumi.getter(name="budgetLimit")
    def budget_limit(self) -> Optional[pulumi.Input['BudgetSpendArgs']]:
        return pulumi.get(self, "budget_limit")

    @budget_limit.setter
    def budget_limit(self, value: Optional[pulumi.Input['BudgetSpendArgs']]):
        pulumi.set(self, "budget_limit", value)

    @property
    @pulumi.getter(name="budgetName")
    def budget_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "budget_name")

    @budget_name.setter
    def budget_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "budget_name", value)

    @property
    @pulumi.getter(name="costFilters")
    def cost_filters(self) -> Optional[Any]:
        return pulumi.get(self, "cost_filters")

    @cost_filters.setter
    def cost_filters(self, value: Optional[Any]):
        pulumi.set(self, "cost_filters", value)

    @property
    @pulumi.getter(name="costTypes")
    def cost_types(self) -> Optional[pulumi.Input['BudgetCostTypesArgs']]:
        return pulumi.get(self, "cost_types")

    @cost_types.setter
    def cost_types(self, value: Optional[pulumi.Input['BudgetCostTypesArgs']]):
        pulumi.set(self, "cost_types", value)

    @property
    @pulumi.getter(name="plannedBudgetLimits")
    def planned_budget_limits(self) -> Optional[Any]:
        return pulumi.get(self, "planned_budget_limits")

    @planned_budget_limits.setter
    def planned_budget_limits(self, value: Optional[Any]):
        pulumi.set(self, "planned_budget_limits", value)

    @property
    @pulumi.getter(name="timePeriod")
    def time_period(self) -> Optional[pulumi.Input['BudgetTimePeriodArgs']]:
        return pulumi.get(self, "time_period")

    @time_period.setter
    def time_period(self, value: Optional[pulumi.Input['BudgetTimePeriodArgs']]):
        pulumi.set(self, "time_period", value)


@pulumi.input_type
class BudgetHistoricalOptionsArgs:
    def __init__(__self__, *,
                 budget_adjustment_period: pulumi.Input[int]):
        pulumi.set(__self__, "budget_adjustment_period", budget_adjustment_period)

    @property
    @pulumi.getter(name="budgetAdjustmentPeriod")
    def budget_adjustment_period(self) -> pulumi.Input[int]:
        return pulumi.get(self, "budget_adjustment_period")

    @budget_adjustment_period.setter
    def budget_adjustment_period(self, value: pulumi.Input[int]):
        pulumi.set(self, "budget_adjustment_period", value)


@pulumi.input_type
class BudgetNotificationWithSubscribersArgs:
    def __init__(__self__, *,
                 notification: pulumi.Input['BudgetNotificationArgs'],
                 subscribers: pulumi.Input[Sequence[pulumi.Input['BudgetSubscriberArgs']]]):
        pulumi.set(__self__, "notification", notification)
        pulumi.set(__self__, "subscribers", subscribers)

    @property
    @pulumi.getter
    def notification(self) -> pulumi.Input['BudgetNotificationArgs']:
        return pulumi.get(self, "notification")

    @notification.setter
    def notification(self, value: pulumi.Input['BudgetNotificationArgs']):
        pulumi.set(self, "notification", value)

    @property
    @pulumi.getter
    def subscribers(self) -> pulumi.Input[Sequence[pulumi.Input['BudgetSubscriberArgs']]]:
        return pulumi.get(self, "subscribers")

    @subscribers.setter
    def subscribers(self, value: pulumi.Input[Sequence[pulumi.Input['BudgetSubscriberArgs']]]):
        pulumi.set(self, "subscribers", value)


@pulumi.input_type
class BudgetNotificationArgs:
    def __init__(__self__, *,
                 comparison_operator: pulumi.Input[str],
                 notification_type: pulumi.Input[str],
                 threshold: pulumi.Input[float],
                 threshold_type: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "comparison_operator", comparison_operator)
        pulumi.set(__self__, "notification_type", notification_type)
        pulumi.set(__self__, "threshold", threshold)
        if threshold_type is not None:
            pulumi.set(__self__, "threshold_type", threshold_type)

    @property
    @pulumi.getter(name="comparisonOperator")
    def comparison_operator(self) -> pulumi.Input[str]:
        return pulumi.get(self, "comparison_operator")

    @comparison_operator.setter
    def comparison_operator(self, value: pulumi.Input[str]):
        pulumi.set(self, "comparison_operator", value)

    @property
    @pulumi.getter(name="notificationType")
    def notification_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "notification_type")

    @notification_type.setter
    def notification_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "notification_type", value)

    @property
    @pulumi.getter
    def threshold(self) -> pulumi.Input[float]:
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: pulumi.Input[float]):
        pulumi.set(self, "threshold", value)

    @property
    @pulumi.getter(name="thresholdType")
    def threshold_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "threshold_type")

    @threshold_type.setter
    def threshold_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "threshold_type", value)


@pulumi.input_type
class BudgetSpendArgs:
    def __init__(__self__, *,
                 amount: pulumi.Input[float],
                 unit: pulumi.Input[str]):
        pulumi.set(__self__, "amount", amount)
        pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def amount(self) -> pulumi.Input[float]:
        return pulumi.get(self, "amount")

    @amount.setter
    def amount(self, value: pulumi.Input[float]):
        pulumi.set(self, "amount", value)

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Input[str]:
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "unit", value)


@pulumi.input_type
class BudgetSubscriberArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 subscription_type: pulumi.Input[str]):
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "subscription_type", subscription_type)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="subscriptionType")
    def subscription_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "subscription_type")

    @subscription_type.setter
    def subscription_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "subscription_type", value)


@pulumi.input_type
class BudgetTimePeriodArgs:
    def __init__(__self__, *,
                 end: Optional[pulumi.Input[str]] = None,
                 start: Optional[pulumi.Input[str]] = None):
        if end is not None:
            pulumi.set(__self__, "end", end)
        if start is not None:
            pulumi.set(__self__, "start", start)

    @property
    @pulumi.getter
    def end(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "end")

    @end.setter
    def end(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end", value)

    @property
    @pulumi.getter
    def start(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "start")

    @start.setter
    def start(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start", value)


@pulumi.input_type
class BudgetsActionActionThresholdArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['BudgetsActionActionThresholdType'],
                 value: pulumi.Input[float]):
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['BudgetsActionActionThresholdType']:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['BudgetsActionActionThresholdType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[float]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[float]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class BudgetsActionDefinitionArgs:
    def __init__(__self__, *,
                 iam_action_definition: Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']] = None,
                 scp_action_definition: Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']] = None,
                 ssm_action_definition: Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']] = None):
        if iam_action_definition is not None:
            pulumi.set(__self__, "iam_action_definition", iam_action_definition)
        if scp_action_definition is not None:
            pulumi.set(__self__, "scp_action_definition", scp_action_definition)
        if ssm_action_definition is not None:
            pulumi.set(__self__, "ssm_action_definition", ssm_action_definition)

    @property
    @pulumi.getter(name="iamActionDefinition")
    def iam_action_definition(self) -> Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']]:
        return pulumi.get(self, "iam_action_definition")

    @iam_action_definition.setter
    def iam_action_definition(self, value: Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']]):
        pulumi.set(self, "iam_action_definition", value)

    @property
    @pulumi.getter(name="scpActionDefinition")
    def scp_action_definition(self) -> Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']]:
        return pulumi.get(self, "scp_action_definition")

    @scp_action_definition.setter
    def scp_action_definition(self, value: Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']]):
        pulumi.set(self, "scp_action_definition", value)

    @property
    @pulumi.getter(name="ssmActionDefinition")
    def ssm_action_definition(self) -> Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']]:
        return pulumi.get(self, "ssm_action_definition")

    @ssm_action_definition.setter
    def ssm_action_definition(self, value: Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']]):
        pulumi.set(self, "ssm_action_definition", value)


@pulumi.input_type
class BudgetsActionIamActionDefinitionArgs:
    def __init__(__self__, *,
                 policy_arn: pulumi.Input[str],
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        pulumi.set(__self__, "policy_arn", policy_arn)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "roles", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users", value)


@pulumi.input_type
class BudgetsActionScpActionDefinitionArgs:
    def __init__(__self__, *,
                 policy_id: pulumi.Input[str],
                 target_ids: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(__self__, "policy_id", policy_id)
        pulumi.set(__self__, "target_ids", target_ids)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter(name="targetIds")
    def target_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "target_ids")

    @target_ids.setter
    def target_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "target_ids", value)


@pulumi.input_type
class BudgetsActionSsmActionDefinitionArgs:
    def __init__(__self__, *,
                 instance_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 region: pulumi.Input[str],
                 subtype: pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']):
        pulumi.set(__self__, "instance_ids", instance_ids)
        pulumi.set(__self__, "region", region)
        pulumi.set(__self__, "subtype", subtype)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def subtype(self) -> pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']:
        return pulumi.get(self, "subtype")

    @subtype.setter
    def subtype(self, value: pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']):
        pulumi.set(self, "subtype", value)


@pulumi.input_type
class BudgetsActionSubscriberArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 type: pulumi.Input['BudgetsActionSubscriberType']):
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['BudgetsActionSubscriberType']:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['BudgetsActionSubscriberType']):
        pulumi.set(self, "type", value)


