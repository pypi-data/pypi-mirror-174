'''
# `opentelekomcloud_css_snapshot_configuration_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_css_snapshot_configuration_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1).
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


class CssSnapshotConfigurationV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1 opentelekomcloud_css_snapshot_configuration_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        automatic: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        configuration: typing.Optional[typing.Union["CssSnapshotConfigurationV1Configuration", typing.Dict[str, typing.Any]]] = None,
        creation_policy: typing.Optional[typing.Union["CssSnapshotConfigurationV1CreationPolicy", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1 opentelekomcloud_css_snapshot_configuration_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#cluster_id CssSnapshotConfigurationV1#cluster_id}.
        :param automatic: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#automatic CssSnapshotConfigurationV1#automatic}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#configuration CssSnapshotConfigurationV1#configuration}
        :param creation_policy: creation_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#creation_policy CssSnapshotConfigurationV1#creation_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#id CssSnapshotConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#timeouts CssSnapshotConfigurationV1#timeouts}
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
                cluster_id: builtins.str,
                automatic: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                configuration: typing.Optional[typing.Union["CssSnapshotConfigurationV1Configuration", typing.Dict[str, typing.Any]]] = None,
                creation_policy: typing.Optional[typing.Union["CssSnapshotConfigurationV1CreationPolicy", typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = CssSnapshotConfigurationV1Config(
            cluster_id=cluster_id,
            automatic=automatic,
            configuration=configuration,
            creation_policy=creation_policy,
            id=id,
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

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        agency: builtins.str,
        bucket: builtins.str,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#agency CssSnapshotConfigurationV1#agency}.
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#bucket CssSnapshotConfigurationV1#bucket}.
        :param kms_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#kms_id CssSnapshotConfigurationV1#kms_id}.
        '''
        value = CssSnapshotConfigurationV1Configuration(
            agency=agency, bucket=bucket, kms_id=kms_id
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putCreationPolicy")
    def put_creation_policy(
        self,
        *,
        enable: typing.Union[builtins.bool, cdktf.IResolvable],
        keepday: jsii.Number,
        period: builtins.str,
        prefix: builtins.str,
        delete_auto: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#enable CssSnapshotConfigurationV1#enable}.
        :param keepday: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#keepday CssSnapshotConfigurationV1#keepday}.
        :param period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#period CssSnapshotConfigurationV1#period}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#prefix CssSnapshotConfigurationV1#prefix}.
        :param delete_auto: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#delete_auto CssSnapshotConfigurationV1#delete_auto}.
        '''
        value = CssSnapshotConfigurationV1CreationPolicy(
            enable=enable,
            keepday=keepday,
            period=period,
            prefix=prefix,
            delete_auto=delete_auto,
        )

        return typing.cast(None, jsii.invoke(self, "putCreationPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#create CssSnapshotConfigurationV1#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#update CssSnapshotConfigurationV1#update}.
        '''
        value = CssSnapshotConfigurationV1Timeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutomatic")
    def reset_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatic", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetCreationPolicy")
    def reset_creation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basePath"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "CssSnapshotConfigurationV1ConfigurationOutputReference":
        return typing.cast("CssSnapshotConfigurationV1ConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(
        self,
    ) -> "CssSnapshotConfigurationV1CreationPolicyOutputReference":
        return typing.cast("CssSnapshotConfigurationV1CreationPolicyOutputReference", jsii.get(self, "creationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CssSnapshotConfigurationV1TimeoutsOutputReference":
        return typing.cast("CssSnapshotConfigurationV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="automaticInput")
    def automatic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "automaticInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(
        self,
    ) -> typing.Optional["CssSnapshotConfigurationV1Configuration"]:
        return typing.cast(typing.Optional["CssSnapshotConfigurationV1Configuration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="creationPolicyInput")
    def creation_policy_input(
        self,
    ) -> typing.Optional["CssSnapshotConfigurationV1CreationPolicy"]:
        return typing.cast(typing.Optional["CssSnapshotConfigurationV1CreationPolicy"], jsii.get(self, "creationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="automatic")
    def automatic(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "automatic"))

    @automatic.setter
    def automatic(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automatic", value)

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "automatic": "automatic",
        "configuration": "configuration",
        "creation_policy": "creationPolicy",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class CssSnapshotConfigurationV1Config(cdktf.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        automatic: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        configuration: typing.Optional[typing.Union["CssSnapshotConfigurationV1Configuration", typing.Dict[str, typing.Any]]] = None,
        creation_policy: typing.Optional[typing.Union["CssSnapshotConfigurationV1CreationPolicy", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#cluster_id CssSnapshotConfigurationV1#cluster_id}.
        :param automatic: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#automatic CssSnapshotConfigurationV1#automatic}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#configuration CssSnapshotConfigurationV1#configuration}
        :param creation_policy: creation_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#creation_policy CssSnapshotConfigurationV1#creation_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#id CssSnapshotConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#timeouts CssSnapshotConfigurationV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = CssSnapshotConfigurationV1Configuration(**configuration)
        if isinstance(creation_policy, dict):
            creation_policy = CssSnapshotConfigurationV1CreationPolicy(**creation_policy)
        if isinstance(timeouts, dict):
            timeouts = CssSnapshotConfigurationV1Timeouts(**timeouts)
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
                cluster_id: builtins.str,
                automatic: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                configuration: typing.Optional[typing.Union["CssSnapshotConfigurationV1Configuration", typing.Dict[str, typing.Any]]] = None,
                creation_policy: typing.Optional[typing.Union["CssSnapshotConfigurationV1CreationPolicy", typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["CssSnapshotConfigurationV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument creation_policy", value=creation_policy, expected_type=type_hints["creation_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
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
        if automatic is not None:
            self._values["automatic"] = automatic
        if configuration is not None:
            self._values["configuration"] = configuration
        if creation_policy is not None:
            self._values["creation_policy"] = creation_policy
        if id is not None:
            self._values["id"] = id
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
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#cluster_id CssSnapshotConfigurationV1#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#automatic CssSnapshotConfigurationV1#automatic}.'''
        result = self._values.get("automatic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional["CssSnapshotConfigurationV1Configuration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#configuration CssSnapshotConfigurationV1#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["CssSnapshotConfigurationV1Configuration"], result)

    @builtins.property
    def creation_policy(
        self,
    ) -> typing.Optional["CssSnapshotConfigurationV1CreationPolicy"]:
        '''creation_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#creation_policy CssSnapshotConfigurationV1#creation_policy}
        '''
        result = self._values.get("creation_policy")
        return typing.cast(typing.Optional["CssSnapshotConfigurationV1CreationPolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#id CssSnapshotConfigurationV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CssSnapshotConfigurationV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#timeouts CssSnapshotConfigurationV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CssSnapshotConfigurationV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssSnapshotConfigurationV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1Configuration",
    jsii_struct_bases=[],
    name_mapping={"agency": "agency", "bucket": "bucket", "kms_id": "kmsId"},
)
class CssSnapshotConfigurationV1Configuration:
    def __init__(
        self,
        *,
        agency: builtins.str,
        bucket: builtins.str,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#agency CssSnapshotConfigurationV1#agency}.
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#bucket CssSnapshotConfigurationV1#bucket}.
        :param kms_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#kms_id CssSnapshotConfigurationV1#kms_id}.
        '''
        if __debug__:
            def stub(
                *,
                agency: builtins.str,
                bucket: builtins.str,
                kms_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument agency", value=agency, expected_type=type_hints["agency"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "agency": agency,
            "bucket": bucket,
        }
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def agency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#agency CssSnapshotConfigurationV1#agency}.'''
        result = self._values.get("agency")
        assert result is not None, "Required property 'agency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#bucket CssSnapshotConfigurationV1#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#kms_id CssSnapshotConfigurationV1#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssSnapshotConfigurationV1Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssSnapshotConfigurationV1ConfigurationOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1ConfigurationOutputReference",
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

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="agencyInput")
    def agency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="agency")
    def agency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agency"))

    @agency.setter
    def agency(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agency", value)

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CssSnapshotConfigurationV1Configuration]:
        return typing.cast(typing.Optional[CssSnapshotConfigurationV1Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CssSnapshotConfigurationV1Configuration],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[CssSnapshotConfigurationV1Configuration],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1CreationPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "keepday": "keepday",
        "period": "period",
        "prefix": "prefix",
        "delete_auto": "deleteAuto",
    },
)
class CssSnapshotConfigurationV1CreationPolicy:
    def __init__(
        self,
        *,
        enable: typing.Union[builtins.bool, cdktf.IResolvable],
        keepday: jsii.Number,
        period: builtins.str,
        prefix: builtins.str,
        delete_auto: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#enable CssSnapshotConfigurationV1#enable}.
        :param keepday: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#keepday CssSnapshotConfigurationV1#keepday}.
        :param period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#period CssSnapshotConfigurationV1#period}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#prefix CssSnapshotConfigurationV1#prefix}.
        :param delete_auto: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#delete_auto CssSnapshotConfigurationV1#delete_auto}.
        '''
        if __debug__:
            def stub(
                *,
                enable: typing.Union[builtins.bool, cdktf.IResolvable],
                keepday: jsii.Number,
                period: builtins.str,
                prefix: builtins.str,
                delete_auto: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument keepday", value=keepday, expected_type=type_hints["keepday"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument delete_auto", value=delete_auto, expected_type=type_hints["delete_auto"])
        self._values: typing.Dict[str, typing.Any] = {
            "enable": enable,
            "keepday": keepday,
            "period": period,
            "prefix": prefix,
        }
        if delete_auto is not None:
            self._values["delete_auto"] = delete_auto

    @builtins.property
    def enable(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#enable CssSnapshotConfigurationV1#enable}.'''
        result = self._values.get("enable")
        assert result is not None, "Required property 'enable' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def keepday(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#keepday CssSnapshotConfigurationV1#keepday}.'''
        result = self._values.get("keepday")
        assert result is not None, "Required property 'keepday' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def period(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#period CssSnapshotConfigurationV1#period}.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#prefix CssSnapshotConfigurationV1#prefix}.'''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_auto(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#delete_auto CssSnapshotConfigurationV1#delete_auto}.'''
        result = self._values.get("delete_auto")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssSnapshotConfigurationV1CreationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssSnapshotConfigurationV1CreationPolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1CreationPolicyOutputReference",
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

    @jsii.member(jsii_name="resetDeleteAuto")
    def reset_delete_auto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAuto", []))

    @builtins.property
    @jsii.member(jsii_name="deleteAutoInput")
    def delete_auto_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "deleteAutoInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="keepdayInput")
    def keepday_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepdayInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAuto")
    def delete_auto(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "deleteAuto"))

    @delete_auto.setter
    def delete_auto(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAuto", value)

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value)

    @builtins.property
    @jsii.member(jsii_name="keepday")
    def keepday(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepday"))

    @keepday.setter
    def keepday(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepday", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CssSnapshotConfigurationV1CreationPolicy]:
        return typing.cast(typing.Optional[CssSnapshotConfigurationV1CreationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CssSnapshotConfigurationV1CreationPolicy],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[CssSnapshotConfigurationV1CreationPolicy],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class CssSnapshotConfigurationV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#create CssSnapshotConfigurationV1#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#update CssSnapshotConfigurationV1#update}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                update: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#create CssSnapshotConfigurationV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/css_snapshot_configuration_v1#update CssSnapshotConfigurationV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssSnapshotConfigurationV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssSnapshotConfigurationV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssSnapshotConfigurationV1.CssSnapshotConfigurationV1TimeoutsOutputReference",
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

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

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
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CssSnapshotConfigurationV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CssSnapshotConfigurationV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CssSnapshotConfigurationV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CssSnapshotConfigurationV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CssSnapshotConfigurationV1",
    "CssSnapshotConfigurationV1Config",
    "CssSnapshotConfigurationV1Configuration",
    "CssSnapshotConfigurationV1ConfigurationOutputReference",
    "CssSnapshotConfigurationV1CreationPolicy",
    "CssSnapshotConfigurationV1CreationPolicyOutputReference",
    "CssSnapshotConfigurationV1Timeouts",
    "CssSnapshotConfigurationV1TimeoutsOutputReference",
]

publication.publish()
