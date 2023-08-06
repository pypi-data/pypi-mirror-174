'''
# `opentelekomcloud_cbr_policy_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_cbr_policy_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3).
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


class CbrPolicyV3(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrPolicyV3.CbrPolicyV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3 opentelekomcloud_cbr_policy_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        operation_type: builtins.str,
        trigger_pattern: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_definition: typing.Optional[typing.Union["CbrPolicyV3OperationDefinition", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3 opentelekomcloud_cbr_policy_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#name CbrPolicyV3#name}.
        :param operation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_type CbrPolicyV3#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#trigger_pattern CbrPolicyV3#trigger_pattern}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#enabled CbrPolicyV3#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#id CbrPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_definition: operation_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_definition CbrPolicyV3#operation_definition}
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
                name: builtins.str,
                operation_type: builtins.str,
                trigger_pattern: typing.Sequence[builtins.str],
                enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                operation_definition: typing.Optional[typing.Union["CbrPolicyV3OperationDefinition", typing.Dict[str, typing.Any]]] = None,
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
        config = CbrPolicyV3Config(
            name=name,
            operation_type=operation_type,
            trigger_pattern=trigger_pattern,
            enabled=enabled,
            id=id,
            operation_definition=operation_definition,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putOperationDefinition")
    def put_operation_definition(
        self,
        *,
        timezone: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param timezone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#timezone CbrPolicyV3#timezone}.
        :param day_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#day_backups CbrPolicyV3#day_backups}.
        :param max_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#max_backups CbrPolicyV3#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#month_backups CbrPolicyV3#month_backups}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#retention_duration_days CbrPolicyV3#retention_duration_days}.
        :param week_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#week_backups CbrPolicyV3#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#year_backups CbrPolicyV3#year_backups}.
        '''
        value = CbrPolicyV3OperationDefinition(
            timezone=timezone,
            day_backups=day_backups,
            max_backups=max_backups,
            month_backups=month_backups,
            retention_duration_days=retention_duration_days,
            week_backups=week_backups,
            year_backups=year_backups,
        )

        return typing.cast(None, jsii.invoke(self, "putOperationDefinition", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperationDefinition")
    def reset_operation_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationDefinition", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="operationDefinition")
    def operation_definition(self) -> "CbrPolicyV3OperationDefinitionOutputReference":
        return typing.cast("CbrPolicyV3OperationDefinitionOutputReference", jsii.get(self, "operationDefinition"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationDefinitionInput")
    def operation_definition_input(
        self,
    ) -> typing.Optional["CbrPolicyV3OperationDefinition"]:
        return typing.cast(typing.Optional["CbrPolicyV3OperationDefinition"], jsii.get(self, "operationDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="operationTypeInput")
    def operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerPatternInput")
    def trigger_pattern_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

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
    @jsii.member(jsii_name="operationType")
    def operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationType"))

    @operation_type.setter
    def operation_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationType", value)

    @builtins.property
    @jsii.member(jsii_name="triggerPattern")
    def trigger_pattern(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerPattern"))

    @trigger_pattern.setter
    def trigger_pattern(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerPattern", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrPolicyV3.CbrPolicyV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "operation_type": "operationType",
        "trigger_pattern": "triggerPattern",
        "enabled": "enabled",
        "id": "id",
        "operation_definition": "operationDefinition",
    },
)
class CbrPolicyV3Config(cdktf.TerraformMetaArguments):
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
        name: builtins.str,
        operation_type: builtins.str,
        trigger_pattern: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_definition: typing.Optional[typing.Union["CbrPolicyV3OperationDefinition", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#name CbrPolicyV3#name}.
        :param operation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_type CbrPolicyV3#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#trigger_pattern CbrPolicyV3#trigger_pattern}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#enabled CbrPolicyV3#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#id CbrPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_definition: operation_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_definition CbrPolicyV3#operation_definition}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(operation_definition, dict):
            operation_definition = CbrPolicyV3OperationDefinition(**operation_definition)
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
                name: builtins.str,
                operation_type: builtins.str,
                trigger_pattern: typing.Sequence[builtins.str],
                enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                operation_definition: typing.Optional[typing.Union["CbrPolicyV3OperationDefinition", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operation_type", value=operation_type, expected_type=type_hints["operation_type"])
            check_type(argname="argument trigger_pattern", value=trigger_pattern, expected_type=type_hints["trigger_pattern"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument operation_definition", value=operation_definition, expected_type=type_hints["operation_definition"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "operation_type": operation_type,
            "trigger_pattern": trigger_pattern,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if operation_definition is not None:
            self._values["operation_definition"] = operation_definition

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#name CbrPolicyV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_type CbrPolicyV3#operation_type}.'''
        result = self._values.get("operation_type")
        assert result is not None, "Required property 'operation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_pattern(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#trigger_pattern CbrPolicyV3#trigger_pattern}.'''
        result = self._values.get("trigger_pattern")
        assert result is not None, "Required property 'trigger_pattern' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#enabled CbrPolicyV3#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#id CbrPolicyV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_definition(self) -> typing.Optional["CbrPolicyV3OperationDefinition"]:
        '''operation_definition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#operation_definition CbrPolicyV3#operation_definition}
        '''
        result = self._values.get("operation_definition")
        return typing.cast(typing.Optional["CbrPolicyV3OperationDefinition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrPolicyV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrPolicyV3.CbrPolicyV3OperationDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "timezone": "timezone",
        "day_backups": "dayBackups",
        "max_backups": "maxBackups",
        "month_backups": "monthBackups",
        "retention_duration_days": "retentionDurationDays",
        "week_backups": "weekBackups",
        "year_backups": "yearBackups",
    },
)
class CbrPolicyV3OperationDefinition:
    def __init__(
        self,
        *,
        timezone: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param timezone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#timezone CbrPolicyV3#timezone}.
        :param day_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#day_backups CbrPolicyV3#day_backups}.
        :param max_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#max_backups CbrPolicyV3#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#month_backups CbrPolicyV3#month_backups}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#retention_duration_days CbrPolicyV3#retention_duration_days}.
        :param week_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#week_backups CbrPolicyV3#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#year_backups CbrPolicyV3#year_backups}.
        '''
        if __debug__:
            def stub(
                *,
                timezone: builtins.str,
                day_backups: typing.Optional[jsii.Number] = None,
                max_backups: typing.Optional[jsii.Number] = None,
                month_backups: typing.Optional[jsii.Number] = None,
                retention_duration_days: typing.Optional[jsii.Number] = None,
                week_backups: typing.Optional[jsii.Number] = None,
                year_backups: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument day_backups", value=day_backups, expected_type=type_hints["day_backups"])
            check_type(argname="argument max_backups", value=max_backups, expected_type=type_hints["max_backups"])
            check_type(argname="argument month_backups", value=month_backups, expected_type=type_hints["month_backups"])
            check_type(argname="argument retention_duration_days", value=retention_duration_days, expected_type=type_hints["retention_duration_days"])
            check_type(argname="argument week_backups", value=week_backups, expected_type=type_hints["week_backups"])
            check_type(argname="argument year_backups", value=year_backups, expected_type=type_hints["year_backups"])
        self._values: typing.Dict[str, typing.Any] = {
            "timezone": timezone,
        }
        if day_backups is not None:
            self._values["day_backups"] = day_backups
        if max_backups is not None:
            self._values["max_backups"] = max_backups
        if month_backups is not None:
            self._values["month_backups"] = month_backups
        if retention_duration_days is not None:
            self._values["retention_duration_days"] = retention_duration_days
        if week_backups is not None:
            self._values["week_backups"] = week_backups
        if year_backups is not None:
            self._values["year_backups"] = year_backups

    @builtins.property
    def timezone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#timezone CbrPolicyV3#timezone}.'''
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def day_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#day_backups CbrPolicyV3#day_backups}.'''
        result = self._values.get("day_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#max_backups CbrPolicyV3#max_backups}.'''
        result = self._values.get("max_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#month_backups CbrPolicyV3#month_backups}.'''
        result = self._values.get("month_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_duration_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#retention_duration_days CbrPolicyV3#retention_duration_days}.'''
        result = self._values.get("retention_duration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#week_backups CbrPolicyV3#week_backups}.'''
        result = self._values.get("week_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_policy_v3#year_backups CbrPolicyV3#year_backups}.'''
        result = self._values.get("year_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrPolicyV3OperationDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrPolicyV3OperationDefinitionOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrPolicyV3.CbrPolicyV3OperationDefinitionOutputReference",
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

    @jsii.member(jsii_name="resetDayBackups")
    def reset_day_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayBackups", []))

    @jsii.member(jsii_name="resetMaxBackups")
    def reset_max_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackups", []))

    @jsii.member(jsii_name="resetMonthBackups")
    def reset_month_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthBackups", []))

    @jsii.member(jsii_name="resetRetentionDurationDays")
    def reset_retention_duration_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDurationDays", []))

    @jsii.member(jsii_name="resetWeekBackups")
    def reset_week_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekBackups", []))

    @jsii.member(jsii_name="resetYearBackups")
    def reset_year_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYearBackups", []))

    @builtins.property
    @jsii.member(jsii_name="dayBackupsInput")
    def day_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackupsInput")
    def max_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="monthBackupsInput")
    def month_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationDaysInput")
    def retention_duration_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDurationDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weekBackupsInput")
    def week_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="yearBackupsInput")
    def year_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="dayBackups")
    def day_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayBackups"))

    @day_backups.setter
    def day_backups(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayBackups", value)

    @builtins.property
    @jsii.member(jsii_name="maxBackups")
    def max_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBackups"))

    @max_backups.setter
    def max_backups(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackups", value)

    @builtins.property
    @jsii.member(jsii_name="monthBackups")
    def month_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthBackups"))

    @month_backups.setter
    def month_backups(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthBackups", value)

    @builtins.property
    @jsii.member(jsii_name="retentionDurationDays")
    def retention_duration_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDurationDays"))

    @retention_duration_days.setter
    def retention_duration_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDurationDays", value)

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value)

    @builtins.property
    @jsii.member(jsii_name="weekBackups")
    def week_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekBackups"))

    @week_backups.setter
    def week_backups(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekBackups", value)

    @builtins.property
    @jsii.member(jsii_name="yearBackups")
    def year_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "yearBackups"))

    @year_backups.setter
    def year_backups(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "yearBackups", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CbrPolicyV3OperationDefinition]:
        return typing.cast(typing.Optional[CbrPolicyV3OperationDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CbrPolicyV3OperationDefinition],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[CbrPolicyV3OperationDefinition]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CbrPolicyV3",
    "CbrPolicyV3Config",
    "CbrPolicyV3OperationDefinition",
    "CbrPolicyV3OperationDefinitionOutputReference",
]

publication.publish()
