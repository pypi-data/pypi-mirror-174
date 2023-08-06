'''
# `opentelekomcloud_s3_bucket_object`

Refer to the Terraform Registory for docs: [`opentelekomcloud_s3_bucket_object`](https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object).
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


class S3BucketObject(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3BucketObject.S3BucketObject",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object opentelekomcloud_s3_bucket_object}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        key: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        sse_kms_key_id: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object opentelekomcloud_s3_bucket_object} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#bucket S3BucketObject#bucket}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#key S3BucketObject#key}.
        :param acl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#acl S3BucketObject#acl}.
        :param cache_control: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#cache_control S3BucketObject#cache_control}.
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content S3BucketObject#content}.
        :param content_disposition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_disposition S3BucketObject#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_encoding S3BucketObject#content_encoding}.
        :param content_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_language S3BucketObject#content_language}.
        :param content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_type S3BucketObject#content_type}.
        :param etag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#etag S3BucketObject#etag}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#id S3BucketObject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param server_side_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#server_side_encryption S3BucketObject#server_side_encryption}.
        :param source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#source S3BucketObject#source}.
        :param sse_kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#sse_kms_key_id S3BucketObject#sse_kms_key_id}.
        :param website_redirect: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#website_redirect S3BucketObject#website_redirect}.
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
                bucket: builtins.str,
                key: builtins.str,
                acl: typing.Optional[builtins.str] = None,
                cache_control: typing.Optional[builtins.str] = None,
                content: typing.Optional[builtins.str] = None,
                content_disposition: typing.Optional[builtins.str] = None,
                content_encoding: typing.Optional[builtins.str] = None,
                content_language: typing.Optional[builtins.str] = None,
                content_type: typing.Optional[builtins.str] = None,
                etag: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                server_side_encryption: typing.Optional[builtins.str] = None,
                source: typing.Optional[builtins.str] = None,
                sse_kms_key_id: typing.Optional[builtins.str] = None,
                website_redirect: typing.Optional[builtins.str] = None,
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
        config = S3BucketObjectConfig(
            bucket=bucket,
            key=key,
            acl=acl,
            cache_control=cache_control,
            content=content,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_language=content_language,
            content_type=content_type,
            etag=etag,
            id=id,
            server_side_encryption=server_side_encryption,
            source=source,
            sse_kms_key_id=sse_kms_key_id,
            website_redirect=website_redirect,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetCacheControl")
    def reset_cache_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheControl", []))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentDisposition")
    def reset_content_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentDisposition", []))

    @jsii.member(jsii_name="resetContentEncoding")
    def reset_content_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentEncoding", []))

    @jsii.member(jsii_name="resetContentLanguage")
    def reset_content_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentLanguage", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServerSideEncryption")
    def reset_server_side_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryption", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSseKmsKeyId")
    def reset_sse_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSseKmsKeyId", []))

    @jsii.member(jsii_name="resetWebsiteRedirect")
    def reset_website_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsiteRedirect", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheControlInput")
    def cache_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheControlInput"))

    @builtins.property
    @jsii.member(jsii_name="contentDispositionInput")
    def content_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="contentEncodingInput")
    def content_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentLanguageInput")
    def content_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionInput")
    def server_side_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverSideEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sseKmsKeyIdInput")
    def sse_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sseKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteRedirectInput")
    def website_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websiteRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value)

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
    @jsii.member(jsii_name="cacheControl")
    def cache_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheControl"))

    @cache_control.setter
    def cache_control(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheControl", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="contentDisposition")
    def content_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentDisposition"))

    @content_disposition.setter
    def content_disposition(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentDisposition", value)

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentEncoding"))

    @content_encoding.setter
    def content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentEncoding", value)

    @builtins.property
    @jsii.member(jsii_name="contentLanguage")
    def content_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentLanguage"))

    @content_language.setter
    def content_language(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value)

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
    @jsii.member(jsii_name="serverSideEncryption")
    def server_side_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverSideEncryption"))

    @server_side_encryption.setter
    def server_side_encryption(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="sseKmsKeyId")
    def sse_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sseKmsKeyId"))

    @sse_kms_key_id.setter
    def sse_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseKmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="websiteRedirect")
    def website_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websiteRedirect"))

    @website_redirect.setter
    def website_redirect(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websiteRedirect", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3BucketObject.S3BucketObjectConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket": "bucket",
        "key": "key",
        "acl": "acl",
        "cache_control": "cacheControl",
        "content": "content",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "etag": "etag",
        "id": "id",
        "server_side_encryption": "serverSideEncryption",
        "source": "source",
        "sse_kms_key_id": "sseKmsKeyId",
        "website_redirect": "websiteRedirect",
    },
)
class S3BucketObjectConfig(cdktf.TerraformMetaArguments):
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
        bucket: builtins.str,
        key: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content: typing.Optional[builtins.str] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        sse_kms_key_id: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#bucket S3BucketObject#bucket}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#key S3BucketObject#key}.
        :param acl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#acl S3BucketObject#acl}.
        :param cache_control: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#cache_control S3BucketObject#cache_control}.
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content S3BucketObject#content}.
        :param content_disposition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_disposition S3BucketObject#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_encoding S3BucketObject#content_encoding}.
        :param content_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_language S3BucketObject#content_language}.
        :param content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_type S3BucketObject#content_type}.
        :param etag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#etag S3BucketObject#etag}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#id S3BucketObject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param server_side_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#server_side_encryption S3BucketObject#server_side_encryption}.
        :param source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#source S3BucketObject#source}.
        :param sse_kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#sse_kms_key_id S3BucketObject#sse_kms_key_id}.
        :param website_redirect: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#website_redirect S3BucketObject#website_redirect}.
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
                bucket: builtins.str,
                key: builtins.str,
                acl: typing.Optional[builtins.str] = None,
                cache_control: typing.Optional[builtins.str] = None,
                content: typing.Optional[builtins.str] = None,
                content_disposition: typing.Optional[builtins.str] = None,
                content_encoding: typing.Optional[builtins.str] = None,
                content_language: typing.Optional[builtins.str] = None,
                content_type: typing.Optional[builtins.str] = None,
                etag: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                server_side_encryption: typing.Optional[builtins.str] = None,
                source: typing.Optional[builtins.str] = None,
                sse_kms_key_id: typing.Optional[builtins.str] = None,
                website_redirect: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_disposition", value=content_disposition, expected_type=type_hints["content_disposition"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument content_language", value=content_language, expected_type=type_hints["content_language"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument sse_kms_key_id", value=sse_kms_key_id, expected_type=type_hints["sse_kms_key_id"])
            check_type(argname="argument website_redirect", value=website_redirect, expected_type=type_hints["website_redirect"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "key": key,
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
        if acl is not None:
            self._values["acl"] = acl
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content is not None:
            self._values["content"] = content
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if etag is not None:
            self._values["etag"] = etag
        if id is not None:
            self._values["id"] = id
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if source is not None:
            self._values["source"] = source
        if sse_kms_key_id is not None:
            self._values["sse_kms_key_id"] = sse_kms_key_id
        if website_redirect is not None:
            self._values["website_redirect"] = website_redirect

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
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#bucket S3BucketObject#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#key S3BucketObject#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#acl S3BucketObject#acl}.'''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_control(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#cache_control S3BucketObject#cache_control}.'''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content S3BucketObject#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_disposition S3BucketObject#content_disposition}.'''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_encoding S3BucketObject#content_encoding}.'''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_language S3BucketObject#content_language}.'''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#content_type S3BucketObject#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#etag S3BucketObject#etag}.'''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#id S3BucketObject#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#server_side_encryption S3BucketObject#server_side_encryption}.'''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#source S3BucketObject#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#sse_kms_key_id S3BucketObject#sse_kms_key_id}.'''
        result = self._values.get("sse_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_redirect(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/s3_bucket_object#website_redirect S3BucketObject#website_redirect}.'''
        result = self._values.get("website_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketObjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "S3BucketObject",
    "S3BucketObjectConfig",
]

publication.publish()
