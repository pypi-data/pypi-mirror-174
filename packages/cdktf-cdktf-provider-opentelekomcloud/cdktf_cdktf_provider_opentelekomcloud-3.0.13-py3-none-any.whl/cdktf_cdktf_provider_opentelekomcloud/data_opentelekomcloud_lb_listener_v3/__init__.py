'''
# `data_opentelekomcloud_lb_listener_v3`

Refer to the Terraform Registory for docs: [`data_opentelekomcloud_lb_listener_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3).
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


class DataOpentelekomcloudLbListenerV3(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3 opentelekomcloud_lb_listener_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        loadbalancer_id: typing.Optional[builtins.str] = None,
        member_address: typing.Optional[builtins.str] = None,
        member_device_id: typing.Optional[builtins.str] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_port: typing.Optional[jsii.Number] = None,
        tls_ciphers_policy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3 opentelekomcloud_lb_listener_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.
        :param member_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.
        :param member_device_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.
        :param member_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.
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
                client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
                client_timeout: typing.Optional[jsii.Number] = None,
                default_pool_id: typing.Optional[builtins.str] = None,
                default_tls_container_ref: typing.Optional[builtins.str] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                keep_alive_timeout: typing.Optional[jsii.Number] = None,
                loadbalancer_id: typing.Optional[builtins.str] = None,
                member_address: typing.Optional[builtins.str] = None,
                member_device_id: typing.Optional[builtins.str] = None,
                member_timeout: typing.Optional[jsii.Number] = None,
                name: typing.Optional[builtins.str] = None,
                protocol: typing.Optional[builtins.str] = None,
                protocol_port: typing.Optional[jsii.Number] = None,
                tls_ciphers_policy: typing.Optional[builtins.str] = None,
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
        config = DataOpentelekomcloudLbListenerV3Config(
            client_ca_tls_container_ref=client_ca_tls_container_ref,
            client_timeout=client_timeout,
            default_pool_id=default_pool_id,
            default_tls_container_ref=default_tls_container_ref,
            description=description,
            id=id,
            keep_alive_timeout=keep_alive_timeout,
            loadbalancer_id=loadbalancer_id,
            member_address=member_address,
            member_device_id=member_device_id,
            member_timeout=member_timeout,
            name=name,
            protocol=protocol,
            protocol_port=protocol_port,
            tls_ciphers_policy=tls_ciphers_policy,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetClientCaTlsContainerRef")
    def reset_client_ca_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCaTlsContainerRef", []))

    @jsii.member(jsii_name="resetClientTimeout")
    def reset_client_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTimeout", []))

    @jsii.member(jsii_name="resetDefaultPoolId")
    def reset_default_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPoolId", []))

    @jsii.member(jsii_name="resetDefaultTlsContainerRef")
    def reset_default_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsContainerRef", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetLoadbalancerId")
    def reset_loadbalancer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadbalancerId", []))

    @jsii.member(jsii_name="resetMemberAddress")
    def reset_member_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberAddress", []))

    @jsii.member(jsii_name="resetMemberDeviceId")
    def reset_member_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberDeviceId", []))

    @jsii.member(jsii_name="resetMemberTimeout")
    def reset_member_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberTimeout", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetProtocolPort")
    def reset_protocol_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolPort", []))

    @jsii.member(jsii_name="resetTlsCiphersPolicy")
    def reset_tls_ciphers_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCiphersPolicy", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="http2Enable")
    def http2_enable(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "http2Enable"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaders")
    def insert_headers(self) -> "DataOpentelekomcloudLbListenerV3InsertHeadersList":
        return typing.cast("DataOpentelekomcloudLbListenerV3InsertHeadersList", jsii.get(self, "insertHeaders"))

    @builtins.property
    @jsii.member(jsii_name="memberRetryEnable")
    def member_retry_enable(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "memberRetryEnable"))

    @builtins.property
    @jsii.member(jsii_name="memoryRetryEnable")
    def memory_retry_enable(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "memoryRetryEnable"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefs")
    def sni_container_refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sniContainerRefs"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> cdktf.StringMap:
        return typing.cast(cdktf.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRefInput")
    def client_ca_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCaTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTimeoutInput")
    def client_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolIdInput")
    def default_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRefInput")
    def default_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerIdInput")
    def loadbalancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="memberAddressInput")
    def member_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="memberDeviceIdInput")
    def member_device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberDeviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="memberTimeoutInput")
    def member_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memberTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortInput")
    def protocol_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolPortInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersPolicyInput")
    def tls_ciphers_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCiphersPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRef")
    def client_ca_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCaTlsContainerRef"))

    @client_ca_tls_container_ref.setter
    def client_ca_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCaTlsContainerRef", value)

    @builtins.property
    @jsii.member(jsii_name="clientTimeout")
    def client_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTimeout"))

    @client_timeout.setter
    def client_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="defaultPoolId")
    def default_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPoolId"))

    @default_pool_id.setter
    def default_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRef")
    def default_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTlsContainerRef"))

    @default_tls_container_ref.setter
    def default_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsContainerRef", value)

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
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="loadbalancerId")
    def loadbalancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancerId"))

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerId", value)

    @builtins.property
    @jsii.member(jsii_name="memberAddress")
    def member_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberAddress"))

    @member_address.setter
    def member_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberAddress", value)

    @builtins.property
    @jsii.member(jsii_name="memberDeviceId")
    def member_device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberDeviceId"))

    @member_device_id.setter
    def member_device_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberDeviceId", value)

    @builtins.property
    @jsii.member(jsii_name="memberTimeout")
    def member_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memberTimeout"))

    @member_timeout.setter
    def member_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberTimeout", value)

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
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

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
    @jsii.member(jsii_name="tlsCiphersPolicy")
    def tls_ciphers_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCiphersPolicy"))

    @tls_ciphers_policy.setter
    def tls_ciphers_policy(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCiphersPolicy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_ca_tls_container_ref": "clientCaTlsContainerRef",
        "client_timeout": "clientTimeout",
        "default_pool_id": "defaultPoolId",
        "default_tls_container_ref": "defaultTlsContainerRef",
        "description": "description",
        "id": "id",
        "keep_alive_timeout": "keepAliveTimeout",
        "loadbalancer_id": "loadbalancerId",
        "member_address": "memberAddress",
        "member_device_id": "memberDeviceId",
        "member_timeout": "memberTimeout",
        "name": "name",
        "protocol": "protocol",
        "protocol_port": "protocolPort",
        "tls_ciphers_policy": "tlsCiphersPolicy",
    },
)
class DataOpentelekomcloudLbListenerV3Config(cdktf.TerraformMetaArguments):
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
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        loadbalancer_id: typing.Optional[builtins.str] = None,
        member_address: typing.Optional[builtins.str] = None,
        member_device_id: typing.Optional[builtins.str] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_port: typing.Optional[jsii.Number] = None,
        tls_ciphers_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.
        :param member_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.
        :param member_device_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.
        :param member_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.
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
                client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
                client_timeout: typing.Optional[jsii.Number] = None,
                default_pool_id: typing.Optional[builtins.str] = None,
                default_tls_container_ref: typing.Optional[builtins.str] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                keep_alive_timeout: typing.Optional[jsii.Number] = None,
                loadbalancer_id: typing.Optional[builtins.str] = None,
                member_address: typing.Optional[builtins.str] = None,
                member_device_id: typing.Optional[builtins.str] = None,
                member_timeout: typing.Optional[jsii.Number] = None,
                name: typing.Optional[builtins.str] = None,
                protocol: typing.Optional[builtins.str] = None,
                protocol_port: typing.Optional[jsii.Number] = None,
                tls_ciphers_policy: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument client_ca_tls_container_ref", value=client_ca_tls_container_ref, expected_type=type_hints["client_ca_tls_container_ref"])
            check_type(argname="argument client_timeout", value=client_timeout, expected_type=type_hints["client_timeout"])
            check_type(argname="argument default_pool_id", value=default_pool_id, expected_type=type_hints["default_pool_id"])
            check_type(argname="argument default_tls_container_ref", value=default_tls_container_ref, expected_type=type_hints["default_tls_container_ref"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument loadbalancer_id", value=loadbalancer_id, expected_type=type_hints["loadbalancer_id"])
            check_type(argname="argument member_address", value=member_address, expected_type=type_hints["member_address"])
            check_type(argname="argument member_device_id", value=member_device_id, expected_type=type_hints["member_device_id"])
            check_type(argname="argument member_timeout", value=member_timeout, expected_type=type_hints["member_timeout"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument tls_ciphers_policy", value=tls_ciphers_policy, expected_type=type_hints["tls_ciphers_policy"])
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
        if client_ca_tls_container_ref is not None:
            self._values["client_ca_tls_container_ref"] = client_ca_tls_container_ref
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if default_pool_id is not None:
            self._values["default_pool_id"] = default_pool_id
        if default_tls_container_ref is not None:
            self._values["default_tls_container_ref"] = default_tls_container_ref
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if loadbalancer_id is not None:
            self._values["loadbalancer_id"] = loadbalancer_id
        if member_address is not None:
            self._values["member_address"] = member_address
        if member_device_id is not None:
            self._values["member_device_id"] = member_device_id
        if member_timeout is not None:
            self._values["member_timeout"] = member_timeout
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_port is not None:
            self._values["protocol_port"] = protocol_port
        if tls_ciphers_policy is not None:
            self._values["tls_ciphers_policy"] = tls_ciphers_policy

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
    def client_ca_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.'''
        result = self._values.get("client_ca_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.'''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.'''
        result = self._values.get("default_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.'''
        result = self._values.get("default_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.'''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def loadbalancer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.'''
        result = self._values.get("loadbalancer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.'''
        result = self._values.get("member_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.'''
        result = self._values.get("member_device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.'''
        result = self._values.get("member_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.'''
        result = self._values.get("protocol_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_ciphers_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.'''
        result = self._values.get("tls_ciphers_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbListenerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeaders",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudLbListenerV3InsertHeaders:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbListenerV3InsertHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudLbListenerV3InsertHeadersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeadersList",
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
    ) -> "DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference", jsii.invoke(self, "get", [index]))

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


class DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference",
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
    @jsii.member(jsii_name="forwardedForPort")
    def forwarded_for_port(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "forwardedForPort"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHost")
    def forwarded_host(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "forwardedHost"))

    @builtins.property
    @jsii.member(jsii_name="forwardedPort")
    def forwarded_port(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "forwardedPort"))

    @builtins.property
    @jsii.member(jsii_name="forwardElbIp")
    def forward_elb_ip(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "forwardElbIp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders]:
        return typing.cast(typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataOpentelekomcloudLbListenerV3",
    "DataOpentelekomcloudLbListenerV3Config",
    "DataOpentelekomcloudLbListenerV3InsertHeaders",
    "DataOpentelekomcloudLbListenerV3InsertHeadersList",
    "DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference",
]

publication.publish()
