'''
# `opentelekomcloud_rds_instance_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_rds_instance_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3).
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


class RdsInstanceV3(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3 opentelekomcloud_rds_instance_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        availability_zone: typing.Sequence[builtins.str],
        db: typing.Union["RdsInstanceV3Db", typing.Dict[str, typing.Any]],
        flavor: builtins.str,
        name: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        volume: typing.Union["RdsInstanceV3Volume", typing.Dict[str, typing.Any]],
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union["RdsInstanceV3BackupStrategy", typing.Dict[str, typing.Any]]] = None,
        ha_replication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        param_group_id: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[str, typing.Any]]] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3 opentelekomcloud_rds_instance_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.
        :param db: db block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#db RdsInstanceV3#db}
        :param flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#flavor RdsInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#name RdsInstanceV3#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#volume RdsInstanceV3#volume}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        :param ha_replication_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#id RdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#parameters RdsInstanceV3#parameters}.
        :param param_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.
        :param public_ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.
        :param restore_point: restore_point block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tag RdsInstanceV3#tag}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tags RdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
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
                availability_zone: typing.Sequence[builtins.str],
                db: typing.Union["RdsInstanceV3Db", typing.Dict[str, typing.Any]],
                flavor: builtins.str,
                name: builtins.str,
                security_group_id: builtins.str,
                subnet_id: builtins.str,
                volume: typing.Union["RdsInstanceV3Volume", typing.Dict[str, typing.Any]],
                vpc_id: builtins.str,
                backup_strategy: typing.Optional[typing.Union["RdsInstanceV3BackupStrategy", typing.Dict[str, typing.Any]]] = None,
                ha_replication_mode: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                param_group_id: typing.Optional[builtins.str] = None,
                public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
                restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[str, typing.Any]]] = None,
                tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = RdsInstanceV3Config(
            availability_zone=availability_zone,
            db=db,
            flavor=flavor,
            name=name,
            security_group_id=security_group_id,
            subnet_id=subnet_id,
            volume=volume,
            vpc_id=vpc_id,
            backup_strategy=backup_strategy,
            ha_replication_mode=ha_replication_mode,
            id=id,
            parameters=parameters,
            param_group_id=param_group_id,
            public_ips=public_ips,
            restore_point=restore_point,
            tag=tag,
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

    @jsii.member(jsii_name="putBackupStrategy")
    def put_backup_strategy(
        self,
        *,
        start_time: builtins.str,
        keep_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#start_time RdsInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.
        '''
        value = RdsInstanceV3BackupStrategy(start_time=start_time, keep_days=keep_days)

        return typing.cast(None, jsii.invoke(self, "putBackupStrategy", [value]))

    @jsii.member(jsii_name="putDb")
    def put_db(
        self,
        *,
        password: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#password RdsInstanceV3#password}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#port RdsInstanceV3#port}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#version RdsInstanceV3#version}.
        '''
        value = RdsInstanceV3Db(
            password=password, port=port, type=type, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putDb", [value]))

    @jsii.member(jsii_name="putRestorePoint")
    def put_restore_point(
        self,
        *,
        instance_id: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.
        :param backup_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        value = RdsInstanceV3RestorePoint(
            instance_id=instance_id, backup_id=backup_id, restore_time=restore_time
        )

        return typing.cast(None, jsii.invoke(self, "putRestorePoint", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#create RdsInstanceV3#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#update RdsInstanceV3#update}.
        '''
        value = RdsInstanceV3Timeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        *,
        size: jsii.Number,
        type: builtins.str,
        disk_encryption_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#size RdsInstanceV3#size}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.
        '''
        value = RdsInstanceV3Volume(
            size=size, type=type, disk_encryption_id=disk_encryption_id
        )

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetBackupStrategy")
    def reset_backup_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupStrategy", []))

    @jsii.member(jsii_name="resetHaReplicationMode")
    def reset_ha_replication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaReplicationMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetParamGroupId")
    def reset_param_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParamGroupId", []))

    @jsii.member(jsii_name="resetPublicIps")
    def reset_public_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIps", []))

    @jsii.member(jsii_name="resetRestorePoint")
    def reset_restore_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePoint", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="backupStrategy")
    def backup_strategy(self) -> "RdsInstanceV3BackupStrategyOutputReference":
        return typing.cast("RdsInstanceV3BackupStrategyOutputReference", jsii.get(self, "backupStrategy"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="db")
    def db(self) -> "RdsInstanceV3DbOutputReference":
        return typing.cast("RdsInstanceV3DbOutputReference", jsii.get(self, "db"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "RdsInstanceV3NodesList":
        return typing.cast("RdsInstanceV3NodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="privateIps")
    def private_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIps"))

    @builtins.property
    @jsii.member(jsii_name="restorePoint")
    def restore_point(self) -> "RdsInstanceV3RestorePointOutputReference":
        return typing.cast("RdsInstanceV3RestorePointOutputReference", jsii.get(self, "restorePoint"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RdsInstanceV3TimeoutsOutputReference":
        return typing.cast("RdsInstanceV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "RdsInstanceV3VolumeOutputReference":
        return typing.cast("RdsInstanceV3VolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategyInput")
    def backup_strategy_input(self) -> typing.Optional["RdsInstanceV3BackupStrategy"]:
        return typing.cast(typing.Optional["RdsInstanceV3BackupStrategy"], jsii.get(self, "backupStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="dbInput")
    def db_input(self) -> typing.Optional["RdsInstanceV3Db"]:
        return typing.cast(typing.Optional["RdsInstanceV3Db"], jsii.get(self, "dbInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="haReplicationModeInput")
    def ha_replication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haReplicationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="paramGroupIdInput")
    def param_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpsInput")
    def public_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInput")
    def restore_point_input(self) -> typing.Optional["RdsInstanceV3RestorePoint"]:
        return typing.cast(typing.Optional["RdsInstanceV3RestorePoint"], jsii.get(self, "restorePointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["RdsInstanceV3Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["RdsInstanceV3Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["RdsInstanceV3Volume"]:
        return typing.cast(typing.Optional["RdsInstanceV3Volume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value)

    @builtins.property
    @jsii.member(jsii_name="haReplicationMode")
    def ha_replication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haReplicationMode"))

    @ha_replication_mode.setter
    def ha_replication_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haReplicationMode", value)

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
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="paramGroupId")
    def param_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paramGroupId"))

    @param_group_id.setter
    def param_group_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paramGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="publicIps")
    def public_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIps"))

    @public_ips.setter
    def public_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIps", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

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

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3BackupStrategy",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime", "keep_days": "keepDays"},
)
class RdsInstanceV3BackupStrategy:
    def __init__(
        self,
        *,
        start_time: builtins.str,
        keep_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#start_time RdsInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.
        '''
        if __debug__:
            def stub(
                *,
                start_time: builtins.str,
                keep_days: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument keep_days", value=keep_days, expected_type=type_hints["keep_days"])
        self._values: typing.Dict[str, typing.Any] = {
            "start_time": start_time,
        }
        if keep_days is not None:
            self._values["keep_days"] = keep_days

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#start_time RdsInstanceV3#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.'''
        result = self._values.get("keep_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3BackupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3BackupStrategyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3BackupStrategyOutputReference",
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

    @jsii.member(jsii_name="resetKeepDays")
    def reset_keep_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepDays", []))

    @builtins.property
    @jsii.member(jsii_name="keepDaysInput")
    def keep_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepDays")
    def keep_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepDays"))

    @keep_days.setter
    def keep_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepDays", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3BackupStrategy]:
        return typing.cast(typing.Optional[RdsInstanceV3BackupStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV3BackupStrategy],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV3BackupStrategy]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Config",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "db": "db",
        "flavor": "flavor",
        "name": "name",
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "volume": "volume",
        "vpc_id": "vpcId",
        "backup_strategy": "backupStrategy",
        "ha_replication_mode": "haReplicationMode",
        "id": "id",
        "parameters": "parameters",
        "param_group_id": "paramGroupId",
        "public_ips": "publicIps",
        "restore_point": "restorePoint",
        "tag": "tag",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class RdsInstanceV3Config(cdktf.TerraformMetaArguments):
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
        availability_zone: typing.Sequence[builtins.str],
        db: typing.Union["RdsInstanceV3Db", typing.Dict[str, typing.Any]],
        flavor: builtins.str,
        name: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        volume: typing.Union["RdsInstanceV3Volume", typing.Dict[str, typing.Any]],
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union[RdsInstanceV3BackupStrategy, typing.Dict[str, typing.Any]]] = None,
        ha_replication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        param_group_id: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[str, typing.Any]]] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.
        :param db: db block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#db RdsInstanceV3#db}
        :param flavor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#flavor RdsInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#name RdsInstanceV3#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#volume RdsInstanceV3#volume}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        :param ha_replication_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#id RdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#parameters RdsInstanceV3#parameters}.
        :param param_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.
        :param public_ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.
        :param restore_point: restore_point block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        :param tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tag RdsInstanceV3#tag}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tags RdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(db, dict):
            db = RdsInstanceV3Db(**db)
        if isinstance(volume, dict):
            volume = RdsInstanceV3Volume(**volume)
        if isinstance(backup_strategy, dict):
            backup_strategy = RdsInstanceV3BackupStrategy(**backup_strategy)
        if isinstance(restore_point, dict):
            restore_point = RdsInstanceV3RestorePoint(**restore_point)
        if isinstance(timeouts, dict):
            timeouts = RdsInstanceV3Timeouts(**timeouts)
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
                availability_zone: typing.Sequence[builtins.str],
                db: typing.Union["RdsInstanceV3Db", typing.Dict[str, typing.Any]],
                flavor: builtins.str,
                name: builtins.str,
                security_group_id: builtins.str,
                subnet_id: builtins.str,
                volume: typing.Union["RdsInstanceV3Volume", typing.Dict[str, typing.Any]],
                vpc_id: builtins.str,
                backup_strategy: typing.Optional[typing.Union[RdsInstanceV3BackupStrategy, typing.Dict[str, typing.Any]]] = None,
                ha_replication_mode: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                param_group_id: typing.Optional[builtins.str] = None,
                public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
                restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[str, typing.Any]]] = None,
                tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument backup_strategy", value=backup_strategy, expected_type=type_hints["backup_strategy"])
            check_type(argname="argument ha_replication_mode", value=ha_replication_mode, expected_type=type_hints["ha_replication_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument param_group_id", value=param_group_id, expected_type=type_hints["param_group_id"])
            check_type(argname="argument public_ips", value=public_ips, expected_type=type_hints["public_ips"])
            check_type(argname="argument restore_point", value=restore_point, expected_type=type_hints["restore_point"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zone": availability_zone,
            "db": db,
            "flavor": flavor,
            "name": name,
            "security_group_id": security_group_id,
            "subnet_id": subnet_id,
            "volume": volume,
            "vpc_id": vpc_id,
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
        if backup_strategy is not None:
            self._values["backup_strategy"] = backup_strategy
        if ha_replication_mode is not None:
            self._values["ha_replication_mode"] = ha_replication_mode
        if id is not None:
            self._values["id"] = id
        if parameters is not None:
            self._values["parameters"] = parameters
        if param_group_id is not None:
            self._values["param_group_id"] = param_group_id
        if public_ips is not None:
            self._values["public_ips"] = public_ips
        if restore_point is not None:
            self._values["restore_point"] = restore_point
        if tag is not None:
            self._values["tag"] = tag
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
    def availability_zone(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db(self) -> "RdsInstanceV3Db":
        '''db block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#db RdsInstanceV3#db}
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast("RdsInstanceV3Db", result)

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#flavor RdsInstanceV3#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#name RdsInstanceV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(self) -> "RdsInstanceV3Volume":
        '''volume block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#volume RdsInstanceV3#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("RdsInstanceV3Volume", result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_strategy(self) -> typing.Optional[RdsInstanceV3BackupStrategy]:
        '''backup_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        '''
        result = self._values.get("backup_strategy")
        return typing.cast(typing.Optional[RdsInstanceV3BackupStrategy], result)

    @builtins.property
    def ha_replication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.'''
        result = self._values.get("ha_replication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#id RdsInstanceV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#parameters RdsInstanceV3#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def param_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.'''
        result = self._values.get("param_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.'''
        result = self._values.get("public_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restore_point(self) -> typing.Optional["RdsInstanceV3RestorePoint"]:
        '''restore_point block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        '''
        result = self._values.get("restore_point")
        return typing.cast(typing.Optional["RdsInstanceV3RestorePoint"], result)

    @builtins.property
    def tag(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tag RdsInstanceV3#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#tags RdsInstanceV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RdsInstanceV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RdsInstanceV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Db",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "port": "port",
        "type": "type",
        "version": "version",
    },
)
class RdsInstanceV3Db:
    def __init__(
        self,
        *,
        password: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#password RdsInstanceV3#password}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#port RdsInstanceV3#port}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#version RdsInstanceV3#version}.
        '''
        if __debug__:
            def stub(
                *,
                password: builtins.str,
                port: typing.Optional[jsii.Number] = None,
                type: typing.Optional[builtins.str] = None,
                version: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
        }
        if port is not None:
            self._values["port"] = port
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#password RdsInstanceV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#port RdsInstanceV3#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#version RdsInstanceV3#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Db(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3DbOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3DbOutputReference",
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

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

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
    def internal_value(self) -> typing.Optional[RdsInstanceV3Db]:
        return typing.cast(typing.Optional[RdsInstanceV3Db], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Db]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV3Db]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Nodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class RdsInstanceV3Nodes:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Nodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3NodesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3NodesList",
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
    def get(self, index: jsii.Number) -> "RdsInstanceV3NodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RdsInstanceV3NodesOutputReference", jsii.invoke(self, "get", [index]))

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


class RdsInstanceV3NodesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3NodesOutputReference",
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
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3Nodes]:
        return typing.cast(typing.Optional[RdsInstanceV3Nodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Nodes]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV3Nodes]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestorePoint",
    jsii_struct_bases=[],
    name_mapping={
        "instance_id": "instanceId",
        "backup_id": "backupId",
        "restore_time": "restoreTime",
    },
)
class RdsInstanceV3RestorePoint:
    def __init__(
        self,
        *,
        instance_id: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.
        :param backup_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        if __debug__:
            def stub(
                *,
                instance_id: builtins.str,
                backup_id: typing.Optional[builtins.str] = None,
                restore_time: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument restore_time", value=restore_time, expected_type=type_hints["restore_time"])
        self._values: typing.Dict[str, typing.Any] = {
            "instance_id": instance_id,
        }
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if restore_time is not None:
            self._values["restore_time"] = restore_time

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.'''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.'''
        result = self._values.get("restore_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3RestorePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3RestorePointOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestorePointOutputReference",
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

    @jsii.member(jsii_name="resetBackupId")
    def reset_backup_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupId", []))

    @jsii.member(jsii_name="resetRestoreTime")
    def reset_restore_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreTime", []))

    @builtins.property
    @jsii.member(jsii_name="backupIdInput")
    def backup_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreTimeInput")
    def restore_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "restoreTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupId"))

    @backup_id.setter
    def backup_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupId", value)

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)

    @builtins.property
    @jsii.member(jsii_name="restoreTime")
    def restore_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "restoreTime"))

    @restore_time.setter
    def restore_time(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3RestorePoint]:
        return typing.cast(typing.Optional[RdsInstanceV3RestorePoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3RestorePoint]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV3RestorePoint]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class RdsInstanceV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#create RdsInstanceV3#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#update RdsInstanceV3#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#create RdsInstanceV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#update RdsInstanceV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[RdsInstanceV3Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[RdsInstanceV3Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[RdsInstanceV3Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[RdsInstanceV3Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Volume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "type": "type",
        "disk_encryption_id": "diskEncryptionId",
    },
)
class RdsInstanceV3Volume:
    def __init__(
        self,
        *,
        size: jsii.Number,
        type: builtins.str,
        disk_encryption_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#size RdsInstanceV3#size}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.
        '''
        if __debug__:
            def stub(
                *,
                size: jsii.Number,
                type: builtins.str,
                disk_encryption_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument disk_encryption_id", value=disk_encryption_id, expected_type=type_hints["disk_encryption_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "size": size,
            "type": type,
        }
        if disk_encryption_id is not None:
            self._values["disk_encryption_id"] = disk_encryption_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#size RdsInstanceV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#type RdsInstanceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.'''
        result = self._values.get("disk_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Volume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3VolumeOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3VolumeOutputReference",
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

    @jsii.member(jsii_name="resetDiskEncryptionId")
    def reset_disk_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionId", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionIdInput")
    def disk_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionId")
    def disk_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionId"))

    @disk_encryption_id.setter
    def disk_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionId", value)

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
    def internal_value(self) -> typing.Optional[RdsInstanceV3Volume]:
        return typing.cast(typing.Optional[RdsInstanceV3Volume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Volume]) -> None:
        if __debug__:
            def stub(value: typing.Optional[RdsInstanceV3Volume]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "RdsInstanceV3",
    "RdsInstanceV3BackupStrategy",
    "RdsInstanceV3BackupStrategyOutputReference",
    "RdsInstanceV3Config",
    "RdsInstanceV3Db",
    "RdsInstanceV3DbOutputReference",
    "RdsInstanceV3Nodes",
    "RdsInstanceV3NodesList",
    "RdsInstanceV3NodesOutputReference",
    "RdsInstanceV3RestorePoint",
    "RdsInstanceV3RestorePointOutputReference",
    "RdsInstanceV3Timeouts",
    "RdsInstanceV3TimeoutsOutputReference",
    "RdsInstanceV3Volume",
    "RdsInstanceV3VolumeOutputReference",
]

publication.publish()
