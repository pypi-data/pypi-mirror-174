'''
# `opentelekomcloud_as_group_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_as_group_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1).
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


class AsGroupV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1 opentelekomcloud_as_group_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        delete_instances: builtins.str,
        delete_publicip: typing.Union[builtins.bool, cdktf.IResolvable],
        networks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
        scaling_group_name: builtins.str,
        vpc_id: builtins.str,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        desire_instance_number: typing.Optional[jsii.Number] = None,
        health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
        health_periodic_audit_method: typing.Optional[builtins.str] = None,
        health_periodic_audit_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        instance_terminate_policy: typing.Optional[builtins.str] = None,
        lbaas_listeners: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]]] = None,
        lb_listener_id: typing.Optional[builtins.str] = None,
        max_instance_number: typing.Optional[jsii.Number] = None,
        min_instance_number: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_configuration_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1 opentelekomcloud_as_group_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param delete_instances: Whether to delete instances when they are removed from the AS group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_instances AsGroupV1#delete_instances}
        :param delete_publicip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.
        :param networks: networks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#networks AsGroupV1#networks}
        :param scaling_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#vpc_id AsGroupV1#vpc_id}.
        :param available_zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#available_zones AsGroupV1#available_zones}.
        :param cool_down_time: The cooling duration, in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        :param desire_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.
        :param health_periodic_audit_grace_period: The grace period for instance health check, in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        :param health_periodic_audit_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.
        :param health_periodic_audit_time: The health check period for instances, in minutes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_terminate_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.
        :param lbaas_listeners: lbaas_listeners block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        :param lb_listener_id: The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        :param max_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.
        :param min_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.
        :param notifications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#notifications AsGroupV1#notifications}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#region AsGroupV1#region}.
        :param scaling_configuration_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.
        :param security_groups: security_groups block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#security_groups AsGroupV1#security_groups}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#tags AsGroupV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#timeouts AsGroupV1#timeouts}
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
                delete_instances: builtins.str,
                delete_publicip: typing.Union[builtins.bool, cdktf.IResolvable],
                networks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
                scaling_group_name: builtins.str,
                vpc_id: builtins.str,
                available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
                cool_down_time: typing.Optional[jsii.Number] = None,
                desire_instance_number: typing.Optional[jsii.Number] = None,
                health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
                health_periodic_audit_method: typing.Optional[builtins.str] = None,
                health_periodic_audit_time: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                instance_terminate_policy: typing.Optional[builtins.str] = None,
                lbaas_listeners: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]]] = None,
                lb_listener_id: typing.Optional[builtins.str] = None,
                max_instance_number: typing.Optional[jsii.Number] = None,
                min_instance_number: typing.Optional[jsii.Number] = None,
                notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
                region: typing.Optional[builtins.str] = None,
                scaling_configuration_id: typing.Optional[builtins.str] = None,
                security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[str, typing.Any]]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = AsGroupV1Config(
            delete_instances=delete_instances,
            delete_publicip=delete_publicip,
            networks=networks,
            scaling_group_name=scaling_group_name,
            vpc_id=vpc_id,
            available_zones=available_zones,
            cool_down_time=cool_down_time,
            desire_instance_number=desire_instance_number,
            health_periodic_audit_grace_period=health_periodic_audit_grace_period,
            health_periodic_audit_method=health_periodic_audit_method,
            health_periodic_audit_time=health_periodic_audit_time,
            id=id,
            instance_terminate_policy=instance_terminate_policy,
            lbaas_listeners=lbaas_listeners,
            lb_listener_id=lb_listener_id,
            max_instance_number=max_instance_number,
            min_instance_number=min_instance_number,
            notifications=notifications,
            region=region,
            scaling_configuration_id=scaling_configuration_id,
            security_groups=security_groups,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLbaasListeners")
    def put_lbaas_listeners(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLbaasListeners", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="putSecurityGroups")
    def put_security_groups(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = AsGroupV1SecurityGroups(id=id)

        return typing.cast(None, jsii.invoke(self, "putSecurityGroups", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#create AsGroupV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete AsGroupV1#delete}.
        '''
        value = AsGroupV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailableZones")
    def reset_available_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableZones", []))

    @jsii.member(jsii_name="resetCoolDownTime")
    def reset_cool_down_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownTime", []))

    @jsii.member(jsii_name="resetDesireInstanceNumber")
    def reset_desire_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesireInstanceNumber", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditGracePeriod")
    def reset_health_periodic_audit_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditGracePeriod", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditMethod")
    def reset_health_periodic_audit_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditMethod", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditTime")
    def reset_health_periodic_audit_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceTerminatePolicy")
    def reset_instance_terminate_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTerminatePolicy", []))

    @jsii.member(jsii_name="resetLbaasListeners")
    def reset_lbaas_listeners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbaasListeners", []))

    @jsii.member(jsii_name="resetLbListenerId")
    def reset_lb_listener_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbListenerId", []))

    @jsii.member(jsii_name="resetMaxInstanceNumber")
    def reset_max_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceNumber", []))

    @jsii.member(jsii_name="resetMinInstanceNumber")
    def reset_min_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceNumber", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingConfigurationId")
    def reset_scaling_configuration_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfigurationId", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="currentInstanceNumber")
    def current_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "currentInstanceNumber"))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @builtins.property
    @jsii.member(jsii_name="lbaasListeners")
    def lbaas_listeners(self) -> "AsGroupV1LbaasListenersList":
        return typing.cast("AsGroupV1LbaasListenersList", jsii.get(self, "lbaasListeners"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "AsGroupV1NetworksList":
        return typing.cast("AsGroupV1NetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> "AsGroupV1SecurityGroupsOutputReference":
        return typing.cast("AsGroupV1SecurityGroupsOutputReference", jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AsGroupV1TimeoutsOutputReference":
        return typing.cast("AsGroupV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownTimeInput")
    def cool_down_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolDownTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInstancesInput")
    def delete_instances_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletePublicipInput")
    def delete_publicip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "deletePublicipInput"))

    @builtins.property
    @jsii.member(jsii_name="desireInstanceNumberInput")
    def desire_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desireInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditGracePeriodInput")
    def health_periodic_audit_grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthPeriodicAuditGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditMethodInput")
    def health_periodic_audit_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthPeriodicAuditMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditTimeInput")
    def health_periodic_audit_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthPeriodicAuditTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTerminatePolicyInput")
    def instance_terminate_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTerminatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="lbaasListenersInput")
    def lbaas_listeners_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1LbaasListeners"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1LbaasListeners"]]], jsii.get(self, "lbaasListenersInput"))

    @builtins.property
    @jsii.member(jsii_name="lbListenerIdInput")
    def lb_listener_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lbListenerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNumberInput")
    def max_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceNumberInput")
    def min_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1Networks"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1Networks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigurationIdInput")
    def scaling_configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingConfigurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupNameInput")
    def scaling_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional["AsGroupV1SecurityGroups"]:
        return typing.cast(typing.Optional["AsGroupV1SecurityGroups"], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["AsGroupV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AsGroupV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value)

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
    @jsii.member(jsii_name="deleteInstances")
    def delete_instances(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteInstances"))

    @delete_instances.setter
    def delete_instances(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteInstances", value)

    @builtins.property
    @jsii.member(jsii_name="deletePublicip")
    def delete_publicip(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "deletePublicip"))

    @delete_publicip.setter
    def delete_publicip(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletePublicip", value)

    @builtins.property
    @jsii.member(jsii_name="desireInstanceNumber")
    def desire_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desireInstanceNumber"))

    @desire_instance_number.setter
    def desire_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desireInstanceNumber", value)

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditGracePeriod")
    def health_periodic_audit_grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthPeriodicAuditGracePeriod"))

    @health_periodic_audit_grace_period.setter
    def health_periodic_audit_grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditGracePeriod", value)

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditMethod")
    def health_periodic_audit_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthPeriodicAuditMethod"))

    @health_periodic_audit_method.setter
    def health_periodic_audit_method(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditMethod", value)

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditTime")
    def health_periodic_audit_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthPeriodicAuditTime"))

    @health_periodic_audit_time.setter
    def health_periodic_audit_time(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditTime", value)

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
    @jsii.member(jsii_name="instanceTerminatePolicy")
    def instance_terminate_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminatePolicy"))

    @instance_terminate_policy.setter
    def instance_terminate_policy(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminatePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="lbListenerId")
    def lb_listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lbListenerId"))

    @lb_listener_id.setter
    def lb_listener_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbListenerId", value)

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNumber")
    def max_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceNumber"))

    @max_instance_number.setter
    def max_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceNumber", value)

    @builtins.property
    @jsii.member(jsii_name="minInstanceNumber")
    def min_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceNumber"))

    @min_instance_number.setter
    def min_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceNumber", value)

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifications"))

    @notifications.setter
    def notifications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifications", value)

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
    @jsii.member(jsii_name="scalingConfigurationId")
    def scaling_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingConfigurationId"))

    @scaling_configuration_id.setter
    def scaling_configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingConfigurationId", value)

    @builtins.property
    @jsii.member(jsii_name="scalingGroupName")
    def scaling_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupName"))

    @scaling_group_name.setter
    def scaling_group_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "delete_instances": "deleteInstances",
        "delete_publicip": "deletePublicip",
        "networks": "networks",
        "scaling_group_name": "scalingGroupName",
        "vpc_id": "vpcId",
        "available_zones": "availableZones",
        "cool_down_time": "coolDownTime",
        "desire_instance_number": "desireInstanceNumber",
        "health_periodic_audit_grace_period": "healthPeriodicAuditGracePeriod",
        "health_periodic_audit_method": "healthPeriodicAuditMethod",
        "health_periodic_audit_time": "healthPeriodicAuditTime",
        "id": "id",
        "instance_terminate_policy": "instanceTerminatePolicy",
        "lbaas_listeners": "lbaasListeners",
        "lb_listener_id": "lbListenerId",
        "max_instance_number": "maxInstanceNumber",
        "min_instance_number": "minInstanceNumber",
        "notifications": "notifications",
        "region": "region",
        "scaling_configuration_id": "scalingConfigurationId",
        "security_groups": "securityGroups",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class AsGroupV1Config(cdktf.TerraformMetaArguments):
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
        delete_instances: builtins.str,
        delete_publicip: typing.Union[builtins.bool, cdktf.IResolvable],
        networks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
        scaling_group_name: builtins.str,
        vpc_id: builtins.str,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        desire_instance_number: typing.Optional[jsii.Number] = None,
        health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
        health_periodic_audit_method: typing.Optional[builtins.str] = None,
        health_periodic_audit_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        instance_terminate_policy: typing.Optional[builtins.str] = None,
        lbaas_listeners: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]]] = None,
        lb_listener_id: typing.Optional[builtins.str] = None,
        max_instance_number: typing.Optional[jsii.Number] = None,
        min_instance_number: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_configuration_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param delete_instances: Whether to delete instances when they are removed from the AS group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_instances AsGroupV1#delete_instances}
        :param delete_publicip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.
        :param networks: networks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#networks AsGroupV1#networks}
        :param scaling_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#vpc_id AsGroupV1#vpc_id}.
        :param available_zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#available_zones AsGroupV1#available_zones}.
        :param cool_down_time: The cooling duration, in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        :param desire_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.
        :param health_periodic_audit_grace_period: The grace period for instance health check, in seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        :param health_periodic_audit_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.
        :param health_periodic_audit_time: The health check period for instances, in minutes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_terminate_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.
        :param lbaas_listeners: lbaas_listeners block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        :param lb_listener_id: The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        :param max_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.
        :param min_instance_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.
        :param notifications: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#notifications AsGroupV1#notifications}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#region AsGroupV1#region}.
        :param scaling_configuration_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.
        :param security_groups: security_groups block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#security_groups AsGroupV1#security_groups}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#tags AsGroupV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#timeouts AsGroupV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security_groups, dict):
            security_groups = AsGroupV1SecurityGroups(**security_groups)
        if isinstance(timeouts, dict):
            timeouts = AsGroupV1Timeouts(**timeouts)
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
                delete_instances: builtins.str,
                delete_publicip: typing.Union[builtins.bool, cdktf.IResolvable],
                networks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[str, typing.Any]]]],
                scaling_group_name: builtins.str,
                vpc_id: builtins.str,
                available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
                cool_down_time: typing.Optional[jsii.Number] = None,
                desire_instance_number: typing.Optional[jsii.Number] = None,
                health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
                health_periodic_audit_method: typing.Optional[builtins.str] = None,
                health_periodic_audit_time: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                instance_terminate_policy: typing.Optional[builtins.str] = None,
                lbaas_listeners: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[str, typing.Any]]]]] = None,
                lb_listener_id: typing.Optional[builtins.str] = None,
                max_instance_number: typing.Optional[jsii.Number] = None,
                min_instance_number: typing.Optional[jsii.Number] = None,
                notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
                region: typing.Optional[builtins.str] = None,
                scaling_configuration_id: typing.Optional[builtins.str] = None,
                security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[str, typing.Any]]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument delete_instances", value=delete_instances, expected_type=type_hints["delete_instances"])
            check_type(argname="argument delete_publicip", value=delete_publicip, expected_type=type_hints["delete_publicip"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument scaling_group_name", value=scaling_group_name, expected_type=type_hints["scaling_group_name"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument cool_down_time", value=cool_down_time, expected_type=type_hints["cool_down_time"])
            check_type(argname="argument desire_instance_number", value=desire_instance_number, expected_type=type_hints["desire_instance_number"])
            check_type(argname="argument health_periodic_audit_grace_period", value=health_periodic_audit_grace_period, expected_type=type_hints["health_periodic_audit_grace_period"])
            check_type(argname="argument health_periodic_audit_method", value=health_periodic_audit_method, expected_type=type_hints["health_periodic_audit_method"])
            check_type(argname="argument health_periodic_audit_time", value=health_periodic_audit_time, expected_type=type_hints["health_periodic_audit_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_terminate_policy", value=instance_terminate_policy, expected_type=type_hints["instance_terminate_policy"])
            check_type(argname="argument lbaas_listeners", value=lbaas_listeners, expected_type=type_hints["lbaas_listeners"])
            check_type(argname="argument lb_listener_id", value=lb_listener_id, expected_type=type_hints["lb_listener_id"])
            check_type(argname="argument max_instance_number", value=max_instance_number, expected_type=type_hints["max_instance_number"])
            check_type(argname="argument min_instance_number", value=min_instance_number, expected_type=type_hints["min_instance_number"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_configuration_id", value=scaling_configuration_id, expected_type=type_hints["scaling_configuration_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "delete_instances": delete_instances,
            "delete_publicip": delete_publicip,
            "networks": networks,
            "scaling_group_name": scaling_group_name,
            "vpc_id": vpc_id,
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
        if available_zones is not None:
            self._values["available_zones"] = available_zones
        if cool_down_time is not None:
            self._values["cool_down_time"] = cool_down_time
        if desire_instance_number is not None:
            self._values["desire_instance_number"] = desire_instance_number
        if health_periodic_audit_grace_period is not None:
            self._values["health_periodic_audit_grace_period"] = health_periodic_audit_grace_period
        if health_periodic_audit_method is not None:
            self._values["health_periodic_audit_method"] = health_periodic_audit_method
        if health_periodic_audit_time is not None:
            self._values["health_periodic_audit_time"] = health_periodic_audit_time
        if id is not None:
            self._values["id"] = id
        if instance_terminate_policy is not None:
            self._values["instance_terminate_policy"] = instance_terminate_policy
        if lbaas_listeners is not None:
            self._values["lbaas_listeners"] = lbaas_listeners
        if lb_listener_id is not None:
            self._values["lb_listener_id"] = lb_listener_id
        if max_instance_number is not None:
            self._values["max_instance_number"] = max_instance_number
        if min_instance_number is not None:
            self._values["min_instance_number"] = min_instance_number
        if notifications is not None:
            self._values["notifications"] = notifications
        if region is not None:
            self._values["region"] = region
        if scaling_configuration_id is not None:
            self._values["scaling_configuration_id"] = scaling_configuration_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def delete_instances(self) -> builtins.str:
        '''Whether to delete instances when they are removed from the AS group.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_instances AsGroupV1#delete_instances}
        '''
        result = self._values.get("delete_instances")
        assert result is not None, "Required property 'delete_instances' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_publicip(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.'''
        result = self._values.get("delete_publicip")
        assert result is not None, "Required property 'delete_publicip' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["AsGroupV1Networks"]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#networks AsGroupV1#networks}
        '''
        result = self._values.get("networks")
        assert result is not None, "Required property 'networks' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["AsGroupV1Networks"]], result)

    @builtins.property
    def scaling_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.'''
        result = self._values.get("scaling_group_name")
        assert result is not None, "Required property 'scaling_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#vpc_id AsGroupV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def available_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#available_zones AsGroupV1#available_zones}.'''
        result = self._values.get("available_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cool_down_time(self) -> typing.Optional[jsii.Number]:
        '''The cooling duration, in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        '''
        result = self._values.get("cool_down_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desire_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.'''
        result = self._values.get("desire_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_periodic_audit_grace_period(self) -> typing.Optional[jsii.Number]:
        '''The grace period for instance health check, in seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        '''
        result = self._values.get("health_periodic_audit_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_periodic_audit_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.'''
        result = self._values.get("health_periodic_audit_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_periodic_audit_time(self) -> typing.Optional[jsii.Number]:
        '''The health check period for instances, in minutes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        '''
        result = self._values.get("health_periodic_audit_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_terminate_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.'''
        result = self._values.get("instance_terminate_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lbaas_listeners(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1LbaasListeners"]]]:
        '''lbaas_listeners block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        '''
        result = self._values.get("lbaas_listeners")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AsGroupV1LbaasListeners"]]], result)

    @builtins.property
    def lb_listener_id(self) -> typing.Optional[builtins.str]:
        '''The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        '''
        result = self._values.get("lb_listener_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.'''
        result = self._values.get("max_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.'''
        result = self._values.get("min_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#notifications AsGroupV1#notifications}.'''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#region AsGroupV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configuration_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.'''
        result = self._values.get("scaling_configuration_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional["AsGroupV1SecurityGroups"]:
        '''security_groups block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#security_groups AsGroupV1#security_groups}
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional["AsGroupV1SecurityGroups"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#tags AsGroupV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AsGroupV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#timeouts AsGroupV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AsGroupV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListeners",
    jsii_struct_bases=[],
    name_mapping={
        "pool_id": "poolId",
        "protocol_port": "protocolPort",
        "weight": "weight",
    },
)
class AsGroupV1LbaasListeners:
    def __init__(
        self,
        *,
        pool_id: builtins.str,
        protocol_port: jsii.Number,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#pool_id AsGroupV1#pool_id}.
        :param protocol_port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#protocol_port AsGroupV1#protocol_port}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#weight AsGroupV1#weight}.
        '''
        if __debug__:
            def stub(
                *,
                pool_id: builtins.str,
                protocol_port: jsii.Number,
                weight: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[str, typing.Any] = {
            "pool_id": pool_id,
            "protocol_port": protocol_port,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#pool_id AsGroupV1#pool_id}.'''
        result = self._values.get("pool_id")
        assert result is not None, "Required property 'pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#protocol_port AsGroupV1#protocol_port}.'''
        result = self._values.get("protocol_port")
        assert result is not None, "Required property 'protocol_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#weight AsGroupV1#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1LbaasListeners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1LbaasListenersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListenersList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsGroupV1LbaasListenersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsGroupV1LbaasListenersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1LbaasListeners]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1LbaasListeners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1LbaasListeners]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1LbaasListeners]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AsGroupV1LbaasListenersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListenersOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="poolIdInput")
    def pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortInput")
    def protocol_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolPortInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="poolId")
    def pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolId"))

    @pool_id.setter
    def pool_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolId", value)

    @builtins.property
    @jsii.member(jsii_name="protocolPort")
    def protocol_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolPort"))

    @protocol_port.setter
    def protocol_port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPort", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AsGroupV1LbaasListeners, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AsGroupV1LbaasListeners, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AsGroupV1LbaasListeners, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[AsGroupV1LbaasListeners, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Networks",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class AsGroupV1Networks:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            def stub(*, id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Networks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1NetworksList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1NetworksList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsGroupV1NetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsGroupV1NetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1Networks]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1Networks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1Networks]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AsGroupV1Networks]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AsGroupV1NetworksOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1NetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AsGroupV1Networks, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AsGroupV1Networks, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AsGroupV1Networks, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[AsGroupV1Networks, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1SecurityGroups",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class AsGroupV1SecurityGroups:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            def stub(*, id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1SecurityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1SecurityGroupsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1SecurityGroupsOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsGroupV1SecurityGroups]:
        return typing.cast(typing.Optional[AsGroupV1SecurityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AsGroupV1SecurityGroups]) -> None:
        if __debug__:
            def stub(value: typing.Optional[AsGroupV1SecurityGroups]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class AsGroupV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#create AsGroupV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete AsGroupV1#delete}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#create AsGroupV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/as_group_v1#delete AsGroupV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1TimeoutsOutputReference",
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

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AsGroupV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AsGroupV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AsGroupV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[AsGroupV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AsGroupV1",
    "AsGroupV1Config",
    "AsGroupV1LbaasListeners",
    "AsGroupV1LbaasListenersList",
    "AsGroupV1LbaasListenersOutputReference",
    "AsGroupV1Networks",
    "AsGroupV1NetworksList",
    "AsGroupV1NetworksOutputReference",
    "AsGroupV1SecurityGroups",
    "AsGroupV1SecurityGroupsOutputReference",
    "AsGroupV1Timeouts",
    "AsGroupV1TimeoutsOutputReference",
]

publication.publish()
