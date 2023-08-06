'''
# `opentelekomcloud_cts_tracker_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_cts_tracker_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1).
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


class CtsTrackerV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsTrackerV1.CtsTrackerV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1 opentelekomcloud_cts_tracker_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        bucket_name: builtins.str,
        is_support_smn: typing.Union[builtins.bool, cdktf.IResolvable],
        file_prefix_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_send_all_key_operation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        need_notify_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CtsTrackerV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        topic_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1 opentelekomcloud_cts_tracker_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#bucket_name CtsTrackerV1#bucket_name}.
        :param is_support_smn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_support_smn CtsTrackerV1#is_support_smn}.
        :param file_prefix_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#file_prefix_name CtsTrackerV1#file_prefix_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#id CtsTrackerV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_send_all_key_operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_send_all_key_operation CtsTrackerV1#is_send_all_key_operation}.
        :param need_notify_user_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#need_notify_user_list CtsTrackerV1#need_notify_user_list}.
        :param operations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#operations CtsTrackerV1#operations}.
        :param project_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#project_name CtsTrackerV1#project_name}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#region CtsTrackerV1#region}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#status CtsTrackerV1#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#timeouts CtsTrackerV1#timeouts}
        :param topic_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#topic_id CtsTrackerV1#topic_id}.
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
                bucket_name: builtins.str,
                is_support_smn: typing.Union[builtins.bool, cdktf.IResolvable],
                file_prefix_name: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                is_send_all_key_operation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                need_notify_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
                operations: typing.Optional[typing.Sequence[builtins.str]] = None,
                project_name: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                status: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["CtsTrackerV1Timeouts", typing.Dict[str, typing.Any]]] = None,
                topic_id: typing.Optional[builtins.str] = None,
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
        config = CtsTrackerV1Config(
            bucket_name=bucket_name,
            is_support_smn=is_support_smn,
            file_prefix_name=file_prefix_name,
            id=id,
            is_send_all_key_operation=is_send_all_key_operation,
            need_notify_user_list=need_notify_user_list,
            operations=operations,
            project_name=project_name,
            region=region,
            status=status,
            timeouts=timeouts,
            topic_id=topic_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#create CtsTrackerV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#delete CtsTrackerV1#delete}.
        '''
        value = CtsTrackerV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFilePrefixName")
    def reset_file_prefix_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePrefixName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsSendAllKeyOperation")
    def reset_is_send_all_key_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSendAllKeyOperation", []))

    @jsii.member(jsii_name="resetNeedNotifyUserList")
    def reset_need_notify_user_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNeedNotifyUserList", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetProjectName")
    def reset_project_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTopicId")
    def reset_topic_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CtsTrackerV1TimeoutsOutputReference":
        return typing.cast("CtsTrackerV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackerName"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="filePrefixNameInput")
    def file_prefix_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePrefixNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isSendAllKeyOperationInput")
    def is_send_all_key_operation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "isSendAllKeyOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="isSupportSmnInput")
    def is_support_smn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "isSupportSmnInput"))

    @builtins.property
    @jsii.member(jsii_name="needNotifyUserListInput")
    def need_notify_user_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "needNotifyUserListInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNameInput")
    def project_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CtsTrackerV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CtsTrackerV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicIdInput")
    def topic_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="filePrefixName")
    def file_prefix_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePrefixName"))

    @file_prefix_name.setter
    def file_prefix_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePrefixName", value)

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
    @jsii.member(jsii_name="isSendAllKeyOperation")
    def is_send_all_key_operation(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "isSendAllKeyOperation"))

    @is_send_all_key_operation.setter
    def is_send_all_key_operation(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSendAllKeyOperation", value)

    @builtins.property
    @jsii.member(jsii_name="isSupportSmn")
    def is_support_smn(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "isSupportSmn"))

    @is_support_smn.setter
    def is_support_smn(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSupportSmn", value)

    @builtins.property
    @jsii.member(jsii_name="needNotifyUserList")
    def need_notify_user_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "needNotifyUserList"))

    @need_notify_user_list.setter
    def need_notify_user_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needNotifyUserList", value)

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operations"))

    @operations.setter
    def operations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operations", value)

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)

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
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="topicId")
    def topic_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicId"))

    @topic_id.setter
    def topic_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsTrackerV1.CtsTrackerV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_name": "bucketName",
        "is_support_smn": "isSupportSmn",
        "file_prefix_name": "filePrefixName",
        "id": "id",
        "is_send_all_key_operation": "isSendAllKeyOperation",
        "need_notify_user_list": "needNotifyUserList",
        "operations": "operations",
        "project_name": "projectName",
        "region": "region",
        "status": "status",
        "timeouts": "timeouts",
        "topic_id": "topicId",
    },
)
class CtsTrackerV1Config(cdktf.TerraformMetaArguments):
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
        bucket_name: builtins.str,
        is_support_smn: typing.Union[builtins.bool, cdktf.IResolvable],
        file_prefix_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_send_all_key_operation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        need_notify_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CtsTrackerV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        topic_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#bucket_name CtsTrackerV1#bucket_name}.
        :param is_support_smn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_support_smn CtsTrackerV1#is_support_smn}.
        :param file_prefix_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#file_prefix_name CtsTrackerV1#file_prefix_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#id CtsTrackerV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_send_all_key_operation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_send_all_key_operation CtsTrackerV1#is_send_all_key_operation}.
        :param need_notify_user_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#need_notify_user_list CtsTrackerV1#need_notify_user_list}.
        :param operations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#operations CtsTrackerV1#operations}.
        :param project_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#project_name CtsTrackerV1#project_name}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#region CtsTrackerV1#region}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#status CtsTrackerV1#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#timeouts CtsTrackerV1#timeouts}
        :param topic_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#topic_id CtsTrackerV1#topic_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CtsTrackerV1Timeouts(**timeouts)
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
                bucket_name: builtins.str,
                is_support_smn: typing.Union[builtins.bool, cdktf.IResolvable],
                file_prefix_name: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                is_send_all_key_operation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                need_notify_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
                operations: typing.Optional[typing.Sequence[builtins.str]] = None,
                project_name: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                status: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["CtsTrackerV1Timeouts", typing.Dict[str, typing.Any]]] = None,
                topic_id: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument is_support_smn", value=is_support_smn, expected_type=type_hints["is_support_smn"])
            check_type(argname="argument file_prefix_name", value=file_prefix_name, expected_type=type_hints["file_prefix_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_send_all_key_operation", value=is_send_all_key_operation, expected_type=type_hints["is_send_all_key_operation"])
            check_type(argname="argument need_notify_user_list", value=need_notify_user_list, expected_type=type_hints["need_notify_user_list"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument topic_id", value=topic_id, expected_type=type_hints["topic_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
            "is_support_smn": is_support_smn,
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
        if file_prefix_name is not None:
            self._values["file_prefix_name"] = file_prefix_name
        if id is not None:
            self._values["id"] = id
        if is_send_all_key_operation is not None:
            self._values["is_send_all_key_operation"] = is_send_all_key_operation
        if need_notify_user_list is not None:
            self._values["need_notify_user_list"] = need_notify_user_list
        if operations is not None:
            self._values["operations"] = operations
        if project_name is not None:
            self._values["project_name"] = project_name
        if region is not None:
            self._values["region"] = region
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if topic_id is not None:
            self._values["topic_id"] = topic_id

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
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#bucket_name CtsTrackerV1#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_support_smn(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_support_smn CtsTrackerV1#is_support_smn}.'''
        result = self._values.get("is_support_smn")
        assert result is not None, "Required property 'is_support_smn' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def file_prefix_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#file_prefix_name CtsTrackerV1#file_prefix_name}.'''
        result = self._values.get("file_prefix_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#id CtsTrackerV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_send_all_key_operation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#is_send_all_key_operation CtsTrackerV1#is_send_all_key_operation}.'''
        result = self._values.get("is_send_all_key_operation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def need_notify_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#need_notify_user_list CtsTrackerV1#need_notify_user_list}.'''
        result = self._values.get("need_notify_user_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#operations CtsTrackerV1#operations}.'''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#project_name CtsTrackerV1#project_name}.'''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#region CtsTrackerV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#status CtsTrackerV1#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CtsTrackerV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#timeouts CtsTrackerV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CtsTrackerV1Timeouts"], result)

    @builtins.property
    def topic_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#topic_id CtsTrackerV1#topic_id}.'''
        result = self._values.get("topic_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsTrackerV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsTrackerV1.CtsTrackerV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CtsTrackerV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#create CtsTrackerV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#delete CtsTrackerV1#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#create CtsTrackerV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cts_tracker_v1#delete CtsTrackerV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsTrackerV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CtsTrackerV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsTrackerV1.CtsTrackerV1TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[CtsTrackerV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CtsTrackerV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CtsTrackerV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CtsTrackerV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CtsTrackerV1",
    "CtsTrackerV1Config",
    "CtsTrackerV1Timeouts",
    "CtsTrackerV1TimeoutsOutputReference",
]

publication.publish()
