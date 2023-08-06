'''
# `opentelekomcloud_cbr_vault_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_cbr_vault_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3).
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


class CbrVaultV3(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3 opentelekomcloud_cbr_vault_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        billing: typing.Union["CbrVaultV3Billing", typing.Dict[str, typing.Any]],
        name: builtins.str,
        auto_bind: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_expand: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        backup_policy_id: typing.Optional[builtins.str] = None,
        bind_rules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        resource: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3 opentelekomcloud_cbr_vault_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing: billing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#billing CbrVaultV3#billing}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#name CbrVaultV3#name}.
        :param auto_bind: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.
        :param auto_expand: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.
        :param backup_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.
        :param bind_rules: bind_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#description CbrVaultV3#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param resource: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#resource CbrVaultV3#resource}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#tags CbrVaultV3#tags}.
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
                billing: typing.Union["CbrVaultV3Billing", typing.Dict[str, typing.Any]],
                name: builtins.str,
                auto_bind: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                auto_expand: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                backup_policy_id: typing.Optional[builtins.str] = None,
                bind_rules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[str, typing.Any]]]]] = None,
                description: typing.Optional[builtins.str] = None,
                enterprise_project_id: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                resource: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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
        config = CbrVaultV3Config(
            billing=billing,
            name=name,
            auto_bind=auto_bind,
            auto_expand=auto_expand,
            backup_policy_id=backup_policy_id,
            bind_rules=bind_rules,
            description=description,
            enterprise_project_id=enterprise_project_id,
            id=id,
            resource=resource,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putBilling")
    def put_billing(
        self,
        *,
        object_type: builtins.str,
        protect_type: builtins.str,
        size: jsii.Number,
        charging_mode: typing.Optional[builtins.str] = None,
        cloud_type: typing.Optional[builtins.str] = None,
        consistent_level: typing.Optional[builtins.str] = None,
        console_url: typing.Optional[builtins.str] = None,
        extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_auto_pay: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        is_auto_renew: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        period_num: typing.Optional[jsii.Number] = None,
        period_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#object_type CbrVaultV3#object_type}.
        :param protect_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#size CbrVaultV3#size}.
        :param charging_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.
        :param cloud_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.
        :param consistent_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.
        :param console_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#console_url CbrVaultV3#console_url}.
        :param extra_info: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.
        :param is_auto_pay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.
        :param is_auto_renew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.
        :param period_num: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_num CbrVaultV3#period_num}.
        :param period_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_type CbrVaultV3#period_type}.
        '''
        value = CbrVaultV3Billing(
            object_type=object_type,
            protect_type=protect_type,
            size=size,
            charging_mode=charging_mode,
            cloud_type=cloud_type,
            consistent_level=consistent_level,
            console_url=console_url,
            extra_info=extra_info,
            is_auto_pay=is_auto_pay,
            is_auto_renew=is_auto_renew,
            period_num=period_num,
            period_type=period_type,
        )

        return typing.cast(None, jsii.invoke(self, "putBilling", [value]))

    @jsii.member(jsii_name="putBindRules")
    def put_bind_rules(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBindRules", [value]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResource", [value]))

    @jsii.member(jsii_name="resetAutoBind")
    def reset_auto_bind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoBind", []))

    @jsii.member(jsii_name="resetAutoExpand")
    def reset_auto_expand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoExpand", []))

    @jsii.member(jsii_name="resetBackupPolicyId")
    def reset_backup_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupPolicyId", []))

    @jsii.member(jsii_name="resetBindRules")
    def reset_bind_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindRules", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnterpriseProjectId")
    def reset_enterprise_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseProjectId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="billing")
    def billing(self) -> "CbrVaultV3BillingOutputReference":
        return typing.cast("CbrVaultV3BillingOutputReference", jsii.get(self, "billing"))

    @builtins.property
    @jsii.member(jsii_name="bindRules")
    def bind_rules(self) -> "CbrVaultV3BindRulesList":
        return typing.cast("CbrVaultV3BindRulesList", jsii.get(self, "bindRules"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "CbrVaultV3ResourceList":
        return typing.cast("CbrVaultV3ResourceList", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="autoBindInput")
    def auto_bind_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "autoBindInput"))

    @builtins.property
    @jsii.member(jsii_name="autoExpandInput")
    def auto_expand_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "autoExpandInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyIdInput")
    def backup_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="billingInput")
    def billing_input(self) -> typing.Optional["CbrVaultV3Billing"]:
        return typing.cast(typing.Optional["CbrVaultV3Billing"], jsii.get(self, "billingInput"))

    @builtins.property
    @jsii.member(jsii_name="bindRulesInput")
    def bind_rules_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3BindRules"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3BindRules"]]], jsii.get(self, "bindRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectIdInput")
    def enterprise_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3Resource"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3Resource"]]], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoBind")
    def auto_bind(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "autoBind"))

    @auto_bind.setter
    def auto_bind(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoBind", value)

    @builtins.property
    @jsii.member(jsii_name="autoExpand")
    def auto_expand(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "autoExpand"))

    @auto_expand.setter
    def auto_expand(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoExpand", value)

    @builtins.property
    @jsii.member(jsii_name="backupPolicyId")
    def backup_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPolicyId"))

    @backup_policy_id.setter
    def backup_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicyId", value)

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
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @enterprise_project_id.setter
    def enterprise_project_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseProjectId", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Billing",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "protect_type": "protectType",
        "size": "size",
        "charging_mode": "chargingMode",
        "cloud_type": "cloudType",
        "consistent_level": "consistentLevel",
        "console_url": "consoleUrl",
        "extra_info": "extraInfo",
        "is_auto_pay": "isAutoPay",
        "is_auto_renew": "isAutoRenew",
        "period_num": "periodNum",
        "period_type": "periodType",
    },
)
class CbrVaultV3Billing:
    def __init__(
        self,
        *,
        object_type: builtins.str,
        protect_type: builtins.str,
        size: jsii.Number,
        charging_mode: typing.Optional[builtins.str] = None,
        cloud_type: typing.Optional[builtins.str] = None,
        consistent_level: typing.Optional[builtins.str] = None,
        console_url: typing.Optional[builtins.str] = None,
        extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_auto_pay: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        is_auto_renew: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        period_num: typing.Optional[jsii.Number] = None,
        period_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#object_type CbrVaultV3#object_type}.
        :param protect_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#size CbrVaultV3#size}.
        :param charging_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.
        :param cloud_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.
        :param consistent_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.
        :param console_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#console_url CbrVaultV3#console_url}.
        :param extra_info: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.
        :param is_auto_pay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.
        :param is_auto_renew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.
        :param period_num: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_num CbrVaultV3#period_num}.
        :param period_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_type CbrVaultV3#period_type}.
        '''
        if __debug__:
            def stub(
                *,
                object_type: builtins.str,
                protect_type: builtins.str,
                size: jsii.Number,
                charging_mode: typing.Optional[builtins.str] = None,
                cloud_type: typing.Optional[builtins.str] = None,
                consistent_level: typing.Optional[builtins.str] = None,
                console_url: typing.Optional[builtins.str] = None,
                extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                is_auto_pay: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                is_auto_renew: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                period_num: typing.Optional[jsii.Number] = None,
                period_type: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument protect_type", value=protect_type, expected_type=type_hints["protect_type"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument charging_mode", value=charging_mode, expected_type=type_hints["charging_mode"])
            check_type(argname="argument cloud_type", value=cloud_type, expected_type=type_hints["cloud_type"])
            check_type(argname="argument consistent_level", value=consistent_level, expected_type=type_hints["consistent_level"])
            check_type(argname="argument console_url", value=console_url, expected_type=type_hints["console_url"])
            check_type(argname="argument extra_info", value=extra_info, expected_type=type_hints["extra_info"])
            check_type(argname="argument is_auto_pay", value=is_auto_pay, expected_type=type_hints["is_auto_pay"])
            check_type(argname="argument is_auto_renew", value=is_auto_renew, expected_type=type_hints["is_auto_renew"])
            check_type(argname="argument period_num", value=period_num, expected_type=type_hints["period_num"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "object_type": object_type,
            "protect_type": protect_type,
            "size": size,
        }
        if charging_mode is not None:
            self._values["charging_mode"] = charging_mode
        if cloud_type is not None:
            self._values["cloud_type"] = cloud_type
        if consistent_level is not None:
            self._values["consistent_level"] = consistent_level
        if console_url is not None:
            self._values["console_url"] = console_url
        if extra_info is not None:
            self._values["extra_info"] = extra_info
        if is_auto_pay is not None:
            self._values["is_auto_pay"] = is_auto_pay
        if is_auto_renew is not None:
            self._values["is_auto_renew"] = is_auto_renew
        if period_num is not None:
            self._values["period_num"] = period_num
        if period_type is not None:
            self._values["period_type"] = period_type

    @builtins.property
    def object_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#object_type CbrVaultV3#object_type}.'''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.'''
        result = self._values.get("protect_type")
        assert result is not None, "Required property 'protect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#size CbrVaultV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def charging_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.'''
        result = self._values.get("charging_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.'''
        result = self._values.get("cloud_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consistent_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.'''
        result = self._values.get("consistent_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def console_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#console_url CbrVaultV3#console_url}.'''
        result = self._values.get("console_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_info(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.'''
        result = self._values.get("extra_info")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.'''
        result = self._values.get("is_auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def is_auto_renew(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.'''
        result = self._values.get("is_auto_renew")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def period_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_num CbrVaultV3#period_num}.'''
        result = self._values.get("period_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#period_type CbrVaultV3#period_type}.'''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Billing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3BillingOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BillingOutputReference",
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

    @jsii.member(jsii_name="resetChargingMode")
    def reset_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChargingMode", []))

    @jsii.member(jsii_name="resetCloudType")
    def reset_cloud_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudType", []))

    @jsii.member(jsii_name="resetConsistentLevel")
    def reset_consistent_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsistentLevel", []))

    @jsii.member(jsii_name="resetConsoleUrl")
    def reset_console_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsoleUrl", []))

    @jsii.member(jsii_name="resetExtraInfo")
    def reset_extra_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraInfo", []))

    @jsii.member(jsii_name="resetIsAutoPay")
    def reset_is_auto_pay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsAutoPay", []))

    @jsii.member(jsii_name="resetIsAutoRenew")
    def reset_is_auto_renew(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsAutoRenew", []))

    @jsii.member(jsii_name="resetPeriodNum")
    def reset_period_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodNum", []))

    @jsii.member(jsii_name="resetPeriodType")
    def reset_period_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodType", []))

    @builtins.property
    @jsii.member(jsii_name="allocated")
    def allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocated"))

    @builtins.property
    @jsii.member(jsii_name="frozenScene")
    def frozen_scene(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frozenScene"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @builtins.property
    @jsii.member(jsii_name="specCode")
    def spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specCode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageUnit")
    def storage_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUnit"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="chargingModeInput")
    def charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudTypeInput")
    def cloud_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="consistentLevelInput")
    def consistent_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consistentLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="consoleUrlInput")
    def console_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consoleUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="extraInfoInput")
    def extra_info_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="isAutoPayInput")
    def is_auto_pay_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "isAutoPayInput"))

    @builtins.property
    @jsii.member(jsii_name="isAutoRenewInput")
    def is_auto_renew_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "isAutoRenewInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeInput")
    def object_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="periodNumInput")
    def period_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodNumInput"))

    @builtins.property
    @jsii.member(jsii_name="periodTypeInput")
    def period_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="protectTypeInput")
    def protect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargingMode")
    def charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargingMode"))

    @charging_mode.setter
    def charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargingMode", value)

    @builtins.property
    @jsii.member(jsii_name="cloudType")
    def cloud_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudType"))

    @cloud_type.setter
    def cloud_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudType", value)

    @builtins.property
    @jsii.member(jsii_name="consistentLevel")
    def consistent_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consistentLevel"))

    @consistent_level.setter
    def consistent_level(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consistentLevel", value)

    @builtins.property
    @jsii.member(jsii_name="consoleUrl")
    def console_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consoleUrl"))

    @console_url.setter
    def console_url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consoleUrl", value)

    @builtins.property
    @jsii.member(jsii_name="extraInfo")
    def extra_info(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraInfo"))

    @extra_info.setter
    def extra_info(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraInfo", value)

    @builtins.property
    @jsii.member(jsii_name="isAutoPay")
    def is_auto_pay(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "isAutoPay"))

    @is_auto_pay.setter
    def is_auto_pay(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAutoPay", value)

    @builtins.property
    @jsii.member(jsii_name="isAutoRenew")
    def is_auto_renew(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "isAutoRenew"))

    @is_auto_renew.setter
    def is_auto_renew(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAutoRenew", value)

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value)

    @builtins.property
    @jsii.member(jsii_name="periodNum")
    def period_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodNum"))

    @period_num.setter
    def period_num(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodNum", value)

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodType", value)

    @builtins.property
    @jsii.member(jsii_name="protectType")
    def protect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectType"))

    @protect_type.setter
    def protect_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectType", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CbrVaultV3Billing]:
        return typing.cast(typing.Optional[CbrVaultV3Billing], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CbrVaultV3Billing]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CbrVaultV3Billing]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRules",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CbrVaultV3BindRules:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#key CbrVaultV3#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#value CbrVaultV3#value}.
        '''
        if __debug__:
            def stub(*, key: builtins.str, value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#key CbrVaultV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#value CbrVaultV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3BindRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3BindRulesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRulesList",
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
    def get(self, index: jsii.Number) -> "CbrVaultV3BindRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CbrVaultV3BindRulesOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CbrVaultV3BindRulesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRulesOutputReference",
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
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CbrVaultV3BindRules, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CbrVaultV3BindRules, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CbrVaultV3BindRules, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CbrVaultV3BindRules, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing": "billing",
        "name": "name",
        "auto_bind": "autoBind",
        "auto_expand": "autoExpand",
        "backup_policy_id": "backupPolicyId",
        "bind_rules": "bindRules",
        "description": "description",
        "enterprise_project_id": "enterpriseProjectId",
        "id": "id",
        "resource": "resource",
        "tags": "tags",
    },
)
class CbrVaultV3Config(cdktf.TerraformMetaArguments):
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
        billing: typing.Union[CbrVaultV3Billing, typing.Dict[str, typing.Any]],
        name: builtins.str,
        auto_bind: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_expand: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        backup_policy_id: typing.Optional[builtins.str] = None,
        bind_rules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        resource: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing: billing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#billing CbrVaultV3#billing}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#name CbrVaultV3#name}.
        :param auto_bind: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.
        :param auto_expand: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.
        :param backup_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.
        :param bind_rules: bind_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#description CbrVaultV3#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param resource: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#resource CbrVaultV3#resource}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#tags CbrVaultV3#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(billing, dict):
            billing = CbrVaultV3Billing(**billing)
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
                billing: typing.Union[CbrVaultV3Billing, typing.Dict[str, typing.Any]],
                name: builtins.str,
                auto_bind: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                auto_expand: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                backup_policy_id: typing.Optional[builtins.str] = None,
                bind_rules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[str, typing.Any]]]]] = None,
                description: typing.Optional[builtins.str] = None,
                enterprise_project_id: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                resource: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[str, typing.Any]]]]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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
            check_type(argname="argument billing", value=billing, expected_type=type_hints["billing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_bind", value=auto_bind, expected_type=type_hints["auto_bind"])
            check_type(argname="argument auto_expand", value=auto_expand, expected_type=type_hints["auto_expand"])
            check_type(argname="argument backup_policy_id", value=backup_policy_id, expected_type=type_hints["backup_policy_id"])
            check_type(argname="argument bind_rules", value=bind_rules, expected_type=type_hints["bind_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enterprise_project_id", value=enterprise_project_id, expected_type=type_hints["enterprise_project_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "billing": billing,
            "name": name,
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
        if auto_bind is not None:
            self._values["auto_bind"] = auto_bind
        if auto_expand is not None:
            self._values["auto_expand"] = auto_expand
        if backup_policy_id is not None:
            self._values["backup_policy_id"] = backup_policy_id
        if bind_rules is not None:
            self._values["bind_rules"] = bind_rules
        if description is not None:
            self._values["description"] = description
        if enterprise_project_id is not None:
            self._values["enterprise_project_id"] = enterprise_project_id
        if id is not None:
            self._values["id"] = id
        if resource is not None:
            self._values["resource"] = resource
        if tags is not None:
            self._values["tags"] = tags

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
    def billing(self) -> CbrVaultV3Billing:
        '''billing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#billing CbrVaultV3#billing}
        '''
        result = self._values.get("billing")
        assert result is not None, "Required property 'billing' is missing"
        return typing.cast(CbrVaultV3Billing, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#name CbrVaultV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_bind(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.'''
        result = self._values.get("auto_bind")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def auto_expand(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.'''
        result = self._values.get("auto_expand")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def backup_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.'''
        result = self._values.get("backup_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bind_rules(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]]:
        '''bind_rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        '''
        result = self._values.get("bind_rules")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3BindRules]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#description CbrVaultV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enterprise_project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.'''
        result = self._values.get("enterprise_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#id CbrVaultV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3Resource"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#resource CbrVaultV3#resource}.'''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CbrVaultV3Resource"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#tags CbrVaultV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Resource",
    jsii_struct_bases=[],
    name_mapping={
        "backup_count": "backupCount",
        "backup_size": "backupSize",
        "exclude_volumes": "excludeVolumes",
        "id": "id",
        "include_volumes": "includeVolumes",
        "name": "name",
        "protect_status": "protectStatus",
        "size": "size",
        "type": "type",
    },
)
class CbrVaultV3Resource:
    def __init__(
        self,
        *,
        backup_count: typing.Optional[jsii.Number] = None,
        backup_size: typing.Optional[jsii.Number] = None,
        exclude_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        include_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_count CbrVaultV3#backup_count}.
        :param backup_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_size CbrVaultV3#backup_size}.
        :param exclude_volumes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#exclude_volumes CbrVaultV3#exclude_volumes}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_volumes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#include_volumes CbrVaultV3#include_volumes}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#name CbrVaultV3#name}.
        :param protect_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#protect_status CbrVaultV3#protect_status}.
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#size CbrVaultV3#size}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#type CbrVaultV3#type}.
        '''
        if __debug__:
            def stub(
                *,
                backup_count: typing.Optional[jsii.Number] = None,
                backup_size: typing.Optional[jsii.Number] = None,
                exclude_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[builtins.str] = None,
                include_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[builtins.str] = None,
                protect_status: typing.Optional[builtins.str] = None,
                size: typing.Optional[jsii.Number] = None,
                type: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument backup_count", value=backup_count, expected_type=type_hints["backup_count"])
            check_type(argname="argument backup_size", value=backup_size, expected_type=type_hints["backup_size"])
            check_type(argname="argument exclude_volumes", value=exclude_volumes, expected_type=type_hints["exclude_volumes"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_volumes", value=include_volumes, expected_type=type_hints["include_volumes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protect_status", value=protect_status, expected_type=type_hints["protect_status"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_count is not None:
            self._values["backup_count"] = backup_count
        if backup_size is not None:
            self._values["backup_size"] = backup_size
        if exclude_volumes is not None:
            self._values["exclude_volumes"] = exclude_volumes
        if id is not None:
            self._values["id"] = id
        if include_volumes is not None:
            self._values["include_volumes"] = include_volumes
        if name is not None:
            self._values["name"] = name
        if protect_status is not None:
            self._values["protect_status"] = protect_status
        if size is not None:
            self._values["size"] = size
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def backup_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_count CbrVaultV3#backup_count}.'''
        result = self._values.get("backup_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#backup_size CbrVaultV3#backup_size}.'''
        result = self._values.get("backup_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def exclude_volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#exclude_volumes CbrVaultV3#exclude_volumes}.'''
        result = self._values.get("exclude_volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#id CbrVaultV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#include_volumes CbrVaultV3#include_volumes}.'''
        result = self._values.get("include_volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#name CbrVaultV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#protect_status CbrVaultV3#protect_status}.'''
        result = self._values.get("protect_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#size CbrVaultV3#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cbr_vault_v3#type CbrVaultV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Resource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3ResourceList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3ResourceList",
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
    def get(self, index: jsii.Number) -> "CbrVaultV3ResourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CbrVaultV3ResourceOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3Resource]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3Resource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3Resource]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CbrVaultV3Resource]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CbrVaultV3ResourceOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3ResourceOutputReference",
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

    @jsii.member(jsii_name="resetBackupCount")
    def reset_backup_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupCount", []))

    @jsii.member(jsii_name="resetBackupSize")
    def reset_backup_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupSize", []))

    @jsii.member(jsii_name="resetExcludeVolumes")
    def reset_exclude_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeVolumes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeVolumes")
    def reset_include_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeVolumes", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtectStatus")
    def reset_protect_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectStatus", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="backupCountInput")
    def backup_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupCountInput"))

    @builtins.property
    @jsii.member(jsii_name="backupSizeInput")
    def backup_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeVolumesInput")
    def exclude_volumes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeVolumesInput")
    def include_volumes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectStatusInput")
    def protect_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupCount")
    def backup_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupCount"))

    @backup_count.setter
    def backup_count(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupCount", value)

    @builtins.property
    @jsii.member(jsii_name="backupSize")
    def backup_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupSize"))

    @backup_size.setter
    def backup_size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupSize", value)

    @builtins.property
    @jsii.member(jsii_name="excludeVolumes")
    def exclude_volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeVolumes"))

    @exclude_volumes.setter
    def exclude_volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeVolumes", value)

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
    @jsii.member(jsii_name="includeVolumes")
    def include_volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeVolumes"))

    @include_volumes.setter
    def include_volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeVolumes", value)

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
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectStatus"))

    @protect_status.setter
    def protect_status(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectStatus", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CbrVaultV3Resource, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CbrVaultV3Resource, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CbrVaultV3Resource, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CbrVaultV3Resource, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CbrVaultV3",
    "CbrVaultV3Billing",
    "CbrVaultV3BillingOutputReference",
    "CbrVaultV3BindRules",
    "CbrVaultV3BindRulesList",
    "CbrVaultV3BindRulesOutputReference",
    "CbrVaultV3Config",
    "CbrVaultV3Resource",
    "CbrVaultV3ResourceList",
    "CbrVaultV3ResourceOutputReference",
]

publication.publish()
