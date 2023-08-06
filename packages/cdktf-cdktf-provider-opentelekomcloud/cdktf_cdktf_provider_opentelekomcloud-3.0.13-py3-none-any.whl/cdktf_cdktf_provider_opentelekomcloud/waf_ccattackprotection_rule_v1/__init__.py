'''
# `opentelekomcloud_waf_ccattackprotection_rule_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_waf_ccattackprotection_rule_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1).
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


class WafCcattackprotectionRuleV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1 opentelekomcloud_waf_ccattackprotection_rule_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        action_category: builtins.str,
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        block_content: typing.Optional[builtins.str] = None,
        block_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1 opentelekomcloud_waf_ccattackprotection_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.
        :param limit_num: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.
        :param policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.
        :param block_content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.
        :param block_content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
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
                action_category: builtins.str,
                limit_num: jsii.Number,
                limit_period: jsii.Number,
                policy_id: builtins.str,
                tag_type: builtins.str,
                url: builtins.str,
                block_content: typing.Optional[builtins.str] = None,
                block_content_type: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                lock_time: typing.Optional[jsii.Number] = None,
                tag_category: typing.Optional[builtins.str] = None,
                tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_index: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = WafCcattackprotectionRuleV1Config(
            action_category=action_category,
            limit_num=limit_num,
            limit_period=limit_period,
            policy_id=policy_id,
            tag_type=tag_type,
            url=url,
            block_content=block_content,
            block_content_type=block_content_type,
            id=id,
            lock_time=lock_time,
            tag_category=tag_category,
            tag_contents=tag_contents,
            tag_index=tag_index,
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

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.
        '''
        value = WafCcattackprotectionRuleV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlockContent")
    def reset_block_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockContent", []))

    @jsii.member(jsii_name="resetBlockContentType")
    def reset_block_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockContentType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLockTime")
    def reset_lock_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockTime", []))

    @jsii.member(jsii_name="resetTagCategory")
    def reset_tag_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCategory", []))

    @jsii.member(jsii_name="resetTagContents")
    def reset_tag_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagContents", []))

    @jsii.member(jsii_name="resetTagIndex")
    def reset_tag_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagIndex", []))

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
    @jsii.member(jsii_name="default")
    def default(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafCcattackprotectionRuleV1TimeoutsOutputReference":
        return typing.cast("WafCcattackprotectionRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionCategoryInput")
    def action_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="blockContentInput")
    def block_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockContentInput"))

    @builtins.property
    @jsii.member(jsii_name="blockContentTypeInput")
    def block_content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockContentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="limitNumInput")
    def limit_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitNumInput"))

    @builtins.property
    @jsii.member(jsii_name="limitPeriodInput")
    def limit_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeInput")
    def lock_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCategoryInput")
    def tag_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagContentsInput")
    def tag_contents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagContentsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagIndexInput")
    def tag_index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="tagTypeInput")
    def tag_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="actionCategory")
    def action_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionCategory"))

    @action_category.setter
    def action_category(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionCategory", value)

    @builtins.property
    @jsii.member(jsii_name="blockContent")
    def block_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockContent"))

    @block_content.setter
    def block_content(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockContent", value)

    @builtins.property
    @jsii.member(jsii_name="blockContentType")
    def block_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockContentType"))

    @block_content_type.setter
    def block_content_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockContentType", value)

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
    @jsii.member(jsii_name="limitNum")
    def limit_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitNum"))

    @limit_num.setter
    def limit_num(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitNum", value)

    @builtins.property
    @jsii.member(jsii_name="limitPeriod")
    def limit_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitPeriod"))

    @limit_period.setter
    def limit_period(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="lockTime")
    def lock_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTime"))

    @lock_time.setter
    def lock_time(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTime", value)

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
    @jsii.member(jsii_name="tagCategory")
    def tag_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagCategory"))

    @tag_category.setter
    def tag_category(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagCategory", value)

    @builtins.property
    @jsii.member(jsii_name="tagContents")
    def tag_contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagContents"))

    @tag_contents.setter
    def tag_contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagContents", value)

    @builtins.property
    @jsii.member(jsii_name="tagIndex")
    def tag_index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagIndex"))

    @tag_index.setter
    def tag_index(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagIndex", value)

    @builtins.property
    @jsii.member(jsii_name="tagType")
    def tag_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagType"))

    @tag_type.setter
    def tag_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagType", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_category": "actionCategory",
        "limit_num": "limitNum",
        "limit_period": "limitPeriod",
        "policy_id": "policyId",
        "tag_type": "tagType",
        "url": "url",
        "block_content": "blockContent",
        "block_content_type": "blockContentType",
        "id": "id",
        "lock_time": "lockTime",
        "tag_category": "tagCategory",
        "tag_contents": "tagContents",
        "tag_index": "tagIndex",
        "timeouts": "timeouts",
    },
)
class WafCcattackprotectionRuleV1Config(cdktf.TerraformMetaArguments):
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
        action_category: builtins.str,
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        block_content: typing.Optional[builtins.str] = None,
        block_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.
        :param limit_num: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.
        :param policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.
        :param block_content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.
        :param block_content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafCcattackprotectionRuleV1Timeouts(**timeouts)
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
                action_category: builtins.str,
                limit_num: jsii.Number,
                limit_period: jsii.Number,
                policy_id: builtins.str,
                tag_type: builtins.str,
                url: builtins.str,
                block_content: typing.Optional[builtins.str] = None,
                block_content_type: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                lock_time: typing.Optional[jsii.Number] = None,
                tag_category: typing.Optional[builtins.str] = None,
                tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_index: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument action_category", value=action_category, expected_type=type_hints["action_category"])
            check_type(argname="argument limit_num", value=limit_num, expected_type=type_hints["limit_num"])
            check_type(argname="argument limit_period", value=limit_period, expected_type=type_hints["limit_period"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument tag_type", value=tag_type, expected_type=type_hints["tag_type"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument block_content", value=block_content, expected_type=type_hints["block_content"])
            check_type(argname="argument block_content_type", value=block_content_type, expected_type=type_hints["block_content_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_time", value=lock_time, expected_type=type_hints["lock_time"])
            check_type(argname="argument tag_category", value=tag_category, expected_type=type_hints["tag_category"])
            check_type(argname="argument tag_contents", value=tag_contents, expected_type=type_hints["tag_contents"])
            check_type(argname="argument tag_index", value=tag_index, expected_type=type_hints["tag_index"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "action_category": action_category,
            "limit_num": limit_num,
            "limit_period": limit_period,
            "policy_id": policy_id,
            "tag_type": tag_type,
            "url": url,
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
        if block_content is not None:
            self._values["block_content"] = block_content
        if block_content_type is not None:
            self._values["block_content_type"] = block_content_type
        if id is not None:
            self._values["id"] = id
        if lock_time is not None:
            self._values["lock_time"] = lock_time
        if tag_category is not None:
            self._values["tag_category"] = tag_category
        if tag_contents is not None:
            self._values["tag_contents"] = tag_contents
        if tag_index is not None:
            self._values["tag_index"] = tag_index
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
    def action_category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.'''
        result = self._values.get("action_category")
        assert result is not None, "Required property 'action_category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def limit_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.'''
        result = self._values.get("limit_num")
        assert result is not None, "Required property 'limit_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def limit_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.'''
        result = self._values.get("limit_period")
        assert result is not None, "Required property 'limit_period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.'''
        result = self._values.get("tag_type")
        assert result is not None, "Required property 'tag_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.'''
        result = self._values.get("block_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.'''
        result = self._values.get("block_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.'''
        result = self._values.get("lock_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.'''
        result = self._values.get("tag_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.'''
        result = self._values.get("tag_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.'''
        result = self._values.get("tag_index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafCcattackprotectionRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafCcattackprotectionRuleV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafCcattackprotectionRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafCcattackprotectionRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafCcattackprotectionRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafCcattackprotectionRuleV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "WafCcattackprotectionRuleV1",
    "WafCcattackprotectionRuleV1Config",
    "WafCcattackprotectionRuleV1Timeouts",
    "WafCcattackprotectionRuleV1TimeoutsOutputReference",
]

publication.publish()
