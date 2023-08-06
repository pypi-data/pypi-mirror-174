'''
# `opentelekomcloud_waf_domain_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_waf_domain_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1).
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


class WafDomainV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1 opentelekomcloud_waf_domain_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        hostname: builtins.str,
        proxy: typing.Union[builtins.bool, cdktf.IResolvable],
        server: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        sip_header_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        tls: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1 opentelekomcloud_waf_domain_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#hostname WafDomainV1#hostname}.
        :param proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#proxy WafDomainV1#proxy}.
        :param server: server block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#server WafDomainV1#server}
        :param certificate_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#cipher WafDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#id WafDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#policy_id WafDomainV1#policy_id}.
        :param sip_header_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.
        :param sip_header_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#timeouts WafDomainV1#timeouts}
        :param tls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#tls WafDomainV1#tls}.
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
                hostname: builtins.str,
                proxy: typing.Union[builtins.bool, cdktf.IResolvable],
                server: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
                certificate_id: typing.Optional[builtins.str] = None,
                cipher: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                policy_id: typing.Optional[builtins.str] = None,
                sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
                sip_header_name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[str, typing.Any]]] = None,
                tls: typing.Optional[builtins.str] = None,
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
        config = WafDomainV1Config(
            hostname=hostname,
            proxy=proxy,
            server=server,
            certificate_id=certificate_id,
            cipher=cipher,
            id=id,
            policy_id=policy_id,
            sip_header_list=sip_header_list,
            sip_header_name=sip_header_name,
            timeouts=timeouts,
            tls=tls,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putServer")
    def put_server(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServer", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#create WafDomainV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#delete WafDomainV1#delete}.
        '''
        value = WafDomainV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertificateId")
    def reset_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateId", []))

    @jsii.member(jsii_name="resetCipher")
    def reset_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCipher", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetSipHeaderList")
    def reset_sip_header_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSipHeaderList", []))

    @jsii.member(jsii_name="resetSipHeaderName")
    def reset_sip_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSipHeaderName", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accessCode")
    def access_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessCode"))

    @builtins.property
    @jsii.member(jsii_name="accessStatus")
    def access_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessStatus"))

    @builtins.property
    @jsii.member(jsii_name="cname")
    def cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cname"))

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protectStatus"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> "WafDomainV1ServerList":
        return typing.cast("WafDomainV1ServerList", jsii.get(self, "server"))

    @builtins.property
    @jsii.member(jsii_name="subDomain")
    def sub_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subDomain"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDomainV1TimeoutsOutputReference":
        return typing.cast("WafDomainV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="txtCode")
    def txt_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "txtCode"))

    @builtins.property
    @jsii.member(jsii_name="certificateIdInput")
    def certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherInput")
    def cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cipherInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["WafDomainV1Server"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["WafDomainV1Server"]]], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="sipHeaderListInput")
    def sip_header_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sipHeaderListInput"))

    @builtins.property
    @jsii.member(jsii_name="sipHeaderNameInput")
    def sip_header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sipHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["WafDomainV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["WafDomainV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @certificate_id.setter
    def certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateId", value)

    @builtins.property
    @jsii.member(jsii_name="cipher")
    def cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cipher"))

    @cipher.setter
    def cipher(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipher", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

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
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "proxy"))

    @proxy.setter
    def proxy(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value)

    @builtins.property
    @jsii.member(jsii_name="sipHeaderList")
    def sip_header_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sipHeaderList"))

    @sip_header_list.setter
    def sip_header_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sipHeaderList", value)

    @builtins.property
    @jsii.member(jsii_name="sipHeaderName")
    def sip_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipHeaderName"))

    @sip_header_name.setter
    def sip_header_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sipHeaderName", value)

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls"))

    @tls.setter
    def tls(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostname": "hostname",
        "proxy": "proxy",
        "server": "server",
        "certificate_id": "certificateId",
        "cipher": "cipher",
        "id": "id",
        "policy_id": "policyId",
        "sip_header_list": "sipHeaderList",
        "sip_header_name": "sipHeaderName",
        "timeouts": "timeouts",
        "tls": "tls",
    },
)
class WafDomainV1Config(cdktf.TerraformMetaArguments):
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
        hostname: builtins.str,
        proxy: typing.Union[builtins.bool, cdktf.IResolvable],
        server: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        sip_header_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        tls: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#hostname WafDomainV1#hostname}.
        :param proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#proxy WafDomainV1#proxy}.
        :param server: server block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#server WafDomainV1#server}
        :param certificate_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#cipher WafDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#id WafDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#policy_id WafDomainV1#policy_id}.
        :param sip_header_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.
        :param sip_header_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#timeouts WafDomainV1#timeouts}
        :param tls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#tls WafDomainV1#tls}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafDomainV1Timeouts(**timeouts)
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
                hostname: builtins.str,
                proxy: typing.Union[builtins.bool, cdktf.IResolvable],
                server: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[str, typing.Any]]]],
                certificate_id: typing.Optional[builtins.str] = None,
                cipher: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                policy_id: typing.Optional[builtins.str] = None,
                sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
                sip_header_name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[str, typing.Any]]] = None,
                tls: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument certificate_id", value=certificate_id, expected_type=type_hints["certificate_id"])
            check_type(argname="argument cipher", value=cipher, expected_type=type_hints["cipher"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument sip_header_list", value=sip_header_list, expected_type=type_hints["sip_header_list"])
            check_type(argname="argument sip_header_name", value=sip_header_name, expected_type=type_hints["sip_header_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[str, typing.Any] = {
            "hostname": hostname,
            "proxy": proxy,
            "server": server,
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
        if certificate_id is not None:
            self._values["certificate_id"] = certificate_id
        if cipher is not None:
            self._values["cipher"] = cipher
        if id is not None:
            self._values["id"] = id
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if sip_header_list is not None:
            self._values["sip_header_list"] = sip_header_list
        if sip_header_name is not None:
            self._values["sip_header_name"] = sip_header_name
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls is not None:
            self._values["tls"] = tls

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
    def hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#hostname WafDomainV1#hostname}.'''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxy(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#proxy WafDomainV1#proxy}.'''
        result = self._values.get("proxy")
        assert result is not None, "Required property 'proxy' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def server(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["WafDomainV1Server"]]:
        '''server block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#server WafDomainV1#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["WafDomainV1Server"]], result)

    @builtins.property
    def certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.'''
        result = self._values.get("certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cipher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#cipher WafDomainV1#cipher}.'''
        result = self._values.get("cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#id WafDomainV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#policy_id WafDomainV1#policy_id}.'''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sip_header_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.'''
        result = self._values.get("sip_header_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sip_header_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.'''
        result = self._values.get("sip_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDomainV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#timeouts WafDomainV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDomainV1Timeouts"], result)

    @builtins.property
    def tls(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#tls WafDomainV1#tls}.'''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Server",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "port": "port",
        "back_protocol": "backProtocol",
        "client_protocol": "clientProtocol",
        "front_protocol": "frontProtocol",
        "server_protocol": "serverProtocol",
    },
)
class WafDomainV1Server:
    def __init__(
        self,
        *,
        address: builtins.str,
        port: builtins.str,
        back_protocol: typing.Optional[builtins.str] = None,
        client_protocol: typing.Optional[builtins.str] = None,
        front_protocol: typing.Optional[builtins.str] = None,
        server_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#address WafDomainV1#address}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#port WafDomainV1#port}.
        :param back_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#back_protocol WafDomainV1#back_protocol}.
        :param client_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#client_protocol WafDomainV1#client_protocol}.
        :param front_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#front_protocol WafDomainV1#front_protocol}.
        :param server_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#server_protocol WafDomainV1#server_protocol}.
        '''
        if __debug__:
            def stub(
                *,
                address: builtins.str,
                port: builtins.str,
                back_protocol: typing.Optional[builtins.str] = None,
                client_protocol: typing.Optional[builtins.str] = None,
                front_protocol: typing.Optional[builtins.str] = None,
                server_protocol: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument back_protocol", value=back_protocol, expected_type=type_hints["back_protocol"])
            check_type(argname="argument client_protocol", value=client_protocol, expected_type=type_hints["client_protocol"])
            check_type(argname="argument front_protocol", value=front_protocol, expected_type=type_hints["front_protocol"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
        self._values: typing.Dict[str, typing.Any] = {
            "address": address,
            "port": port,
        }
        if back_protocol is not None:
            self._values["back_protocol"] = back_protocol
        if client_protocol is not None:
            self._values["client_protocol"] = client_protocol
        if front_protocol is not None:
            self._values["front_protocol"] = front_protocol
        if server_protocol is not None:
            self._values["server_protocol"] = server_protocol

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#address WafDomainV1#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#port WafDomainV1#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def back_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#back_protocol WafDomainV1#back_protocol}.'''
        result = self._values.get("back_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#client_protocol WafDomainV1#client_protocol}.'''
        result = self._values.get("client_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def front_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#front_protocol WafDomainV1#front_protocol}.'''
        result = self._values.get("front_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#server_protocol WafDomainV1#server_protocol}.'''
        result = self._values.get("server_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Server(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDomainV1ServerList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1ServerList",
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
    def get(self, index: jsii.Number) -> "WafDomainV1ServerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDomainV1ServerOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[WafDomainV1Server]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[WafDomainV1Server]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[WafDomainV1Server]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[WafDomainV1Server]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WafDomainV1ServerOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1ServerOutputReference",
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

    @jsii.member(jsii_name="resetBackProtocol")
    def reset_back_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackProtocol", []))

    @jsii.member(jsii_name="resetClientProtocol")
    def reset_client_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientProtocol", []))

    @jsii.member(jsii_name="resetFrontProtocol")
    def reset_front_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontProtocol", []))

    @jsii.member(jsii_name="resetServerProtocol")
    def reset_server_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="backProtocolInput")
    def back_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProtocolInput")
    def client_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="frontProtocolInput")
    def front_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serverProtocolInput")
    def server_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="backProtocol")
    def back_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backProtocol"))

    @back_protocol.setter
    def back_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="clientProtocol")
    def client_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientProtocol"))

    @client_protocol.setter
    def client_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="frontProtocol")
    def front_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontProtocol"))

    @front_protocol.setter
    def front_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="serverProtocol")
    def server_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverProtocol"))

    @server_protocol.setter
    def server_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WafDomainV1Server, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WafDomainV1Server, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WafDomainV1Server, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[WafDomainV1Server, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDomainV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#create WafDomainV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#delete WafDomainV1#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#create WafDomainV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_domain_v1#delete WafDomainV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDomainV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[WafDomainV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WafDomainV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WafDomainV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[WafDomainV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "WafDomainV1",
    "WafDomainV1Config",
    "WafDomainV1Server",
    "WafDomainV1ServerList",
    "WafDomainV1ServerOutputReference",
    "WafDomainV1Timeouts",
    "WafDomainV1TimeoutsOutputReference",
]

publication.publish()
