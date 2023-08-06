'''
# `opentelekomcloud_csbs_backup_policy_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_csbs_backup_policy_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1).
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


class CsbsBackupPolicyV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1 opentelekomcloud_csbs_backup_policy_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
        scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[str, typing.Any]],
        common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1 opentelekomcloud_csbs_backup_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param resource: resource block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        :param scheduled_operation: scheduled_operation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        :param common: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
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
                resource: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
                scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[str, typing.Any]],
                common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                provider_id: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = CsbsBackupPolicyV1Config(
            name=name,
            resource=resource,
            scheduled_operation=scheduled_operation,
            common=common,
            description=description,
            id=id,
            provider_id=provider_id,
            region=region,
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

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResource", [value]))

    @jsii.member(jsii_name="putScheduledOperation")
    def put_scheduled_operation(
        self,
        *,
        operation_type: builtins.str,
        trigger_pattern: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param operation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.
        :param day_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.
        :param max_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param permanent: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.
        :param timezone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.
        :param week_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.
        '''
        value = CsbsBackupPolicyV1ScheduledOperation(
            operation_type=operation_type,
            trigger_pattern=trigger_pattern,
            day_backups=day_backups,
            description=description,
            enabled=enabled,
            max_backups=max_backups,
            month_backups=month_backups,
            name=name,
            permanent=permanent,
            retention_duration_days=retention_duration_days,
            timezone=timezone,
            week_backups=week_backups,
            year_backups=year_backups,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledOperation", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.
        '''
        value = CsbsBackupPolicyV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCommon")
    def reset_common(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommon", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProviderId")
    def reset_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "CsbsBackupPolicyV1ResourceList":
        return typing.cast("CsbsBackupPolicyV1ResourceList", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperation")
    def scheduled_operation(
        self,
    ) -> "CsbsBackupPolicyV1ScheduledOperationOutputReference":
        return typing.cast("CsbsBackupPolicyV1ScheduledOperationOutputReference", jsii.get(self, "scheduledOperation"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CsbsBackupPolicyV1TagsList":
        return typing.cast("CsbsBackupPolicyV1TagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CsbsBackupPolicyV1TimeoutsOutputReference":
        return typing.cast("CsbsBackupPolicyV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="commonInput")
    def common_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "commonInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperationInput")
    def scheduled_operation_input(
        self,
    ) -> typing.Optional["CsbsBackupPolicyV1ScheduledOperation"]:
        return typing.cast(typing.Optional["CsbsBackupPolicyV1ScheduledOperation"], jsii.get(self, "scheduledOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="common")
    def common(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "common"))

    @common.setter
    def common(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "common", value)

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
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Config",
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
        "resource": "resource",
        "scheduled_operation": "scheduledOperation",
        "common": "common",
        "description": "description",
        "id": "id",
        "provider_id": "providerId",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class CsbsBackupPolicyV1Config(cdktf.TerraformMetaArguments):
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
        resource: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
        scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[str, typing.Any]],
        common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param resource: resource block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        :param scheduled_operation: scheduled_operation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        :param common: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scheduled_operation, dict):
            scheduled_operation = CsbsBackupPolicyV1ScheduledOperation(**scheduled_operation)
        if isinstance(timeouts, dict):
            timeouts = CsbsBackupPolicyV1Timeouts(**timeouts)
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
                resource: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[str, typing.Any]]]],
                scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[str, typing.Any]],
                common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                provider_id: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument scheduled_operation", value=scheduled_operation, expected_type=type_hints["scheduled_operation"])
            check_type(argname="argument common", value=common, expected_type=type_hints["common"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "resource": resource,
            "scheduled_operation": scheduled_operation,
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
        if common is not None:
            self._values["common"] = common
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if provider_id is not None:
            self._values["provider_id"] = provider_id
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]:
        '''resource block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]], result)

    @builtins.property
    def scheduled_operation(self) -> "CsbsBackupPolicyV1ScheduledOperation":
        '''scheduled_operation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        '''
        result = self._values.get("scheduled_operation")
        assert result is not None, "Required property 'scheduled_operation' is missing"
        return typing.cast("CsbsBackupPolicyV1ScheduledOperation", result)

    @builtins.property
    def common(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.'''
        result = self._values.get("common")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.'''
        result = self._values.get("provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CsbsBackupPolicyV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CsbsBackupPolicyV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Resource",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name", "type": "type"},
)
class CsbsBackupPolicyV1Resource:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#type CsbsBackupPolicyV1#type}.
        '''
        if __debug__:
            def stub(
                *,
                id: builtins.str,
                name: builtins.str,
                type: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "name": name,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#type CsbsBackupPolicyV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Resource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1ResourceList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ResourceList",
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
    def get(self, index: jsii.Number) -> "CsbsBackupPolicyV1ResourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CsbsBackupPolicyV1ResourceOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CsbsBackupPolicyV1ResourceOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ResourceOutputReference",
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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
    ) -> typing.Optional[typing.Union[CsbsBackupPolicyV1Resource, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CsbsBackupPolicyV1Resource, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CsbsBackupPolicyV1Resource, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CsbsBackupPolicyV1Resource, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ScheduledOperation",
    jsii_struct_bases=[],
    name_mapping={
        "operation_type": "operationType",
        "trigger_pattern": "triggerPattern",
        "day_backups": "dayBackups",
        "description": "description",
        "enabled": "enabled",
        "max_backups": "maxBackups",
        "month_backups": "monthBackups",
        "name": "name",
        "permanent": "permanent",
        "retention_duration_days": "retentionDurationDays",
        "timezone": "timezone",
        "week_backups": "weekBackups",
        "year_backups": "yearBackups",
    },
)
class CsbsBackupPolicyV1ScheduledOperation:
    def __init__(
        self,
        *,
        operation_type: builtins.str,
        trigger_pattern: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param operation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.
        :param day_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.
        :param max_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param permanent: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.
        :param timezone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.
        :param week_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.
        '''
        if __debug__:
            def stub(
                *,
                operation_type: builtins.str,
                trigger_pattern: builtins.str,
                day_backups: typing.Optional[jsii.Number] = None,
                description: typing.Optional[builtins.str] = None,
                enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                max_backups: typing.Optional[jsii.Number] = None,
                month_backups: typing.Optional[jsii.Number] = None,
                name: typing.Optional[builtins.str] = None,
                permanent: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                retention_duration_days: typing.Optional[jsii.Number] = None,
                timezone: typing.Optional[builtins.str] = None,
                week_backups: typing.Optional[jsii.Number] = None,
                year_backups: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument operation_type", value=operation_type, expected_type=type_hints["operation_type"])
            check_type(argname="argument trigger_pattern", value=trigger_pattern, expected_type=type_hints["trigger_pattern"])
            check_type(argname="argument day_backups", value=day_backups, expected_type=type_hints["day_backups"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_backups", value=max_backups, expected_type=type_hints["max_backups"])
            check_type(argname="argument month_backups", value=month_backups, expected_type=type_hints["month_backups"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permanent", value=permanent, expected_type=type_hints["permanent"])
            check_type(argname="argument retention_duration_days", value=retention_duration_days, expected_type=type_hints["retention_duration_days"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument week_backups", value=week_backups, expected_type=type_hints["week_backups"])
            check_type(argname="argument year_backups", value=year_backups, expected_type=type_hints["year_backups"])
        self._values: typing.Dict[str, typing.Any] = {
            "operation_type": operation_type,
            "trigger_pattern": trigger_pattern,
        }
        if day_backups is not None:
            self._values["day_backups"] = day_backups
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_backups is not None:
            self._values["max_backups"] = max_backups
        if month_backups is not None:
            self._values["month_backups"] = month_backups
        if name is not None:
            self._values["name"] = name
        if permanent is not None:
            self._values["permanent"] = permanent
        if retention_duration_days is not None:
            self._values["retention_duration_days"] = retention_duration_days
        if timezone is not None:
            self._values["timezone"] = timezone
        if week_backups is not None:
            self._values["week_backups"] = week_backups
        if year_backups is not None:
            self._values["year_backups"] = year_backups

    @builtins.property
    def operation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.'''
        result = self._values.get("operation_type")
        assert result is not None, "Required property 'operation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.'''
        result = self._values.get("trigger_pattern")
        assert result is not None, "Required property 'trigger_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def day_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.'''
        result = self._values.get("day_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def max_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.'''
        result = self._values.get("max_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.'''
        result = self._values.get("month_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.'''
        result = self._values.get("permanent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def retention_duration_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.'''
        result = self._values.get("retention_duration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.'''
        result = self._values.get("week_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.'''
        result = self._values.get("year_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1ScheduledOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1ScheduledOperationOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ScheduledOperationOutputReference",
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

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMaxBackups")
    def reset_max_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackups", []))

    @jsii.member(jsii_name="resetMonthBackups")
    def reset_month_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthBackups", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPermanent")
    def reset_permanent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanent", []))

    @jsii.member(jsii_name="resetRetentionDurationDays")
    def reset_retention_duration_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDurationDays", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetWeekBackups")
    def reset_week_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekBackups", []))

    @jsii.member(jsii_name="resetYearBackups")
    def reset_year_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYearBackups", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

    @builtins.property
    @jsii.member(jsii_name="triggerType")
    def trigger_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerType"))

    @builtins.property
    @jsii.member(jsii_name="dayBackupsInput")
    def day_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackupsInput")
    def max_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="monthBackupsInput")
    def month_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationTypeInput")
    def operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentInput")
    def permanent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "permanentInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationDaysInput")
    def retention_duration_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDurationDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerPatternInput")
    def trigger_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerPatternInput"))

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
    @jsii.member(jsii_name="permanent")
    def permanent(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "permanent"))

    @permanent.setter
    def permanent(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanent", value)

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
    @jsii.member(jsii_name="triggerPattern")
    def trigger_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerPattern"))

    @trigger_pattern.setter
    def trigger_pattern(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerPattern", value)

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
    def internal_value(self) -> typing.Optional[CsbsBackupPolicyV1ScheduledOperation]:
        return typing.cast(typing.Optional[CsbsBackupPolicyV1ScheduledOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CsbsBackupPolicyV1ScheduledOperation],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[CsbsBackupPolicyV1ScheduledOperation],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Tags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CsbsBackupPolicyV1Tags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#key CsbsBackupPolicyV1#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#value CsbsBackupPolicyV1#value}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#key CsbsBackupPolicyV1#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#value CsbsBackupPolicyV1#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Tags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1TagsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TagsList",
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
    def get(self, index: jsii.Number) -> "CsbsBackupPolicyV1TagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CsbsBackupPolicyV1TagsOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CsbsBackupPolicyV1TagsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TagsOutputReference",
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
    ) -> typing.Optional[typing.Union[CsbsBackupPolicyV1Tags, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CsbsBackupPolicyV1Tags, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CsbsBackupPolicyV1Tags, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CsbsBackupPolicyV1Tags, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CsbsBackupPolicyV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CsbsBackupPolicyV1",
    "CsbsBackupPolicyV1Config",
    "CsbsBackupPolicyV1Resource",
    "CsbsBackupPolicyV1ResourceList",
    "CsbsBackupPolicyV1ResourceOutputReference",
    "CsbsBackupPolicyV1ScheduledOperation",
    "CsbsBackupPolicyV1ScheduledOperationOutputReference",
    "CsbsBackupPolicyV1Tags",
    "CsbsBackupPolicyV1TagsList",
    "CsbsBackupPolicyV1TagsOutputReference",
    "CsbsBackupPolicyV1Timeouts",
    "CsbsBackupPolicyV1TimeoutsOutputReference",
]

publication.publish()
