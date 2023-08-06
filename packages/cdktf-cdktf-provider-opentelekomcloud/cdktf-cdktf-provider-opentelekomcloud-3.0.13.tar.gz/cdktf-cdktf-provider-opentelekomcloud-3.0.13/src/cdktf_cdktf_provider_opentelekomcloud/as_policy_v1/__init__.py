'''
# `opentelekomcloud_as_policy_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_as_policy_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class AsPolicyV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1 opentelekomcloud_as_policy_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        scaling_group_id: builtins.str,
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[str, typing.Any]]] = None,
        scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1 opentelekomcloud_as_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scaling_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#id AsPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#region AsPolicyV1#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                scaling_group_id: builtins.str,
                scaling_policy_name: builtins.str,
                scaling_policy_type: builtins.str,
                alarm_id: typing.Optional[builtins.str] = None,
                cool_down_time: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[str, typing.Any]]] = None,
                scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[str, typing.Any]]] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsPolicyV1Config(
            scaling_group_id=scaling_group_id,
            scaling_policy_name=scaling_policy_name,
            scaling_policy_type=scaling_policy_type,
            alarm_id=alarm_id,
            cool_down_time=cool_down_time,
            id=id,
            region=region,
            scaling_policy_action=scaling_policy_action,
            scheduled_policy=scheduled_policy,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putScalingPolicyAction")
    def put_scaling_policy_action(
        self,
        *,
        instance_number: typing.Optional[jsii.Number] = None,
        operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#instance_number AsPolicyV1#instance_number}.
        :param operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#operation AsPolicyV1#operation}.
        '''
        value = AsPolicyV1ScalingPolicyAction(
            instance_number=instance_number, operation=operation
        )

        return typing.cast(None, jsii.invoke(self, "putScalingPolicyAction", [value]))

    @jsii.member(jsii_name="putScheduledPolicy")
    def put_scheduled_policy(
        self,
        *,
        launch_time: builtins.str,
        end_time: typing.Optional[builtins.str] = None,
        recurrence_type: typing.Optional[builtins.str] = None,
        recurrence_value: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#launch_time AsPolicyV1#launch_time}.
        :param end_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#end_time AsPolicyV1#end_time}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.
        :param recurrence_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.
        :param start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#start_time AsPolicyV1#start_time}.
        '''
        value = AsPolicyV1ScheduledPolicy(
            launch_time=launch_time,
            end_time=end_time,
            recurrence_type=recurrence_type,
            recurrence_value=recurrence_value,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledPolicy", [value]))

    @jsii.member(jsii_name="resetAlarmId")
    def reset_alarm_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmId", []))

    @jsii.member(jsii_name="resetCoolDownTime")
    def reset_cool_down_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingPolicyAction")
    def reset_scaling_policy_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingPolicyAction", []))

    @jsii.member(jsii_name="resetScheduledPolicy")
    def reset_scheduled_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledPolicy", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyAction")
    def scaling_policy_action(self) -> "AsPolicyV1ScalingPolicyActionOutputReference":
        return typing.cast("AsPolicyV1ScalingPolicyActionOutputReference", jsii.get(self, "scalingPolicyAction"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicy")
    def scheduled_policy(self) -> "AsPolicyV1ScheduledPolicyOutputReference":
        return typing.cast("AsPolicyV1ScheduledPolicyOutputReference", jsii.get(self, "scheduledPolicy"))

    @builtins.property
    @jsii.member(jsii_name="alarmIdInput")
    def alarm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownTimeInput")
    def cool_down_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolDownTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupIdInput")
    def scaling_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyActionInput")
    def scaling_policy_action_input(
        self,
    ) -> typing.Optional["AsPolicyV1ScalingPolicyAction"]:
        return typing.cast(typing.Optional["AsPolicyV1ScalingPolicyAction"], jsii.get(self, "scalingPolicyActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyNameInput")
    def scaling_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyTypeInput")
    def scaling_policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicyInput")
    def scheduled_policy_input(self) -> typing.Optional["AsPolicyV1ScheduledPolicy"]:
        return typing.cast(typing.Optional["AsPolicyV1ScheduledPolicy"], jsii.get(self, "scheduledPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmId")
    def alarm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmId"))

    @alarm_id.setter
    def alarm_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmId", value)

    @builtins.property
    @jsii.member(jsii_name="coolDownTime")
    def cool_down_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolDownTime"))

    @cool_down_time.setter
    def cool_down_time(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownTime", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="scalingGroupId")
    def scaling_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupId"))

    @scaling_group_id.setter
    def scaling_group_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyName")
    def scaling_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyName"))

    @scaling_policy_name.setter
    def scaling_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyType")
    def scaling_policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyType"))

    @scaling_policy_type.setter
    def scaling_policy_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "scaling_group_id": "scalingGroupId",
        "scaling_policy_name": "scalingPolicyName",
        "scaling_policy_type": "scalingPolicyType",
        "alarm_id": "alarmId",
        "cool_down_time": "coolDownTime",
        "id": "id",
        "region": "region",
        "scaling_policy_action": "scalingPolicyAction",
        "scheduled_policy": "scheduledPolicy",
    },
)
class AsPolicyV1Config(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        scaling_group_id: builtins.str,
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[str, typing.Any]]] = None,
        scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scaling_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#id AsPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#region AsPolicyV1#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scaling_policy_action, dict):
            scaling_policy_action = AsPolicyV1ScalingPolicyAction(**scaling_policy_action)
        if isinstance(scheduled_policy, dict):
            scheduled_policy = AsPolicyV1ScheduledPolicy(**scheduled_policy)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                scaling_group_id: builtins.str,
                scaling_policy_name: builtins.str,
                scaling_policy_type: builtins.str,
                alarm_id: typing.Optional[builtins.str] = None,
                cool_down_time: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[str, typing.Any]]] = None,
                scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scaling_group_id", value=scaling_group_id, expected_type=type_hints["scaling_group_id"])
            check_type(argname="argument scaling_policy_name", value=scaling_policy_name, expected_type=type_hints["scaling_policy_name"])
            check_type(argname="argument scaling_policy_type", value=scaling_policy_type, expected_type=type_hints["scaling_policy_type"])
            check_type(argname="argument alarm_id", value=alarm_id, expected_type=type_hints["alarm_id"])
            check_type(argname="argument cool_down_time", value=cool_down_time, expected_type=type_hints["cool_down_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_policy_action", value=scaling_policy_action, expected_type=type_hints["scaling_policy_action"])
            check_type(argname="argument scheduled_policy", value=scheduled_policy, expected_type=type_hints["scheduled_policy"])
        self._values: typing.Dict[str, typing.Any] = {
            "scaling_group_id": scaling_group_id,
            "scaling_policy_name": scaling_policy_name,
            "scaling_policy_type": scaling_policy_type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if alarm_id is not None:
            self._values["alarm_id"] = alarm_id
        if cool_down_time is not None:
            self._values["cool_down_time"] = cool_down_time
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if scaling_policy_action is not None:
            self._values["scaling_policy_action"] = scaling_policy_action
        if scheduled_policy is not None:
            self._values["scheduled_policy"] = scheduled_policy

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def scaling_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.'''
        result = self._values.get("scaling_group_id")
        assert result is not None, "Required property 'scaling_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_policy_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.'''
        result = self._values.get("scaling_policy_name")
        assert result is not None, "Required property 'scaling_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_policy_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.'''
        result = self._values.get("scaling_policy_type")
        assert result is not None, "Required property 'scaling_policy_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.'''
        result = self._values.get("alarm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cool_down_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.'''
        result = self._values.get("cool_down_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#id AsPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#region AsPolicyV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_policy_action(self) -> typing.Optional["AsPolicyV1ScalingPolicyAction"]:
        '''scaling_policy_action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        '''
        result = self._values.get("scaling_policy_action")
        return typing.cast(typing.Optional["AsPolicyV1ScalingPolicyAction"], result)

    @builtins.property
    def scheduled_policy(self) -> typing.Optional["AsPolicyV1ScheduledPolicy"]:
        '''scheduled_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        '''
        result = self._values.get("scheduled_policy")
        return typing.cast(typing.Optional["AsPolicyV1ScheduledPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScalingPolicyAction",
    jsii_struct_bases=[],
    name_mapping={"instance_number": "instanceNumber", "operation": "operation"},
)
class AsPolicyV1ScalingPolicyAction:
    def __init__(
        self,
        *,
        instance_number: typing.Optional[jsii.Number] = None,
        operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#instance_number AsPolicyV1#instance_number}.
        :param operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#operation AsPolicyV1#operation}.
        '''
        if __debug__:
            def stub(
                *,
                instance_number: typing.Optional[jsii.Number] = None,
                operation: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument instance_number", value=instance_number, expected_type=type_hints["instance_number"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        self._values: typing.Dict[str, typing.Any] = {}
        if instance_number is not None:
            self._values["instance_number"] = instance_number
        if operation is not None:
            self._values["operation"] = operation

    @builtins.property
    def instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#instance_number AsPolicyV1#instance_number}.'''
        result = self._values.get("instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#operation AsPolicyV1#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1ScalingPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV1ScalingPolicyActionOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScalingPolicyActionOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceNumber")
    def reset_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceNumber", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @builtins.property
    @jsii.member(jsii_name="instanceNumberInput")
    def instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNumber")
    def instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceNumber"))

    @instance_number.setter
    def instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceNumber", value)

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsPolicyV1ScalingPolicyAction]:
        return typing.cast(typing.Optional[AsPolicyV1ScalingPolicyAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsPolicyV1ScalingPolicyAction],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[AsPolicyV1ScalingPolicyAction]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScheduledPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "launch_time": "launchTime",
        "end_time": "endTime",
        "recurrence_type": "recurrenceType",
        "recurrence_value": "recurrenceValue",
        "start_time": "startTime",
    },
)
class AsPolicyV1ScheduledPolicy:
    def __init__(
        self,
        *,
        launch_time: builtins.str,
        end_time: typing.Optional[builtins.str] = None,
        recurrence_type: typing.Optional[builtins.str] = None,
        recurrence_value: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#launch_time AsPolicyV1#launch_time}.
        :param end_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#end_time AsPolicyV1#end_time}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.
        :param recurrence_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.
        :param start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#start_time AsPolicyV1#start_time}.
        '''
        if __debug__:
            def stub(
                *,
                launch_time: builtins.str,
                end_time: typing.Optional[builtins.str] = None,
                recurrence_type: typing.Optional[builtins.str] = None,
                recurrence_value: typing.Optional[builtins.str] = None,
                start_time: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument launch_time", value=launch_time, expected_type=type_hints["launch_time"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument recurrence_type", value=recurrence_type, expected_type=type_hints["recurrence_type"])
            check_type(argname="argument recurrence_value", value=recurrence_value, expected_type=type_hints["recurrence_value"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {
            "launch_time": launch_time,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if recurrence_type is not None:
            self._values["recurrence_type"] = recurrence_type
        if recurrence_value is not None:
            self._values["recurrence_value"] = recurrence_value
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def launch_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#launch_time AsPolicyV1#launch_time}.'''
        result = self._values.get("launch_time")
        assert result is not None, "Required property 'launch_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#end_time AsPolicyV1#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.'''
        result = self._values.get("recurrence_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.'''
        result = self._values.get("recurrence_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_policy_v1#start_time AsPolicyV1#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1ScheduledPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV1ScheduledPolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScheduledPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetRecurrenceType")
    def reset_recurrence_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceType", []))

    @jsii.member(jsii_name="resetRecurrenceValue")
    def reset_recurrence_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceValue", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTimeInput")
    def launch_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceTypeInput")
    def recurrence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceValueInput")
    def recurrence_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceValueInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value)

    @builtins.property
    @jsii.member(jsii_name="launchTime")
    def launch_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTime"))

    @launch_time.setter
    def launch_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTime", value)

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value)

    @builtins.property
    @jsii.member(jsii_name="recurrenceValue")
    def recurrence_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceValue"))

    @recurrence_value.setter
    def recurrence_value(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceValue", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsPolicyV1ScheduledPolicy]:
        return typing.cast(typing.Optional[AsPolicyV1ScheduledPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AsPolicyV1ScheduledPolicy]) -> None:
        if __debug__:
            def stub(value: typing.Optional[AsPolicyV1ScheduledPolicy]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AsPolicyV1",
    "AsPolicyV1Config",
    "AsPolicyV1ScalingPolicyAction",
    "AsPolicyV1ScalingPolicyActionOutputReference",
    "AsPolicyV1ScheduledPolicy",
    "AsPolicyV1ScheduledPolicyOutputReference",
]

publication.publish()
