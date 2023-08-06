'''
# `data_opentelekomcloud_lb_loadbalancer_v3`

Refer to the Terraform Registory for docs: [`data_opentelekomcloud_lb_loadbalancer_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3).
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


class DataOpentelekomcloudLbLoadbalancerV3(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        vip_address: typing.Optional[builtins.str] = None,
        vip_port_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param l4_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.
        :param router_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.
        :param vip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.
        :param vip_port_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.
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
                id: typing.Optional[builtins.str] = None,
                l4_flavor: typing.Optional[builtins.str] = None,
                l7_flavor: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                router_id: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                vip_address: typing.Optional[builtins.str] = None,
                vip_port_id: typing.Optional[builtins.str] = None,
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
        config = DataOpentelekomcloudLbLoadbalancerV3Config(
            id=id,
            l4_flavor=l4_flavor,
            l7_flavor=l7_flavor,
            name=name,
            router_id=router_id,
            subnet_id=subnet_id,
            vip_address=vip_address,
            vip_port_id=vip_port_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetL4Flavor")
    def reset_l4_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Flavor", []))

    @jsii.member(jsii_name="resetL7Flavor")
    def reset_l7_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL7Flavor", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRouterId")
    def reset_router_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterId", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVipAddress")
    def reset_vip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipAddress", []))

    @jsii.member(jsii_name="resetVipPortId")
    def reset_vip_port_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipPortId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "adminStateUp"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="ipTargetEnable")
    def ip_target_enable(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "ipTargetEnable"))

    @builtins.property
    @jsii.member(jsii_name="networkIds")
    def network_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIds"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "DataOpentelekomcloudLbLoadbalancerV3PublicIpList":
        return typing.cast("DataOpentelekomcloudLbLoadbalancerV3PublicIpList", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> cdktf.StringMap:
        return typing.cast(cdktf.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="routerIdInput")
    def router_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vipAddressInput")
    def vip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="vipPortIdInput")
    def vip_port_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipPortIdInput"))

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

    @builtins.property
    @jsii.member(jsii_name="vipPortId")
    def vip_port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipPortId"))

    @vip_port_id.setter
    def vip_port_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vipPortId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "l4_flavor": "l4Flavor",
        "l7_flavor": "l7Flavor",
        "name": "name",
        "router_id": "routerId",
        "subnet_id": "subnetId",
        "vip_address": "vipAddress",
        "vip_port_id": "vipPortId",
    },
)
class DataOpentelekomcloudLbLoadbalancerV3Config(cdktf.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        vip_address: typing.Optional[builtins.str] = None,
        vip_port_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param l4_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.
        :param router_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.
        :param vip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.
        :param vip_port_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
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
                id: typing.Optional[builtins.str] = None,
                l4_flavor: typing.Optional[builtins.str] = None,
                l7_flavor: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                router_id: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                vip_address: typing.Optional[builtins.str] = None,
                vip_port_id: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument l4_flavor", value=l4_flavor, expected_type=type_hints["l4_flavor"])
            check_type(argname="argument l7_flavor", value=l7_flavor, expected_type=type_hints["l7_flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vip_address", value=vip_address, expected_type=type_hints["vip_address"])
            check_type(argname="argument vip_port_id", value=vip_port_id, expected_type=type_hints["vip_port_id"])
        self._values: typing.Dict[str, typing.Any] = {}
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
        if id is not None:
            self._values["id"] = id
        if l4_flavor is not None:
            self._values["l4_flavor"] = l4_flavor
        if l7_flavor is not None:
            self._values["l7_flavor"] = l7_flavor
        if name is not None:
            self._values["name"] = name
        if router_id is not None:
            self._values["router_id"] = router_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if vip_address is not None:
            self._values["vip_address"] = vip_address
        if vip_port_id is not None:
            self._values["vip_port_id"] = vip_port_id

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l4_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.'''
        result = self._values.get("l4_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l7_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.'''
        result = self._values.get("l7_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.'''
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.'''
        result = self._values.get("vip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vip_port_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.'''
        result = self._values.get("vip_port_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbLoadbalancerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIp",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudLbLoadbalancerV3PublicIp:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbLoadbalancerV3PublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudLbLoadbalancerV3PublicIpList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIpList",
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
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference", jsii.invoke(self, "get", [index]))

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


class DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference",
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
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareType")
    def bandwidth_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthShareType"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="ipType")
    def ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp]:
        return typing.cast(typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataOpentelekomcloudLbLoadbalancerV3",
    "DataOpentelekomcloudLbLoadbalancerV3Config",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIp",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIpList",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference",
]

publication.publish()
