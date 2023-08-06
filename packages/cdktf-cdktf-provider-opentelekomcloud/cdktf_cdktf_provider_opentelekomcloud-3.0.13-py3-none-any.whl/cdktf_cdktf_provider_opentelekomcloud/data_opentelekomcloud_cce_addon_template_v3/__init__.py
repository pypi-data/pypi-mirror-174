'''
# `data_opentelekomcloud_cce_addon_template_v3`

Refer to the Terraform Registory for docs: [`data_opentelekomcloud_cce_addon_template_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3).
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


class DataOpentelekomcloudCceAddonTemplateV3(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCceAddonTemplateV3.DataOpentelekomcloudCceAddonTemplateV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3 opentelekomcloud_cce_addon_template_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        addon_name: builtins.str,
        addon_version: builtins.str,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_versions: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
        swr_addr: typing.Optional[builtins.str] = None,
        swr_user: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3 opentelekomcloud_cce_addon_template_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param addon_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.
        :param addon_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.
        :param cluster_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.
        :param cluster_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.
        :param swr_addr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.
        :param swr_user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.
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
                addon_name: builtins.str,
                addon_version: builtins.str,
                cluster_ip: typing.Optional[builtins.str] = None,
                cluster_versions: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                image_version: typing.Optional[builtins.str] = None,
                swr_addr: typing.Optional[builtins.str] = None,
                swr_user: typing.Optional[builtins.str] = None,
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
        config = DataOpentelekomcloudCceAddonTemplateV3Config(
            addon_name=addon_name,
            addon_version=addon_version,
            cluster_ip=cluster_ip,
            cluster_versions=cluster_versions,
            id=id,
            image_version=image_version,
            swr_addr=swr_addr,
            swr_user=swr_user,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetClusterIp")
    def reset_cluster_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIp", []))

    @jsii.member(jsii_name="resetClusterVersions")
    def reset_cluster_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterVersions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetSwrAddr")
    def reset_swr_addr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwrAddr", []))

    @jsii.member(jsii_name="resetSwrUser")
    def reset_swr_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwrUser", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="addonNameInput")
    def addon_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="addonVersionInput")
    def addon_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addonVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpInput")
    def cluster_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIpInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionsInput")
    def cluster_versions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="swrAddrInput")
    def swr_addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "swrAddrInput"))

    @builtins.property
    @jsii.member(jsii_name="swrUserInput")
    def swr_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "swrUserInput"))

    @builtins.property
    @jsii.member(jsii_name="addonName")
    def addon_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addonName"))

    @addon_name.setter
    def addon_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonName", value)

    @builtins.property
    @jsii.member(jsii_name="addonVersion")
    def addon_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addonVersion"))

    @addon_version.setter
    def addon_version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonVersion", value)

    @builtins.property
    @jsii.member(jsii_name="clusterIp")
    def cluster_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIp"))

    @cluster_ip.setter
    def cluster_ip(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIp", value)

    @builtins.property
    @jsii.member(jsii_name="clusterVersions")
    def cluster_versions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersions"))

    @cluster_versions.setter
    def cluster_versions(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersions", value)

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
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value)

    @builtins.property
    @jsii.member(jsii_name="swrAddr")
    def swr_addr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "swrAddr"))

    @swr_addr.setter
    def swr_addr(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swrAddr", value)

    @builtins.property
    @jsii.member(jsii_name="swrUser")
    def swr_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "swrUser"))

    @swr_user.setter
    def swr_user(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swrUser", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCceAddonTemplateV3.DataOpentelekomcloudCceAddonTemplateV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "addon_name": "addonName",
        "addon_version": "addonVersion",
        "cluster_ip": "clusterIp",
        "cluster_versions": "clusterVersions",
        "id": "id",
        "image_version": "imageVersion",
        "swr_addr": "swrAddr",
        "swr_user": "swrUser",
    },
)
class DataOpentelekomcloudCceAddonTemplateV3Config(cdktf.TerraformMetaArguments):
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
        addon_name: builtins.str,
        addon_version: builtins.str,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_versions: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
        swr_addr: typing.Optional[builtins.str] = None,
        swr_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param addon_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.
        :param addon_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.
        :param cluster_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.
        :param cluster_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.
        :param swr_addr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.
        :param swr_user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.
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
                addon_name: builtins.str,
                addon_version: builtins.str,
                cluster_ip: typing.Optional[builtins.str] = None,
                cluster_versions: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                image_version: typing.Optional[builtins.str] = None,
                swr_addr: typing.Optional[builtins.str] = None,
                swr_user: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument addon_name", value=addon_name, expected_type=type_hints["addon_name"])
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument cluster_ip", value=cluster_ip, expected_type=type_hints["cluster_ip"])
            check_type(argname="argument cluster_versions", value=cluster_versions, expected_type=type_hints["cluster_versions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument swr_addr", value=swr_addr, expected_type=type_hints["swr_addr"])
            check_type(argname="argument swr_user", value=swr_user, expected_type=type_hints["swr_user"])
        self._values: typing.Dict[str, typing.Any] = {
            "addon_name": addon_name,
            "addon_version": addon_version,
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
        if cluster_ip is not None:
            self._values["cluster_ip"] = cluster_ip
        if cluster_versions is not None:
            self._values["cluster_versions"] = cluster_versions
        if id is not None:
            self._values["id"] = id
        if image_version is not None:
            self._values["image_version"] = image_version
        if swr_addr is not None:
            self._values["swr_addr"] = swr_addr
        if swr_user is not None:
            self._values["swr_user"] = swr_user

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
    def addon_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.'''
        result = self._values.get("addon_name")
        assert result is not None, "Required property 'addon_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addon_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.'''
        result = self._values.get("addon_version")
        assert result is not None, "Required property 'addon_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.'''
        result = self._values.get("cluster_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_versions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.'''
        result = self._values.get("cluster_versions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.'''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swr_addr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.'''
        result = self._values.get("swr_addr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swr_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/d/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.'''
        result = self._values.get("swr_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCceAddonTemplateV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudCceAddonTemplateV3",
    "DataOpentelekomcloudCceAddonTemplateV3Config",
]

publication.publish()
