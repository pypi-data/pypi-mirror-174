'''
# `opentelekomcloud_rds_instance_v1`

Refer to the Terraform Registory for docs: [`opentelekomcloud_rds_instance_v1`](https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1).
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


class RdsInstanceV1(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1 opentelekomcloud_rds_instance_v1}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        availabilityzone: builtins.str,
        datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[str, typing.Any]],
        dbrtpd: builtins.str,
        flavorref: builtins.str,
        nics: typing.Union["RdsInstanceV1Nics", typing.Dict[str, typing.Any]],
        securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[str, typing.Any]],
        volume: typing.Union["RdsInstanceV1Volume", typing.Dict[str, typing.Any]],
        vpc: builtins.str,
        backupstrategy: typing.Optional[typing.Union["RdsInstanceV1Backupstrategy", typing.Dict[str, typing.Any]]] = None,
        dbport: typing.Optional[builtins.str] = None,
        ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1 opentelekomcloud_rds_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availabilityzone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#datastore RdsInstanceV1#datastore}
        :param dbrtpd: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.
        :param flavorref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#nics RdsInstanceV1#nics}
        :param securitygroup: securitygroup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#volume RdsInstanceV1#volume}
        :param vpc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#vpc RdsInstanceV1#vpc}.
        :param backupstrategy: backupstrategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        :param dbport: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbport RdsInstanceV1#dbport}.
        :param ha: ha block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#ha RdsInstanceV1#ha}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#name RdsInstanceV1#name}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#region RdsInstanceV1#region}.
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#tag RdsInstanceV1#tag}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
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
                availabilityzone: builtins.str,
                datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[str, typing.Any]],
                dbrtpd: builtins.str,
                flavorref: builtins.str,
                nics: typing.Union["RdsInstanceV1Nics", typing.Dict[str, typing.Any]],
                securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[str, typing.Any]],
                volume: typing.Union["RdsInstanceV1Volume", typing.Dict[str, typing.Any]],
                vpc: builtins.str,
                backupstrategy: typing.Optional[typing.Union["RdsInstanceV1Backupstrategy", typing.Dict[str, typing.Any]]] = None,
                dbport: typing.Optional[builtins.str] = None,
                ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = RdsInstanceV1Config(
            availabilityzone=availabilityzone,
            datastore=datastore,
            dbrtpd=dbrtpd,
            flavorref=flavorref,
            nics=nics,
            securitygroup=securitygroup,
            volume=volume,
            vpc=vpc,
            backupstrategy=backupstrategy,
            dbport=dbport,
            ha=ha,
            id=id,
            name=name,
            region=region,
            tag=tag,
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

    @jsii.member(jsii_name="putBackupstrategy")
    def put_backupstrategy(
        self,
        *,
        keepdays: typing.Optional[jsii.Number] = None,
        starttime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keepdays: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.
        :param starttime: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#starttime RdsInstanceV1#starttime}.
        '''
        value = RdsInstanceV1Backupstrategy(keepdays=keepdays, starttime=starttime)

        return typing.cast(None, jsii.invoke(self, "putBackupstrategy", [value]))

    @jsii.member(jsii_name="putDatastore")
    def put_datastore(self, *, type: builtins.str, version: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#version RdsInstanceV1#version}.
        '''
        value = RdsInstanceV1Datastore(type=type, version=version)

        return typing.cast(None, jsii.invoke(self, "putDatastore", [value]))

    @jsii.member(jsii_name="putHa")
    def put_ha(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        replicationmode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#enable RdsInstanceV1#enable}.
        :param replicationmode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.
        '''
        value = RdsInstanceV1Ha(enable=enable, replicationmode=replicationmode)

        return typing.cast(None, jsii.invoke(self, "putHa", [value]))

    @jsii.member(jsii_name="putNics")
    def put_nics(self, *, subnetid: builtins.str) -> None:
        '''
        :param subnetid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.
        '''
        value = RdsInstanceV1Nics(subnetid=subnetid)

        return typing.cast(None, jsii.invoke(self, "putNics", [value]))

    @jsii.member(jsii_name="putSecuritygroup")
    def put_securitygroup(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = RdsInstanceV1Securitygroup(id=id)

        return typing.cast(None, jsii.invoke(self, "putSecuritygroup", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#create RdsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#delete RdsInstanceV1#delete}.
        '''
        value = RdsInstanceV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(self, *, size: jsii.Number, type: builtins.str) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#size RdsInstanceV1#size}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.
        '''
        value = RdsInstanceV1Volume(size=size, type=type)

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetBackupstrategy")
    def reset_backupstrategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupstrategy", []))

    @jsii.member(jsii_name="resetDbport")
    def reset_dbport(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbport", []))

    @jsii.member(jsii_name="resetHa")
    def reset_ha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHa", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="backupstrategy")
    def backupstrategy(self) -> "RdsInstanceV1BackupstrategyOutputReference":
        return typing.cast("RdsInstanceV1BackupstrategyOutputReference", jsii.get(self, "backupstrategy"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> "RdsInstanceV1DatastoreOutputReference":
        return typing.cast("RdsInstanceV1DatastoreOutputReference", jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="ha")
    def ha(self) -> "RdsInstanceV1HaOutputReference":
        return typing.cast("RdsInstanceV1HaOutputReference", jsii.get(self, "ha"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="nics")
    def nics(self) -> "RdsInstanceV1NicsOutputReference":
        return typing.cast("RdsInstanceV1NicsOutputReference", jsii.get(self, "nics"))

    @builtins.property
    @jsii.member(jsii_name="securitygroup")
    def securitygroup(self) -> "RdsInstanceV1SecuritygroupOutputReference":
        return typing.cast("RdsInstanceV1SecuritygroupOutputReference", jsii.get(self, "securitygroup"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RdsInstanceV1TimeoutsOutputReference":
        return typing.cast("RdsInstanceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "RdsInstanceV1VolumeOutputReference":
        return typing.cast("RdsInstanceV1VolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityzoneInput")
    def availabilityzone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityzoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupstrategyInput")
    def backupstrategy_input(self) -> typing.Optional["RdsInstanceV1Backupstrategy"]:
        return typing.cast(typing.Optional["RdsInstanceV1Backupstrategy"], jsii.get(self, "backupstrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional["RdsInstanceV1Datastore"]:
        return typing.cast(typing.Optional["RdsInstanceV1Datastore"], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="dbportInput")
    def dbport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbportInput"))

    @builtins.property
    @jsii.member(jsii_name="dbrtpdInput")
    def dbrtpd_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbrtpdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorrefInput")
    def flavorref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorrefInput"))

    @builtins.property
    @jsii.member(jsii_name="haInput")
    def ha_input(self) -> typing.Optional["RdsInstanceV1Ha"]:
        return typing.cast(typing.Optional["RdsInstanceV1Ha"], jsii.get(self, "haInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nicsInput")
    def nics_input(self) -> typing.Optional["RdsInstanceV1Nics"]:
        return typing.cast(typing.Optional["RdsInstanceV1Nics"], jsii.get(self, "nicsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securitygroupInput")
    def securitygroup_input(self) -> typing.Optional["RdsInstanceV1Securitygroup"]:
        return typing.cast(typing.Optional["RdsInstanceV1Securitygroup"], jsii.get(self, "securitygroupInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["RdsInstanceV1Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["RdsInstanceV1Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["RdsInstanceV1Volume"]:
        return typing.cast(typing.Optional["RdsInstanceV1Volume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityzone")
    def availabilityzone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityzone"))

    @availabilityzone.setter
    def availabilityzone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityzone", value)

    @builtins.property
    @jsii.member(jsii_name="dbport")
    def dbport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbport"))

    @dbport.setter
    def dbport(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbport", value)

    @builtins.property
    @jsii.member(jsii_name="dbrtpd")
    def dbrtpd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbrtpd"))

    @dbrtpd.setter
    def dbrtpd(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbrtpd", value)

    @builtins.property
    @jsii.member(jsii_name="flavorref")
    def flavorref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorref"))

    @flavorref.setter
    def flavorref(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorref", value)

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
    @jsii.member(jsii_name="tag")
    def tag(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Backupstrategy",
    jsii_struct_bases=[],
    name_mapping={"keepdays": "keepdays", "starttime": "starttime"},
)
class RdsInstanceV1Backupstrategy:
    def __init__(
        self,
        *,
        keepdays: typing.Optional[jsii.Number] = None,
        starttime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keepdays: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.
        :param starttime: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#starttime RdsInstanceV1#starttime}.
        '''
        if __debug__:
            def stub(
                *,
                keepdays: typing.Optional[jsii.Number] = None,
                starttime: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument keepdays", value=keepdays, expected_type=type_hints["keepdays"])
            check_type(argname="argument starttime", value=starttime, expected_type=type_hints["starttime"])
        self._values: typing.Dict[str, typing.Any] = {}
        if keepdays is not None:
            self._values["keepdays"] = keepdays
        if starttime is not None:
            self._values["starttime"] = starttime

    @builtins.property
    def keepdays(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.'''
        result = self._values.get("keepdays")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starttime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#starttime RdsInstanceV1#starttime}.'''
        result = self._values.get("starttime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Backupstrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1BackupstrategyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1BackupstrategyOutputReference",
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

    @jsii.member(jsii_name="resetKeepdays")
    def reset_keepdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepdays", []))

    @jsii.member(jsii_name="resetStarttime")
    def reset_starttime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStarttime", []))

    @builtins.property
    @jsii.member(jsii_name="keepdaysInput")
    def keepdays_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="starttimeInput")
    def starttime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "starttimeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepdays")
    def keepdays(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepdays"))

    @keepdays.setter
    def keepdays(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepdays", value)

    @builtins.property
    @jsii.member(jsii_name="starttime")
    def starttime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "starttime"))

    @starttime.setter
    def starttime(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "starttime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Backupstrategy]:
        return typing.cast(typing.Optional[RdsInstanceV1Backupstrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV1Backupstrategy],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Backupstrategy]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availabilityzone": "availabilityzone",
        "datastore": "datastore",
        "dbrtpd": "dbrtpd",
        "flavorref": "flavorref",
        "nics": "nics",
        "securitygroup": "securitygroup",
        "volume": "volume",
        "vpc": "vpc",
        "backupstrategy": "backupstrategy",
        "dbport": "dbport",
        "ha": "ha",
        "id": "id",
        "name": "name",
        "region": "region",
        "tag": "tag",
        "timeouts": "timeouts",
    },
)
class RdsInstanceV1Config(cdktf.TerraformMetaArguments):
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
        availabilityzone: builtins.str,
        datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[str, typing.Any]],
        dbrtpd: builtins.str,
        flavorref: builtins.str,
        nics: typing.Union["RdsInstanceV1Nics", typing.Dict[str, typing.Any]],
        securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[str, typing.Any]],
        volume: typing.Union["RdsInstanceV1Volume", typing.Dict[str, typing.Any]],
        vpc: builtins.str,
        backupstrategy: typing.Optional[typing.Union[RdsInstanceV1Backupstrategy, typing.Dict[str, typing.Any]]] = None,
        dbport: typing.Optional[builtins.str] = None,
        ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availabilityzone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#datastore RdsInstanceV1#datastore}
        :param dbrtpd: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.
        :param flavorref: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#nics RdsInstanceV1#nics}
        :param securitygroup: securitygroup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#volume RdsInstanceV1#volume}
        :param vpc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#vpc RdsInstanceV1#vpc}.
        :param backupstrategy: backupstrategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        :param dbport: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbport RdsInstanceV1#dbport}.
        :param ha: ha block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#ha RdsInstanceV1#ha}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#name RdsInstanceV1#name}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#region RdsInstanceV1#region}.
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#tag RdsInstanceV1#tag}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(datastore, dict):
            datastore = RdsInstanceV1Datastore(**datastore)
        if isinstance(nics, dict):
            nics = RdsInstanceV1Nics(**nics)
        if isinstance(securitygroup, dict):
            securitygroup = RdsInstanceV1Securitygroup(**securitygroup)
        if isinstance(volume, dict):
            volume = RdsInstanceV1Volume(**volume)
        if isinstance(backupstrategy, dict):
            backupstrategy = RdsInstanceV1Backupstrategy(**backupstrategy)
        if isinstance(ha, dict):
            ha = RdsInstanceV1Ha(**ha)
        if isinstance(timeouts, dict):
            timeouts = RdsInstanceV1Timeouts(**timeouts)
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
                availabilityzone: builtins.str,
                datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[str, typing.Any]],
                dbrtpd: builtins.str,
                flavorref: builtins.str,
                nics: typing.Union["RdsInstanceV1Nics", typing.Dict[str, typing.Any]],
                securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[str, typing.Any]],
                volume: typing.Union["RdsInstanceV1Volume", typing.Dict[str, typing.Any]],
                vpc: builtins.str,
                backupstrategy: typing.Optional[typing.Union[RdsInstanceV1Backupstrategy, typing.Dict[str, typing.Any]]] = None,
                dbport: typing.Optional[builtins.str] = None,
                ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument availabilityzone", value=availabilityzone, expected_type=type_hints["availabilityzone"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument dbrtpd", value=dbrtpd, expected_type=type_hints["dbrtpd"])
            check_type(argname="argument flavorref", value=flavorref, expected_type=type_hints["flavorref"])
            check_type(argname="argument nics", value=nics, expected_type=type_hints["nics"])
            check_type(argname="argument securitygroup", value=securitygroup, expected_type=type_hints["securitygroup"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument backupstrategy", value=backupstrategy, expected_type=type_hints["backupstrategy"])
            check_type(argname="argument dbport", value=dbport, expected_type=type_hints["dbport"])
            check_type(argname="argument ha", value=ha, expected_type=type_hints["ha"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "availabilityzone": availabilityzone,
            "datastore": datastore,
            "dbrtpd": dbrtpd,
            "flavorref": flavorref,
            "nics": nics,
            "securitygroup": securitygroup,
            "volume": volume,
            "vpc": vpc,
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
        if backupstrategy is not None:
            self._values["backupstrategy"] = backupstrategy
        if dbport is not None:
            self._values["dbport"] = dbport
        if ha is not None:
            self._values["ha"] = ha
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if tag is not None:
            self._values["tag"] = tag
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
    def availabilityzone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.'''
        result = self._values.get("availabilityzone")
        assert result is not None, "Required property 'availabilityzone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore(self) -> "RdsInstanceV1Datastore":
        '''datastore block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#datastore RdsInstanceV1#datastore}
        '''
        result = self._values.get("datastore")
        assert result is not None, "Required property 'datastore' is missing"
        return typing.cast("RdsInstanceV1Datastore", result)

    @builtins.property
    def dbrtpd(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.'''
        result = self._values.get("dbrtpd")
        assert result is not None, "Required property 'dbrtpd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavorref(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.'''
        result = self._values.get("flavorref")
        assert result is not None, "Required property 'flavorref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nics(self) -> "RdsInstanceV1Nics":
        '''nics block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#nics RdsInstanceV1#nics}
        '''
        result = self._values.get("nics")
        assert result is not None, "Required property 'nics' is missing"
        return typing.cast("RdsInstanceV1Nics", result)

    @builtins.property
    def securitygroup(self) -> "RdsInstanceV1Securitygroup":
        '''securitygroup block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        '''
        result = self._values.get("securitygroup")
        assert result is not None, "Required property 'securitygroup' is missing"
        return typing.cast("RdsInstanceV1Securitygroup", result)

    @builtins.property
    def volume(self) -> "RdsInstanceV1Volume":
        '''volume block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#volume RdsInstanceV1#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("RdsInstanceV1Volume", result)

    @builtins.property
    def vpc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#vpc RdsInstanceV1#vpc}.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backupstrategy(self) -> typing.Optional[RdsInstanceV1Backupstrategy]:
        '''backupstrategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        '''
        result = self._values.get("backupstrategy")
        return typing.cast(typing.Optional[RdsInstanceV1Backupstrategy], result)

    @builtins.property
    def dbport(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#dbport RdsInstanceV1#dbport}.'''
        result = self._values.get("dbport")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha(self) -> typing.Optional["RdsInstanceV1Ha"]:
        '''ha block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#ha RdsInstanceV1#ha}
        '''
        result = self._values.get("ha")
        return typing.cast(typing.Optional["RdsInstanceV1Ha"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#name RdsInstanceV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#region RdsInstanceV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#tag RdsInstanceV1#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RdsInstanceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RdsInstanceV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Datastore",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "version": "version"},
)
class RdsInstanceV1Datastore:
    def __init__(self, *, type: builtins.str, version: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#version RdsInstanceV1#version}.
        '''
        if __debug__:
            def stub(*, type: builtins.str, version: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
            "version": version,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#version RdsInstanceV1#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Datastore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1DatastoreOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1DatastoreOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

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
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Datastore]:
        return typing.cast(typing.Optional[RdsInstanceV1Datastore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Datastore]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Datastore]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Ha",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "replicationmode": "replicationmode"},
)
class RdsInstanceV1Ha:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        replicationmode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#enable RdsInstanceV1#enable}.
        :param replicationmode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.
        '''
        if __debug__:
            def stub(
                *,
                enable: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                replicationmode: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument replicationmode", value=replicationmode, expected_type=type_hints["replicationmode"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if replicationmode is not None:
            self._values["replicationmode"] = replicationmode

    @builtins.property
    def enable(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#enable RdsInstanceV1#enable}.'''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def replicationmode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.'''
        result = self._values.get("replicationmode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Ha(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1HaOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1HaOutputReference",
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

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetReplicationmode")
    def reset_replicationmode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationmode", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationmodeInput")
    def replicationmode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationmodeInput"))

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
    @jsii.member(jsii_name="replicationmode")
    def replicationmode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationmode"))

    @replicationmode.setter
    def replicationmode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationmode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Ha]:
        return typing.cast(typing.Optional[RdsInstanceV1Ha], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Ha]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Ha]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Nics",
    jsii_struct_bases=[],
    name_mapping={"subnetid": "subnetid"},
)
class RdsInstanceV1Nics:
    def __init__(self, *, subnetid: builtins.str) -> None:
        '''
        :param subnetid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.
        '''
        if __debug__:
            def stub(*, subnetid: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument subnetid", value=subnetid, expected_type=type_hints["subnetid"])
        self._values: typing.Dict[str, typing.Any] = {
            "subnetid": subnetid,
        }

    @builtins.property
    def subnetid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.'''
        result = self._values.get("subnetid")
        assert result is not None, "Required property 'subnetid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Nics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1NicsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1NicsOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="subnetidInput")
    def subnetid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetidInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetid")
    def subnetid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetid"))

    @subnetid.setter
    def subnetid(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetid", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Nics]:
        return typing.cast(typing.Optional[RdsInstanceV1Nics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Nics]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Nics]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Securitygroup",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class RdsInstanceV1Securitygroup:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            def stub(*, id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#id RdsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Securitygroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1SecuritygroupOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1SecuritygroupOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Securitygroup]:
        return typing.cast(typing.Optional[RdsInstanceV1Securitygroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV1Securitygroup],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Securitygroup]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class RdsInstanceV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#create RdsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#delete RdsInstanceV1#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#create RdsInstanceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#delete RdsInstanceV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[RdsInstanceV1Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RdsInstanceV1Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RdsInstanceV1Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[RdsInstanceV1Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Volume",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "type": "type"},
)
class RdsInstanceV1Volume:
    def __init__(self, *, size: jsii.Number, type: builtins.str) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#size RdsInstanceV1#size}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.
        '''
        if __debug__:
            def stub(*, size: jsii.Number, type: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {
            "size": size,
            "type": type,
        }

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#size RdsInstanceV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v1#type RdsInstanceV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Volume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1VolumeOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1VolumeOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
    def internal_value(self) -> typing.Optional[RdsInstanceV1Volume]:
        return typing.cast(typing.Optional[RdsInstanceV1Volume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Volume]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV1Volume]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "RdsInstanceV1",
    "RdsInstanceV1Backupstrategy",
    "RdsInstanceV1BackupstrategyOutputReference",
    "RdsInstanceV1Config",
    "RdsInstanceV1Datastore",
    "RdsInstanceV1DatastoreOutputReference",
    "RdsInstanceV1Ha",
    "RdsInstanceV1HaOutputReference",
    "RdsInstanceV1Nics",
    "RdsInstanceV1NicsOutputReference",
    "RdsInstanceV1Securitygroup",
    "RdsInstanceV1SecuritygroupOutputReference",
    "RdsInstanceV1Timeouts",
    "RdsInstanceV1TimeoutsOutputReference",
    "RdsInstanceV1Volume",
    "RdsInstanceV1VolumeOutputReference",
]

publication.publish()
