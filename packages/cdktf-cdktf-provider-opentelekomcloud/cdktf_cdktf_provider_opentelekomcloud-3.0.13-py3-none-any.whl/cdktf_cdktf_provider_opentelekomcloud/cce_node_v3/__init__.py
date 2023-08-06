'''
# `opentelekomcloud_cce_node_v3`

Refer to the Terraform Registory for docs: [`opentelekomcloud_cce_node_v3`](https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3).
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


class CceNodeV3(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3 opentelekomcloud_cce_node_v3}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        cluster_id: builtins.str,
        data_volumes: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
        flavor_id: builtins.str,
        key_pair: builtins.str,
        root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        ecs_performance_type: typing.Optional[builtins.str] = None,
        eip_count: typing.Optional[jsii.Number] = None,
        eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        extend_param_charging_mode: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iptype: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sharetype: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3 opentelekomcloud_cce_node_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#availability_zone CceNodeV3#availability_zone}.
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#cluster_id CceNodeV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        :param flavor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#flavor_id CceNodeV3#flavor_id}.
        :param key_pair: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#key_pair CceNodeV3#key_pair}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#root_volume CceNodeV3#root_volume}
        :param annotations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#annotations CceNodeV3#annotations}.
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.
        :param billing_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#billing_mode CceNodeV3#billing_mode}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.
        :param ecs_performance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.
        :param eip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_count CceNodeV3#eip_count}.
        :param eip_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_ids CceNodeV3#eip_ids}.
        :param extend_param_charging_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#id CceNodeV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iptype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#iptype CceNodeV3#iptype}.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.
        :param labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#labels CceNodeV3#labels}.
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#max_pods CceNodeV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#name CceNodeV3#name}.
        :param order_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#order_id CceNodeV3#order_id}.
        :param os: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#os CceNodeV3#os}.
        :param postinstall: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#postinstall CceNodeV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#preinstall CceNodeV3#preinstall}.
        :param private_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#private_ip CceNodeV3#private_ip}.
        :param product_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#product_id CceNodeV3#product_id}.
        :param public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#public_key CceNodeV3#public_key}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#region CceNodeV3#region}.
        :param sharetype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#sharetype CceNodeV3#sharetype}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#subnet_id CceNodeV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#tags CceNodeV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#taints CceNodeV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#timeouts CceNodeV3#timeouts}
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
                availability_zone: builtins.str,
                cluster_id: builtins.str,
                data_volumes: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
                flavor_id: builtins.str,
                key_pair: builtins.str,
                root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[str, typing.Any]],
                annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                bandwidth_charge_mode: typing.Optional[builtins.str] = None,
                bandwidth_size: typing.Optional[jsii.Number] = None,
                billing_mode: typing.Optional[jsii.Number] = None,
                docker_base_size: typing.Optional[jsii.Number] = None,
                docker_lvm_config_override: typing.Optional[builtins.str] = None,
                ecs_performance_type: typing.Optional[builtins.str] = None,
                eip_count: typing.Optional[jsii.Number] = None,
                eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                extend_param_charging_mode: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                iptype: typing.Optional[builtins.str] = None,
                k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                max_pods: typing.Optional[jsii.Number] = None,
                name: typing.Optional[builtins.str] = None,
                order_id: typing.Optional[builtins.str] = None,
                os: typing.Optional[builtins.str] = None,
                postinstall: typing.Optional[builtins.str] = None,
                preinstall: typing.Optional[builtins.str] = None,
                private_ip: typing.Optional[builtins.str] = None,
                product_id: typing.Optional[builtins.str] = None,
                public_key: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                sharetype: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                taints: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = CceNodeV3Config(
            availability_zone=availability_zone,
            cluster_id=cluster_id,
            data_volumes=data_volumes,
            flavor_id=flavor_id,
            key_pair=key_pair,
            root_volume=root_volume,
            annotations=annotations,
            bandwidth_charge_mode=bandwidth_charge_mode,
            bandwidth_size=bandwidth_size,
            billing_mode=billing_mode,
            docker_base_size=docker_base_size,
            docker_lvm_config_override=docker_lvm_config_override,
            ecs_performance_type=ecs_performance_type,
            eip_count=eip_count,
            eip_ids=eip_ids,
            extend_param_charging_mode=extend_param_charging_mode,
            id=id,
            iptype=iptype,
            k8_s_tags=k8_s_tags,
            labels=labels,
            max_pods=max_pods,
            name=name,
            order_id=order_id,
            os=os,
            postinstall=postinstall,
            preinstall=preinstall,
            private_ip=private_ip,
            product_id=product_id,
            public_key=public_key,
            region=region,
            sharetype=sharetype,
            subnet_id=subnet_id,
            tags=tags,
            taints=taints,
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

    @jsii.member(jsii_name="putDataVolumes")
    def put_data_volumes(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataVolumes", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param kms_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        value = CceNodeV3RootVolume(
            size=size, volumetype=volumetype, extend_param=extend_param, kms_id=kms_id
        )

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#create CceNodeV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#delete CceNodeV3#delete}.
        '''
        value = CceNodeV3Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBandwidthChargeMode")
    def reset_bandwidth_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthChargeMode", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetBillingMode")
    def reset_billing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingMode", []))

    @jsii.member(jsii_name="resetDockerBaseSize")
    def reset_docker_base_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerBaseSize", []))

    @jsii.member(jsii_name="resetDockerLvmConfigOverride")
    def reset_docker_lvm_config_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerLvmConfigOverride", []))

    @jsii.member(jsii_name="resetEcsPerformanceType")
    def reset_ecs_performance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsPerformanceType", []))

    @jsii.member(jsii_name="resetEipCount")
    def reset_eip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEipCount", []))

    @jsii.member(jsii_name="resetEipIds")
    def reset_eip_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEipIds", []))

    @jsii.member(jsii_name="resetExtendParamChargingMode")
    def reset_extend_param_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParamChargingMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIptype")
    def reset_iptype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIptype", []))

    @jsii.member(jsii_name="resetK8STags")
    def reset_k8_s_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetK8STags", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOrderId")
    def reset_order_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderId", []))

    @jsii.member(jsii_name="resetOs")
    def reset_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOs", []))

    @jsii.member(jsii_name="resetPostinstall")
    def reset_postinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostinstall", []))

    @jsii.member(jsii_name="resetPreinstall")
    def reset_preinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreinstall", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetProductId")
    def reset_product_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductId", []))

    @jsii.member(jsii_name="resetPublicKey")
    def reset_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSharetype")
    def reset_sharetype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharetype", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

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
    @jsii.member(jsii_name="dataVolumes")
    def data_volumes(self) -> "CceNodeV3DataVolumesList":
        return typing.cast("CceNodeV3DataVolumesList", jsii.get(self, "dataVolumes"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "CceNodeV3RootVolumeOutputReference":
        return typing.cast("CceNodeV3RootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "CceNodeV3TaintsList":
        return typing.cast("CceNodeV3TaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CceNodeV3TimeoutsOutputReference":
        return typing.cast("CceNodeV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeModeInput")
    def bandwidth_charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthChargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="billingModeInput")
    def billing_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "billingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataVolumesInput")
    def data_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3DataVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3DataVolumes"]]], jsii.get(self, "dataVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSizeInput")
    def docker_base_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerBaseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverrideInput")
    def docker_lvm_config_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerLvmConfigOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsPerformanceTypeInput")
    def ecs_performance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ecsPerformanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="eipCountInput")
    def eip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eipCountInput"))

    @builtins.property
    @jsii.member(jsii_name="eipIdsInput")
    def eip_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eipIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParamChargingModeInput")
    def extend_param_charging_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "extendParamChargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iptypeInput")
    def iptype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iptypeInput"))

    @builtins.property
    @jsii.member(jsii_name="k8STagsInput")
    def k8_s_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "k8STagsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderIdInput")
    def order_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="postinstallInput")
    def postinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="preinstallInput")
    def preinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(self) -> typing.Optional["CceNodeV3RootVolume"]:
        return typing.cast(typing.Optional["CceNodeV3RootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="sharetypeInput")
    def sharetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3Taints"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3Taints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CceNodeV3Timeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CceNodeV3Timeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @bandwidth_charge_mode.setter
    def bandwidth_charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthChargeMode", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value)

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
    @jsii.member(jsii_name="dockerBaseSize")
    def docker_base_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerBaseSize"))

    @docker_base_size.setter
    def docker_base_size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerBaseSize", value)

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverride")
    def docker_lvm_config_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerLvmConfigOverride"))

    @docker_lvm_config_override.setter
    def docker_lvm_config_override(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerLvmConfigOverride", value)

    @builtins.property
    @jsii.member(jsii_name="ecsPerformanceType")
    def ecs_performance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsPerformanceType"))

    @ecs_performance_type.setter
    def ecs_performance_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecsPerformanceType", value)

    @builtins.property
    @jsii.member(jsii_name="eipCount")
    def eip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eipCount"))

    @eip_count.setter
    def eip_count(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eipCount", value)

    @builtins.property
    @jsii.member(jsii_name="eipIds")
    def eip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eipIds"))

    @eip_ids.setter
    def eip_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eipIds", value)

    @builtins.property
    @jsii.member(jsii_name="extendParamChargingMode")
    def extend_param_charging_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "extendParamChargingMode"))

    @extend_param_charging_mode.setter
    def extend_param_charging_mode(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParamChargingMode", value)

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value)

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
    @jsii.member(jsii_name="iptype")
    def iptype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iptype"))

    @iptype.setter
    def iptype(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iptype", value)

    @builtins.property
    @jsii.member(jsii_name="k8STags")
    def k8_s_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "k8STags"))

    @k8_s_tags.setter
    def k8_s_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "k8STags", value)

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value)

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
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @order_id.setter
    def order_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderId", value)

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value)

    @builtins.property
    @jsii.member(jsii_name="postinstall")
    def postinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postinstall"))

    @postinstall.setter
    def postinstall(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postinstall", value)

    @builtins.property
    @jsii.member(jsii_name="preinstall")
    def preinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preinstall"))

    @preinstall.setter
    def preinstall(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preinstall", value)

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value)

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
    @jsii.member(jsii_name="sharetype")
    def sharetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharetype"))

    @sharetype.setter
    def sharetype(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharetype", value)

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
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Config",
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
        "cluster_id": "clusterId",
        "data_volumes": "dataVolumes",
        "flavor_id": "flavorId",
        "key_pair": "keyPair",
        "root_volume": "rootVolume",
        "annotations": "annotations",
        "bandwidth_charge_mode": "bandwidthChargeMode",
        "bandwidth_size": "bandwidthSize",
        "billing_mode": "billingMode",
        "docker_base_size": "dockerBaseSize",
        "docker_lvm_config_override": "dockerLvmConfigOverride",
        "ecs_performance_type": "ecsPerformanceType",
        "eip_count": "eipCount",
        "eip_ids": "eipIds",
        "extend_param_charging_mode": "extendParamChargingMode",
        "id": "id",
        "iptype": "iptype",
        "k8_s_tags": "k8STags",
        "labels": "labels",
        "max_pods": "maxPods",
        "name": "name",
        "order_id": "orderId",
        "os": "os",
        "postinstall": "postinstall",
        "preinstall": "preinstall",
        "private_ip": "privateIp",
        "product_id": "productId",
        "public_key": "publicKey",
        "region": "region",
        "sharetype": "sharetype",
        "subnet_id": "subnetId",
        "tags": "tags",
        "taints": "taints",
        "timeouts": "timeouts",
    },
)
class CceNodeV3Config(cdktf.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        cluster_id: builtins.str,
        data_volumes: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
        flavor_id: builtins.str,
        key_pair: builtins.str,
        root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        ecs_performance_type: typing.Optional[builtins.str] = None,
        eip_count: typing.Optional[jsii.Number] = None,
        eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        extend_param_charging_mode: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iptype: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sharetype: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#availability_zone CceNodeV3#availability_zone}.
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#cluster_id CceNodeV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        :param flavor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#flavor_id CceNodeV3#flavor_id}.
        :param key_pair: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#key_pair CceNodeV3#key_pair}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#root_volume CceNodeV3#root_volume}
        :param annotations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#annotations CceNodeV3#annotations}.
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.
        :param billing_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#billing_mode CceNodeV3#billing_mode}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.
        :param ecs_performance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.
        :param eip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_count CceNodeV3#eip_count}.
        :param eip_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_ids CceNodeV3#eip_ids}.
        :param extend_param_charging_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#id CceNodeV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iptype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#iptype CceNodeV3#iptype}.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.
        :param labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#labels CceNodeV3#labels}.
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#max_pods CceNodeV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#name CceNodeV3#name}.
        :param order_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#order_id CceNodeV3#order_id}.
        :param os: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#os CceNodeV3#os}.
        :param postinstall: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#postinstall CceNodeV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#preinstall CceNodeV3#preinstall}.
        :param private_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#private_ip CceNodeV3#private_ip}.
        :param product_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#product_id CceNodeV3#product_id}.
        :param public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#public_key CceNodeV3#public_key}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#region CceNodeV3#region}.
        :param sharetype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#sharetype CceNodeV3#sharetype}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#subnet_id CceNodeV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#tags CceNodeV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#taints CceNodeV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#timeouts CceNodeV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(root_volume, dict):
            root_volume = CceNodeV3RootVolume(**root_volume)
        if isinstance(timeouts, dict):
            timeouts = CceNodeV3Timeouts(**timeouts)
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
                availability_zone: builtins.str,
                cluster_id: builtins.str,
                data_volumes: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[str, typing.Any]]]],
                flavor_id: builtins.str,
                key_pair: builtins.str,
                root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[str, typing.Any]],
                annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                bandwidth_charge_mode: typing.Optional[builtins.str] = None,
                bandwidth_size: typing.Optional[jsii.Number] = None,
                billing_mode: typing.Optional[jsii.Number] = None,
                docker_base_size: typing.Optional[jsii.Number] = None,
                docker_lvm_config_override: typing.Optional[builtins.str] = None,
                ecs_performance_type: typing.Optional[builtins.str] = None,
                eip_count: typing.Optional[jsii.Number] = None,
                eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                extend_param_charging_mode: typing.Optional[jsii.Number] = None,
                id: typing.Optional[builtins.str] = None,
                iptype: typing.Optional[builtins.str] = None,
                k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                max_pods: typing.Optional[jsii.Number] = None,
                name: typing.Optional[builtins.str] = None,
                order_id: typing.Optional[builtins.str] = None,
                os: typing.Optional[builtins.str] = None,
                postinstall: typing.Optional[builtins.str] = None,
                preinstall: typing.Optional[builtins.str] = None,
                private_ip: typing.Optional[builtins.str] = None,
                product_id: typing.Optional[builtins.str] = None,
                public_key: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                sharetype: typing.Optional[builtins.str] = None,
                subnet_id: typing.Optional[builtins.str] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                taints: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument data_volumes", value=data_volumes, expected_type=type_hints["data_volumes"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument bandwidth_charge_mode", value=bandwidth_charge_mode, expected_type=type_hints["bandwidth_charge_mode"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument docker_base_size", value=docker_base_size, expected_type=type_hints["docker_base_size"])
            check_type(argname="argument docker_lvm_config_override", value=docker_lvm_config_override, expected_type=type_hints["docker_lvm_config_override"])
            check_type(argname="argument ecs_performance_type", value=ecs_performance_type, expected_type=type_hints["ecs_performance_type"])
            check_type(argname="argument eip_count", value=eip_count, expected_type=type_hints["eip_count"])
            check_type(argname="argument eip_ids", value=eip_ids, expected_type=type_hints["eip_ids"])
            check_type(argname="argument extend_param_charging_mode", value=extend_param_charging_mode, expected_type=type_hints["extend_param_charging_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iptype", value=iptype, expected_type=type_hints["iptype"])
            check_type(argname="argument k8_s_tags", value=k8_s_tags, expected_type=type_hints["k8_s_tags"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order_id", value=order_id, expected_type=type_hints["order_id"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument postinstall", value=postinstall, expected_type=type_hints["postinstall"])
            check_type(argname="argument preinstall", value=preinstall, expected_type=type_hints["preinstall"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sharetype", value=sharetype, expected_type=type_hints["sharetype"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zone": availability_zone,
            "cluster_id": cluster_id,
            "data_volumes": data_volumes,
            "flavor_id": flavor_id,
            "key_pair": key_pair,
            "root_volume": root_volume,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if bandwidth_charge_mode is not None:
            self._values["bandwidth_charge_mode"] = bandwidth_charge_mode
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if docker_base_size is not None:
            self._values["docker_base_size"] = docker_base_size
        if docker_lvm_config_override is not None:
            self._values["docker_lvm_config_override"] = docker_lvm_config_override
        if ecs_performance_type is not None:
            self._values["ecs_performance_type"] = ecs_performance_type
        if eip_count is not None:
            self._values["eip_count"] = eip_count
        if eip_ids is not None:
            self._values["eip_ids"] = eip_ids
        if extend_param_charging_mode is not None:
            self._values["extend_param_charging_mode"] = extend_param_charging_mode
        if id is not None:
            self._values["id"] = id
        if iptype is not None:
            self._values["iptype"] = iptype
        if k8_s_tags is not None:
            self._values["k8_s_tags"] = k8_s_tags
        if labels is not None:
            self._values["labels"] = labels
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if name is not None:
            self._values["name"] = name
        if order_id is not None:
            self._values["order_id"] = order_id
        if os is not None:
            self._values["os"] = os
        if postinstall is not None:
            self._values["postinstall"] = postinstall
        if preinstall is not None:
            self._values["preinstall"] = preinstall
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if product_id is not None:
            self._values["product_id"] = product_id
        if public_key is not None:
            self._values["public_key"] = public_key
        if region is not None:
            self._values["region"] = region
        if sharetype is not None:
            self._values["sharetype"] = sharetype
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints
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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#availability_zone CceNodeV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#cluster_id CceNodeV3#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_volumes(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["CceNodeV3DataVolumes"]]:
        '''data_volumes block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        '''
        result = self._values.get("data_volumes")
        assert result is not None, "Required property 'data_volumes' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["CceNodeV3DataVolumes"]], result)

    @builtins.property
    def flavor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#flavor_id CceNodeV3#flavor_id}.'''
        result = self._values.get("flavor_id")
        assert result is not None, "Required property 'flavor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_pair(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#key_pair CceNodeV3#key_pair}.'''
        result = self._values.get("key_pair")
        assert result is not None, "Required property 'key_pair' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_volume(self) -> "CceNodeV3RootVolume":
        '''root_volume block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#root_volume CceNodeV3#root_volume}
        '''
        result = self._values.get("root_volume")
        assert result is not None, "Required property 'root_volume' is missing"
        return typing.cast("CceNodeV3RootVolume", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#annotations CceNodeV3#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bandwidth_charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.'''
        result = self._values.get("bandwidth_charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#billing_mode CceNodeV3#billing_mode}.'''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_base_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.'''
        result = self._values.get("docker_base_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_lvm_config_override(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.'''
        result = self._values.get("docker_lvm_config_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs_performance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.'''
        result = self._values.get("ecs_performance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eip_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_count CceNodeV3#eip_count}.'''
        result = self._values.get("eip_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#eip_ids CceNodeV3#eip_ids}.'''
        result = self._values.get("eip_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extend_param_charging_mode(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.'''
        result = self._values.get("extend_param_charging_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#id CceNodeV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iptype(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#iptype CceNodeV3#iptype}.'''
        result = self._values.get("iptype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def k8_s_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.'''
        result = self._values.get("k8_s_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#labels CceNodeV3#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#max_pods CceNodeV3#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#name CceNodeV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#order_id CceNodeV3#order_id}.'''
        result = self._values.get("order_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#os CceNodeV3#os}.'''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#postinstall CceNodeV3#postinstall}.'''
        result = self._values.get("postinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#preinstall CceNodeV3#preinstall}.'''
        result = self._values.get("preinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#private_ip CceNodeV3#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#product_id CceNodeV3#product_id}.'''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#public_key CceNodeV3#public_key}.'''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#region CceNodeV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharetype(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#sharetype CceNodeV3#sharetype}.'''
        result = self._values.get("sharetype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#subnet_id CceNodeV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#tags CceNodeV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3Taints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#taints CceNodeV3#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CceNodeV3Taints"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CceNodeV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#timeouts CceNodeV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CceNodeV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "kms_id": "kmsId",
    },
)
class CceNodeV3DataVolumes:
    def __init__(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param kms_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        if __debug__:
            def stub(
                *,
                size: jsii.Number,
                volumetype: builtins.str,
                extend_param: typing.Optional[builtins.str] = None,
                kms_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volumetype", value=volumetype, expected_type=type_hints["volumetype"])
            check_type(argname="argument extend_param", value=extend_param, expected_type=type_hints["extend_param"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "size": size,
            "volumetype": volumetype,
        }
        if extend_param is not None:
            self._values["extend_param"] = extend_param
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#size CceNodeV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#volumetype CceNodeV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param CceNodeV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#kms_id CceNodeV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3DataVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3DataVolumesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumesList",
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
    def get(self, index: jsii.Number) -> "CceNodeV3DataVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeV3DataVolumesOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3DataVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3DataVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3DataVolumes]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3DataVolumes]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CceNodeV3DataVolumesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumesOutputReference",
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

    @jsii.member(jsii_name="resetExtendParam")
    def reset_extend_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParam", []))

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="extendParamInput")
    def extend_param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendParamInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumetypeInput")
    def volumetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @extend_param.setter
    def extend_param(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value)

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
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CceNodeV3DataVolumes, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CceNodeV3DataVolumes, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CceNodeV3DataVolumes, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CceNodeV3DataVolumes, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3RootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "kms_id": "kmsId",
    },
)
class CceNodeV3RootVolume:
    def __init__(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param kms_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        if __debug__:
            def stub(
                *,
                size: jsii.Number,
                volumetype: builtins.str,
                extend_param: typing.Optional[builtins.str] = None,
                kms_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volumetype", value=volumetype, expected_type=type_hints["volumetype"])
            check_type(argname="argument extend_param", value=extend_param, expected_type=type_hints["extend_param"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "size": size,
            "volumetype": volumetype,
        }
        if extend_param is not None:
            self._values["extend_param"] = extend_param
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#size CceNodeV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#volumetype CceNodeV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#extend_param CceNodeV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#kms_id CceNodeV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3RootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3RootVolumeOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3RootVolumeOutputReference",
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

    @jsii.member(jsii_name="resetExtendParam")
    def reset_extend_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParam", []))

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="extendParamInput")
    def extend_param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendParamInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumetypeInput")
    def volumetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @extend_param.setter
    def extend_param(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value)

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
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodeV3RootVolume]:
        return typing.cast(typing.Optional[CceNodeV3RootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CceNodeV3RootVolume]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CceNodeV3RootVolume]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Taints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class CceNodeV3Taints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#effect CceNodeV3#effect}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#key CceNodeV3#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#value CceNodeV3#value}.
        '''
        if __debug__:
            def stub(
                *,
                effect: builtins.str,
                key: builtins.str,
                value: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#effect CceNodeV3#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#key CceNodeV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#value CceNodeV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Taints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3TaintsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TaintsList",
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
    def get(self, index: jsii.Number) -> "CceNodeV3TaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeV3TaintsOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3Taints]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3Taints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3Taints]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CceNodeV3Taints]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CceNodeV3TaintsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TaintsOutputReference",
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
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

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
    ) -> typing.Optional[typing.Union[CceNodeV3Taints, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CceNodeV3Taints, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CceNodeV3Taints, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CceNodeV3Taints, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CceNodeV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#create CceNodeV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#delete CceNodeV3#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#create CceNodeV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/opentelekomcloud/r/cce_node_v3#delete CceNodeV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3TimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[CceNodeV3Timeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CceNodeV3Timeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CceNodeV3Timeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CceNodeV3Timeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CceNodeV3",
    "CceNodeV3Config",
    "CceNodeV3DataVolumes",
    "CceNodeV3DataVolumesList",
    "CceNodeV3DataVolumesOutputReference",
    "CceNodeV3RootVolume",
    "CceNodeV3RootVolumeOutputReference",
    "CceNodeV3Taints",
    "CceNodeV3TaintsList",
    "CceNodeV3TaintsOutputReference",
    "CceNodeV3Timeouts",
    "CceNodeV3TimeoutsOutputReference",
]

publication.publish()
