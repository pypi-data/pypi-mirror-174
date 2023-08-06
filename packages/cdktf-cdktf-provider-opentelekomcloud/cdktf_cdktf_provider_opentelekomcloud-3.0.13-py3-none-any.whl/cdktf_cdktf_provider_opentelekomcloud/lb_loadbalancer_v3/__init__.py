'''
# `opentelekomcloud_lb_loadbalancer_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_lb_loadbalancer_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3).
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


class LbLoadbalancerV3(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        network_ids: typing.Sequence[builtins.str],
        admin_state_up: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_target_enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[str, typing.Any]]] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vip_address: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.
        :param network_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_target_enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.
        :param l4_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        :param router_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.
        :param vip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.
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
                availability_zones: typing.Sequence[builtins.str],
                network_ids: typing.Sequence[builtins.str],
                admin_state_up: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                ip_target_enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                l4_flavor: typing.Optional[builtins.str] = None,
                l7_flavor: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[str, typing.Any]]] = None,
                router_id: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                vip_address: typing.Optional[builtins.str] = None,
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
        config = LbLoadbalancerV3Config(
            availability_zones=availability_zones,
            network_ids=network_ids,
            admin_state_up=admin_state_up,
            description=description,
            id=id,
            ip_target_enable=ip_target_enable,
            l4_flavor=l4_flavor,
            l7_flavor=l7_flavor,
            name=name,
            public_ip=public_ip,
            router_id=router_id,
            subnet_id=subnet_id,
            tags=tags,
            vip_address=vip_address,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPublicIp")
    def put_public_ip(
        self,
        *,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_share_type: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.
        :param bandwidth_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.
        :param bandwidth_share_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.
        '''
        value = LbLoadbalancerV3PublicIp(
            bandwidth_charge_mode=bandwidth_charge_mode,
            bandwidth_name=bandwidth_name,
            bandwidth_share_type=bandwidth_share_type,
            bandwidth_size=bandwidth_size,
            id=id,
            ip_type=ip_type,
        )

        return typing.cast(None, jsii.invoke(self, "putPublicIp", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpTargetEnable")
    def reset_ip_target_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpTargetEnable", []))

    @jsii.member(jsii_name="resetL4Flavor")
    def reset_l4_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Flavor", []))

    @jsii.member(jsii_name="resetL7Flavor")
    def reset_l7_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL7Flavor", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPublicIp")
    def reset_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIp", []))

    @jsii.member(jsii_name="resetRouterId")
    def reset_router_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterId", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVipAddress")
    def reset_vip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipAddress", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "LbLoadbalancerV3PublicIpOutputReference":
        return typing.cast("LbLoadbalancerV3PublicIpOutputReference", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="vipPortId")
    def vip_port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipPortId"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTargetEnableInput")
    def ip_target_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "ipTargetEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="l4FlavorInput")
    def l4_flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "l4FlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="l7FlavorInput")
    def l7_flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "l7FlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdsInput")
    def network_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpInput")
    def public_ip_input(self) -> typing.Optional["LbLoadbalancerV3PublicIp"]:
        return typing.cast(typing.Optional["LbLoadbalancerV3PublicIp"], jsii.get(self, "publicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="routerIdInput")
    def router_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vipAddressInput")
    def vip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
    @jsii.member(jsii_name="ipTargetEnable")
    def ip_target_enable(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "ipTargetEnable"))

    @ip_target_enable.setter
    def ip_target_enable(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipTargetEnable", value)

    @builtins.property
    @jsii.member(jsii_name="l4Flavor")
    def l4_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l4Flavor"))

    @l4_flavor.setter
    def l4_flavor(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l4Flavor", value)

    @builtins.property
    @jsii.member(jsii_name="l7Flavor")
    def l7_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l7Flavor"))

    @l7_flavor.setter
    def l7_flavor(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l7Flavor", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkIds")
    def network_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIds"))

    @network_ids.setter
    def network_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIds", value)

    @builtins.property
    @jsii.member(jsii_name="routerId")
    def router_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerId"))

    @router_id.setter
    def router_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routerId", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

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
    @jsii.member(jsii_name="vipAddress")
    def vip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipAddress"))

    @vip_address.setter
    def vip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vipAddress", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zones": "availabilityZones",
        "network_ids": "networkIds",
        "admin_state_up": "adminStateUp",
        "description": "description",
        "id": "id",
        "ip_target_enable": "ipTargetEnable",
        "l4_flavor": "l4Flavor",
        "l7_flavor": "l7Flavor",
        "name": "name",
        "public_ip": "publicIp",
        "router_id": "routerId",
        "subnet_id": "subnetId",
        "tags": "tags",
        "vip_address": "vipAddress",
    },
)
class LbLoadbalancerV3Config(cdktf.TerraformMetaArguments):
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
        availability_zones: typing.Sequence[builtins.str],
        network_ids: typing.Sequence[builtins.str],
        admin_state_up: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_target_enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[str, typing.Any]]] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.
        :param network_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_target_enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.
        :param l4_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        :param router_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.
        :param vip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(public_ip, dict):
            public_ip = LbLoadbalancerV3PublicIp(**public_ip)
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
                availability_zones: typing.Sequence[builtins.str],
                network_ids: typing.Sequence[builtins.str],
                admin_state_up: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                ip_target_enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                l4_flavor: typing.Optional[builtins.str] = None,
                l7_flavor: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[str, typing.Any]]] = None,
                router_id: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                vip_address: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument network_ids", value=network_ids, expected_type=type_hints["network_ids"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_target_enable", value=ip_target_enable, expected_type=type_hints["ip_target_enable"])
            check_type(argname="argument l4_flavor", value=l4_flavor, expected_type=type_hints["l4_flavor"])
            check_type(argname="argument l7_flavor", value=l7_flavor, expected_type=type_hints["l7_flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_ip", value=public_ip, expected_type=type_hints["public_ip"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vip_address", value=vip_address, expected_type=type_hints["vip_address"])
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zones": availability_zones,
            "network_ids": network_ids,
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
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_target_enable is not None:
            self._values["ip_target_enable"] = ip_target_enable
        if l4_flavor is not None:
            self._values["l4_flavor"] = l4_flavor
        if l7_flavor is not None:
            self._values["l7_flavor"] = l7_flavor
        if name is not None:
            self._values["name"] = name
        if public_ip is not None:
            self._values["public_ip"] = public_ip
        if router_id is not None:
            self._values["router_id"] = router_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if vip_address is not None:
            self._values["vip_address"] = vip_address

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
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.'''
        result = self._values.get("network_ids")
        assert result is not None, "Required property 'network_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_target_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.'''
        result = self._values.get("ip_target_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def l4_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.'''
        result = self._values.get("l4_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l7_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.'''
        result = self._values.get("l7_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip(self) -> typing.Optional["LbLoadbalancerV3PublicIp"]:
        '''public_ip block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        '''
        result = self._values.get("public_ip")
        return typing.cast(typing.Optional["LbLoadbalancerV3PublicIp"], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.'''
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.'''
        result = self._values.get("vip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbLoadbalancerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3PublicIp",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_charge_mode": "bandwidthChargeMode",
        "bandwidth_name": "bandwidthName",
        "bandwidth_share_type": "bandwidthShareType",
        "bandwidth_size": "bandwidthSize",
        "id": "id",
        "ip_type": "ipType",
    },
)
class LbLoadbalancerV3PublicIp:
    def __init__(
        self,
        *,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_share_type: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.
        :param bandwidth_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.
        :param bandwidth_share_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.
        '''
        if __debug__:
            def stub(
                *,
                bandwidth_charge_mode: typing.Optional[builtins.str] = None,
                bandwidth_name: typing.Optional[builtins.str] = None,
                bandwidth_share_type: typing.Optional[builtins.str] = None,
                bandwidth_size: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                ip_type: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bandwidth_charge_mode", value=bandwidth_charge_mode, expected_type=type_hints["bandwidth_charge_mode"])
            check_type(argname="argument bandwidth_name", value=bandwidth_name, expected_type=type_hints["bandwidth_name"])
            check_type(argname="argument bandwidth_share_type", value=bandwidth_share_type, expected_type=type_hints["bandwidth_share_type"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_type", value=ip_type, expected_type=type_hints["ip_type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if bandwidth_charge_mode is not None:
            self._values["bandwidth_charge_mode"] = bandwidth_charge_mode
        if bandwidth_name is not None:
            self._values["bandwidth_name"] = bandwidth_name
        if bandwidth_share_type is not None:
            self._values["bandwidth_share_type"] = bandwidth_share_type
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if id is not None:
            self._values["id"] = id
        if ip_type is not None:
            self._values["ip_type"] = ip_type

    @builtins.property
    def bandwidth_charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.'''
        result = self._values.get("bandwidth_charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.'''
        result = self._values.get("bandwidth_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_share_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.'''
        result = self._values.get("bandwidth_share_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#id LbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.'''
        result = self._values.get("ip_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbLoadbalancerV3PublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbLoadbalancerV3PublicIpOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3PublicIpOutputReference",
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

    @jsii.member(jsii_name="resetBandwidthChargeMode")
    def reset_bandwidth_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthChargeMode", []))

    @jsii.member(jsii_name="resetBandwidthName")
    def reset_bandwidth_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthName", []))

    @jsii.member(jsii_name="resetBandwidthShareType")
    def reset_bandwidth_share_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthShareType", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpType")
    def reset_ip_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpType", []))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="managed")
    def managed(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "managed"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeModeInput")
    def bandwidth_charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthChargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthNameInput")
    def bandwidth_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareTypeInput")
    def bandwidth_share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthShareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTypeInput")
    def ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @bandwidth_charge_mode.setter
    def bandwidth_charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthChargeMode", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @bandwidth_name.setter
    def bandwidth_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthName", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareType")
    def bandwidth_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthShareType"))

    @bandwidth_share_type.setter
    def bandwidth_share_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthShareType", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value)

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
    @jsii.member(jsii_name="ipType")
    def ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipType"))

    @ip_type.setter
    def ip_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbLoadbalancerV3PublicIp]:
        return typing.cast(typing.Optional[LbLoadbalancerV3PublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LbLoadbalancerV3PublicIp]) -> None:
        if __debug__:
            def stub(value: typing.Optional[LbLoadbalancerV3PublicIp]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LbLoadbalancerV3",
    "LbLoadbalancerV3Config",
    "LbLoadbalancerV3PublicIp",
    "LbLoadbalancerV3PublicIpOutputReference",
]

publication.publish()
