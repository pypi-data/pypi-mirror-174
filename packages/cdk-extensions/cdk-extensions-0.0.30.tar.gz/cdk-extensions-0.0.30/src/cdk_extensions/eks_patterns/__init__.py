'''
# Vibe-io CDK-Extensions EC2 Construct Library

The `cdk-extensions/eks-patterns` module contains higher-level Amazon EKS constructs which follow common architectural patterns. It constains:

* Cluster Integrated with Common AWS Services

## Cluster Integrated with Common AWS Services

To define an EKS cluster that comes pre-installed with common services many Kubernetes clusters running on AWS will use, instantiate one of the following:

* AwsIntegratedFargateCluster

```
declare const vpc: ec2.Vpc;
const cluster = new eks_patterns.AwsIntegratedFargateCluster(this, 'cluster', {
    version: eks.KubernetesVersion.V1_21,
    vpc: vpc,
    vpcSubnets: [
        {
            onePerAz: true,
            subnetGroupName: 'private'
        }
    ]
});
```

### Integrated Services

#### Route 53

Route 53 integration is provided by means of the [External DNS Kubernetes Add-on](https://github.com/kubernetes-sigs/external-dns). Services and ingresses in the cluster can be discovered and External DNS will manage appropriate DNS records in Route 53.

External DNS is enabled by default and must be explicitly disabled using:

```
const cluster = new eks_patterns.AwsIntegratedFargateCluster(this, 'cluster', {
    externalDnsOptions: {
        enabled: false,
    },
    version: eks.KubernetesVersion.V1_21,
});
```

#### Container Insights

Integration with Container Insights is implemented using [AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/introduction) as described in [this AWS blog post](https://aws.amazon.com/blogs/containers/introducing-amazon-cloudwatch-container-insights-for-amazon-eks-fargate-using-aws-distro-for-opentelemetry/).

This help you collect, aggregate, and visualize advanced metrics from your services running on EKS and Fargate.

Container Insights is enabled by default and must be explicitly disabled using:

```
const cluster = new eks_patterns.AwsIntegratedFargateCluster(this, 'cluster', {
    cloudWatchMonitoringOptions: {
        enabled: false,
    },
    version: eks.KubernetesVersion.V1_21,
});
```

#### CloudWatch Logs

CloudWatch Logs integration is provided using the [built-in log router provided by Fargate](https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html).

Currently this will ship logs for all containers to a CloudWatch log group that can be filtered to find the pods for specific pods and services.

We plan to expand the functionality of this resource to expand log destinations and provide more advanced log filtering.

Container Insights is enabled by default and must be explicitly disabled using:

```
const cluster = new eks_patterns.AwsIntegratedFargateCluster(this, 'cluster', {
    fargateLogger: {
        enabled: false,
    },
    version: eks.KubernetesVersion.V1_21,
});
```

#### Secrets Manager

Integration to Secrets Manager is provided using the [External Secrets Operatore](https://external-secrets.io/) Kubernetes operator.

You can use it to configure links between Secrets Manager secrets (such as those created for RDS instances) and Kubernetes secrets which can be exposed to your pods as environment variables. Changes to the secret in Secrets Manager will automatically be synchronized into the secret in the EKS cluster.

Secrets Manager integration is enabled by default and must be explicitly disabled using:

```
const cluster = new eks_patterns.AwsIntegratedFargateCluster(this, 'cluster', {
    externalSecretsOptions: {
        enabled: false,
    },
    version: eks.KubernetesVersion.V1_21,
});
```
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

import aws_cdk
import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_ssm
import constructs
from ..k8s_aws import (
    CloudWatchMonitoring as _CloudWatchMonitoring_bd5b6f0b,
    ExternalDns as _ExternalDns_941d01d4,
    ExternalSecret as _ExternalSecret_5ca098dd,
    ExternalSecretsOperator as _ExternalSecretsOperator_bac1dfc1,
    FargateLogger as _FargateLogger_f9dab33b,
    NamespacedExternalSecretOptions as _NamespacedExternalSecretOptions_df08c698,
    SecretFieldReference as _SecretFieldReference_5a196607,
)


class AwsIntegratedFargateCluster(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.eks_patterns.AwsIntegratedFargateCluster",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cloud_watch_monitoring_options: typing.Optional[typing.Union["CloudWatchMonitoringOptions", typing.Dict[str, typing.Any]]] = None,
        external_dns_options: typing.Optional[typing.Union["ExternalDnsOptions", typing.Dict[str, typing.Any]]] = None,
        external_secrets_options: typing.Optional[typing.Union["ExternalSecretsOptions", typing.Dict[str, typing.Any]]] = None,
        logging_options: typing.Optional[typing.Union["FargateLoggingOptions", typing.Dict[str, typing.Any]]] = None,
        default_profile: typing.Optional[typing.Union[aws_cdk.aws_eks.FargateProfileOptions, typing.Dict[str, typing.Any]]] = None,
        alb_controller: typing.Optional[typing.Union[aws_cdk.aws_eks.AlbControllerOptions, typing.Dict[str, typing.Any]]] = None,
        cluster_handler_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cluster_handler_security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        cluster_logging: typing.Optional[typing.Sequence[aws_cdk.aws_eks.ClusterLoggingTypes]] = None,
        core_dns_compute_type: typing.Optional[aws_cdk.aws_eks.CoreDnsComputeType] = None,
        endpoint_access: typing.Optional[aws_cdk.aws_eks.EndpointAccess] = None,
        kubectl_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kubectl_layer: typing.Optional[aws_cdk.aws_lambda.ILayerVersion] = None,
        kubectl_memory: typing.Optional[aws_cdk.Size] = None,
        masters_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        on_event_layer: typing.Optional[aws_cdk.aws_lambda.ILayerVersion] = None,
        output_masters_role_arn: typing.Optional[builtins.bool] = None,
        place_cluster_handler_in_vpc: typing.Optional[builtins.bool] = None,
        prune: typing.Optional[builtins.bool] = None,
        secrets_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
        version: aws_cdk.aws_eks.KubernetesVersion,
        cluster_name: typing.Optional[builtins.str] = None,
        output_cluster_name: typing.Optional[builtins.bool] = None,
        output_config_command: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_watch_monitoring_options: 
        :param external_dns_options: 
        :param external_secrets_options: 
        :param logging_options: 
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.
        :param alb_controller: Install the AWS Load Balancer Controller onto the cluster. Default: - The controller is not installed.
        :param cluster_handler_environment: Custom environment variables when interacting with the EKS endpoint to manage the cluster lifecycle. Default: - No environment variables.
        :param cluster_handler_security_group: A security group to associate with the Cluster Handler's Lambdas. The Cluster Handler's Lambdas are responsible for calling AWS's EKS API. Requires ``placeClusterHandlerInVpc`` to be set to true. Default: - No security group.
        :param cluster_logging: The cluster log types which you want to enable. Default: - none
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`), compatibleRuntimes: [lambda.Runtime.PROVIDED], }); Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param kubectl_memory: Amount of memory to allocate to the provider's lambda function. Default: Size.gibibytes(1)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param on_event_layer: An AWS Lambda Layer which includes the NPM dependency ``proxy-agent``. This layer is used by the onEvent handler to route AWS SDK requests through a proxy. By default, the provider will use the layer included in the "aws-lambda-layer-node-proxy-agent" SAR application which is available in all commercial regions. To deploy the layer locally define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'proxy-agent-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`), compatibleRuntimes: [lambda.Runtime.NODEJS_14_X], }); Default: - a layer bundled with this module.
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param place_cluster_handler_in_vpc: If set to true, the cluster handler functions will be placed in the private subnets of the cluster vpc, subject to the ``vpcSubnets`` selection strategy. Default: false
        :param prune: Indicates whether Kubernetes resources added through ``addManifest()`` can be automatically pruned. When this is enabled (default), prune labels will be allocated and injected to each resource. These labels will then be used when issuing the ``kubectl apply`` operation with the ``--prune`` switch. Default: true
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.
        :param service_ipv4_cidr: The CIDR block to assign Kubernetes service IP addresses from. Default: - Kubernetes assigns addresses from either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks
        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following: ``vpcSubnets: [{ subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }]`` Default: - All public and private subnets
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsIntegratedFargateCluster.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsIntegratedFargateClusterProps(
            cloud_watch_monitoring_options=cloud_watch_monitoring_options,
            external_dns_options=external_dns_options,
            external_secrets_options=external_secrets_options,
            logging_options=logging_options,
            default_profile=default_profile,
            alb_controller=alb_controller,
            cluster_handler_environment=cluster_handler_environment,
            cluster_handler_security_group=cluster_handler_security_group,
            cluster_logging=cluster_logging,
            core_dns_compute_type=core_dns_compute_type,
            endpoint_access=endpoint_access,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            kubectl_memory=kubectl_memory,
            masters_role=masters_role,
            on_event_layer=on_event_layer,
            output_masters_role_arn=output_masters_role_arn,
            place_cluster_handler_in_vpc=place_cluster_handler_in_vpc,
            prune=prune,
            secrets_encryption_key=secrets_encryption_key,
            service_ipv4_cidr=service_ipv4_cidr,
            version=version,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            role=role,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="registerSecretsManagerSecret")
    def register_secrets_manager_secret(
        self,
        id: builtins.str,
        secret: aws_cdk.aws_secretsmanager.ISecret,
        *,
        namespace: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[typing.Union[_SecretFieldReference_5a196607, typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> _ExternalSecret_5ca098dd:
        '''
        :param id: -
        :param secret: -
        :param namespace: 
        :param fields: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsIntegratedFargateCluster.register_secrets_manager_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        options = _NamespacedExternalSecretOptions_df08c698(
            namespace=namespace, fields=fields, name=name
        )

        return typing.cast(_ExternalSecret_5ca098dd, jsii.invoke(self, "registerSecretsManagerSecret", [id, secret, options]))

    @jsii.member(jsii_name="registerSsmParameterSecret")
    def register_ssm_parameter_secret(
        self,
        id: builtins.str,
        parameter: aws_cdk.aws_ssm.IParameter,
        *,
        namespace: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[typing.Union[_SecretFieldReference_5a196607, typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> _ExternalSecret_5ca098dd:
        '''
        :param id: -
        :param parameter: -
        :param namespace: 
        :param fields: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsIntegratedFargateCluster.register_ssm_parameter_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        options = _NamespacedExternalSecretOptions_df08c698(
            namespace=namespace, fields=fields, name=name
        )

        return typing.cast(_ExternalSecret_5ca098dd, jsii.invoke(self, "registerSsmParameterSecret", [id, parameter, options]))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_eks.FargateCluster:
        return typing.cast(aws_cdk.aws_eks.FargateCluster, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMonitoring")
    def cloud_watch_monitoring(self) -> typing.Optional[_CloudWatchMonitoring_bd5b6f0b]:
        return typing.cast(typing.Optional[_CloudWatchMonitoring_bd5b6f0b], jsii.get(self, "cloudWatchMonitoring"))

    @builtins.property
    @jsii.member(jsii_name="externalDns")
    def external_dns(self) -> typing.Optional[_ExternalDns_941d01d4]:
        return typing.cast(typing.Optional[_ExternalDns_941d01d4], jsii.get(self, "externalDns"))

    @builtins.property
    @jsii.member(jsii_name="externalSecrets")
    def external_secrets(self) -> typing.Optional[_ExternalSecretsOperator_bac1dfc1]:
        return typing.cast(typing.Optional[_ExternalSecretsOperator_bac1dfc1], jsii.get(self, "externalSecrets"))

    @builtins.property
    @jsii.member(jsii_name="fargateLogger")
    def fargate_logger(self) -> typing.Optional[_FargateLogger_f9dab33b]:
        return typing.cast(typing.Optional[_FargateLogger_f9dab33b], jsii.get(self, "fargateLogger"))


@jsii.data_type(
    jsii_type="cdk-extensions.eks_patterns.AwsIntegratedFargateClusterProps",
    jsii_struct_bases=[aws_cdk.aws_eks.FargateClusterProps],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "alb_controller": "albController",
        "cluster_handler_environment": "clusterHandlerEnvironment",
        "cluster_handler_security_group": "clusterHandlerSecurityGroup",
        "cluster_logging": "clusterLogging",
        "core_dns_compute_type": "coreDnsComputeType",
        "endpoint_access": "endpointAccess",
        "kubectl_environment": "kubectlEnvironment",
        "kubectl_layer": "kubectlLayer",
        "kubectl_memory": "kubectlMemory",
        "masters_role": "mastersRole",
        "on_event_layer": "onEventLayer",
        "output_masters_role_arn": "outputMastersRoleArn",
        "place_cluster_handler_in_vpc": "placeClusterHandlerInVpc",
        "prune": "prune",
        "secrets_encryption_key": "secretsEncryptionKey",
        "service_ipv4_cidr": "serviceIpv4Cidr",
        "default_profile": "defaultProfile",
        "cloud_watch_monitoring_options": "cloudWatchMonitoringOptions",
        "external_dns_options": "externalDnsOptions",
        "external_secrets_options": "externalSecretsOptions",
        "logging_options": "loggingOptions",
    },
)
class AwsIntegratedFargateClusterProps(aws_cdk.aws_eks.FargateClusterProps):
    def __init__(
        self,
        *,
        version: aws_cdk.aws_eks.KubernetesVersion,
        cluster_name: typing.Optional[builtins.str] = None,
        output_cluster_name: typing.Optional[builtins.bool] = None,
        output_config_command: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
        alb_controller: typing.Optional[typing.Union[aws_cdk.aws_eks.AlbControllerOptions, typing.Dict[str, typing.Any]]] = None,
        cluster_handler_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cluster_handler_security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        cluster_logging: typing.Optional[typing.Sequence[aws_cdk.aws_eks.ClusterLoggingTypes]] = None,
        core_dns_compute_type: typing.Optional[aws_cdk.aws_eks.CoreDnsComputeType] = None,
        endpoint_access: typing.Optional[aws_cdk.aws_eks.EndpointAccess] = None,
        kubectl_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kubectl_layer: typing.Optional[aws_cdk.aws_lambda.ILayerVersion] = None,
        kubectl_memory: typing.Optional[aws_cdk.Size] = None,
        masters_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        on_event_layer: typing.Optional[aws_cdk.aws_lambda.ILayerVersion] = None,
        output_masters_role_arn: typing.Optional[builtins.bool] = None,
        place_cluster_handler_in_vpc: typing.Optional[builtins.bool] = None,
        prune: typing.Optional[builtins.bool] = None,
        secrets_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
        default_profile: typing.Optional[typing.Union[aws_cdk.aws_eks.FargateProfileOptions, typing.Dict[str, typing.Any]]] = None,
        cloud_watch_monitoring_options: typing.Optional[typing.Union["CloudWatchMonitoringOptions", typing.Dict[str, typing.Any]]] = None,
        external_dns_options: typing.Optional[typing.Union["ExternalDnsOptions", typing.Dict[str, typing.Any]]] = None,
        external_secrets_options: typing.Optional[typing.Union["ExternalSecretsOptions", typing.Dict[str, typing.Any]]] = None,
        logging_options: typing.Optional[typing.Union["FargateLoggingOptions", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following: ``vpcSubnets: [{ subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }]`` Default: - All public and private subnets
        :param alb_controller: Install the AWS Load Balancer Controller onto the cluster. Default: - The controller is not installed.
        :param cluster_handler_environment: Custom environment variables when interacting with the EKS endpoint to manage the cluster lifecycle. Default: - No environment variables.
        :param cluster_handler_security_group: A security group to associate with the Cluster Handler's Lambdas. The Cluster Handler's Lambdas are responsible for calling AWS's EKS API. Requires ``placeClusterHandlerInVpc`` to be set to true. Default: - No security group.
        :param cluster_logging: The cluster log types which you want to enable. Default: - none
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`), compatibleRuntimes: [lambda.Runtime.PROVIDED], }); Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param kubectl_memory: Amount of memory to allocate to the provider's lambda function. Default: Size.gibibytes(1)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param on_event_layer: An AWS Lambda Layer which includes the NPM dependency ``proxy-agent``. This layer is used by the onEvent handler to route AWS SDK requests through a proxy. By default, the provider will use the layer included in the "aws-lambda-layer-node-proxy-agent" SAR application which is available in all commercial regions. To deploy the layer locally define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'proxy-agent-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`), compatibleRuntimes: [lambda.Runtime.NODEJS_14_X], }); Default: - a layer bundled with this module.
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param place_cluster_handler_in_vpc: If set to true, the cluster handler functions will be placed in the private subnets of the cluster vpc, subject to the ``vpcSubnets`` selection strategy. Default: false
        :param prune: Indicates whether Kubernetes resources added through ``addManifest()`` can be automatically pruned. When this is enabled (default), prune labels will be allocated and injected to each resource. These labels will then be used when issuing the ``kubectl apply`` operation with the ``--prune`` switch. Default: true
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.
        :param service_ipv4_cidr: The CIDR block to assign Kubernetes service IP addresses from. Default: - Kubernetes assigns addresses from either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.
        :param cloud_watch_monitoring_options: 
        :param external_dns_options: 
        :param external_secrets_options: 
        :param logging_options: 
        '''
        if isinstance(alb_controller, dict):
            alb_controller = aws_cdk.aws_eks.AlbControllerOptions(**alb_controller)
        if isinstance(default_profile, dict):
            default_profile = aws_cdk.aws_eks.FargateProfileOptions(**default_profile)
        if isinstance(cloud_watch_monitoring_options, dict):
            cloud_watch_monitoring_options = CloudWatchMonitoringOptions(**cloud_watch_monitoring_options)
        if isinstance(external_dns_options, dict):
            external_dns_options = ExternalDnsOptions(**external_dns_options)
        if isinstance(external_secrets_options, dict):
            external_secrets_options = ExternalSecretsOptions(**external_secrets_options)
        if isinstance(logging_options, dict):
            logging_options = FargateLoggingOptions(**logging_options)
        if __debug__:
            type_hints = typing.get_type_hints(AwsIntegratedFargateClusterProps.__init__)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument output_cluster_name", value=output_cluster_name, expected_type=type_hints["output_cluster_name"])
            check_type(argname="argument output_config_command", value=output_config_command, expected_type=type_hints["output_config_command"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument alb_controller", value=alb_controller, expected_type=type_hints["alb_controller"])
            check_type(argname="argument cluster_handler_environment", value=cluster_handler_environment, expected_type=type_hints["cluster_handler_environment"])
            check_type(argname="argument cluster_handler_security_group", value=cluster_handler_security_group, expected_type=type_hints["cluster_handler_security_group"])
            check_type(argname="argument cluster_logging", value=cluster_logging, expected_type=type_hints["cluster_logging"])
            check_type(argname="argument core_dns_compute_type", value=core_dns_compute_type, expected_type=type_hints["core_dns_compute_type"])
            check_type(argname="argument endpoint_access", value=endpoint_access, expected_type=type_hints["endpoint_access"])
            check_type(argname="argument kubectl_environment", value=kubectl_environment, expected_type=type_hints["kubectl_environment"])
            check_type(argname="argument kubectl_layer", value=kubectl_layer, expected_type=type_hints["kubectl_layer"])
            check_type(argname="argument kubectl_memory", value=kubectl_memory, expected_type=type_hints["kubectl_memory"])
            check_type(argname="argument masters_role", value=masters_role, expected_type=type_hints["masters_role"])
            check_type(argname="argument on_event_layer", value=on_event_layer, expected_type=type_hints["on_event_layer"])
            check_type(argname="argument output_masters_role_arn", value=output_masters_role_arn, expected_type=type_hints["output_masters_role_arn"])
            check_type(argname="argument place_cluster_handler_in_vpc", value=place_cluster_handler_in_vpc, expected_type=type_hints["place_cluster_handler_in_vpc"])
            check_type(argname="argument prune", value=prune, expected_type=type_hints["prune"])
            check_type(argname="argument secrets_encryption_key", value=secrets_encryption_key, expected_type=type_hints["secrets_encryption_key"])
            check_type(argname="argument service_ipv4_cidr", value=service_ipv4_cidr, expected_type=type_hints["service_ipv4_cidr"])
            check_type(argname="argument default_profile", value=default_profile, expected_type=type_hints["default_profile"])
            check_type(argname="argument cloud_watch_monitoring_options", value=cloud_watch_monitoring_options, expected_type=type_hints["cloud_watch_monitoring_options"])
            check_type(argname="argument external_dns_options", value=external_dns_options, expected_type=type_hints["external_dns_options"])
            check_type(argname="argument external_secrets_options", value=external_secrets_options, expected_type=type_hints["external_secrets_options"])
            check_type(argname="argument logging_options", value=logging_options, expected_type=type_hints["logging_options"])
        self._values: typing.Dict[str, typing.Any] = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if alb_controller is not None:
            self._values["alb_controller"] = alb_controller
        if cluster_handler_environment is not None:
            self._values["cluster_handler_environment"] = cluster_handler_environment
        if cluster_handler_security_group is not None:
            self._values["cluster_handler_security_group"] = cluster_handler_security_group
        if cluster_logging is not None:
            self._values["cluster_logging"] = cluster_logging
        if core_dns_compute_type is not None:
            self._values["core_dns_compute_type"] = core_dns_compute_type
        if endpoint_access is not None:
            self._values["endpoint_access"] = endpoint_access
        if kubectl_environment is not None:
            self._values["kubectl_environment"] = kubectl_environment
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if kubectl_memory is not None:
            self._values["kubectl_memory"] = kubectl_memory
        if masters_role is not None:
            self._values["masters_role"] = masters_role
        if on_event_layer is not None:
            self._values["on_event_layer"] = on_event_layer
        if output_masters_role_arn is not None:
            self._values["output_masters_role_arn"] = output_masters_role_arn
        if place_cluster_handler_in_vpc is not None:
            self._values["place_cluster_handler_in_vpc"] = place_cluster_handler_in_vpc
        if prune is not None:
            self._values["prune"] = prune
        if secrets_encryption_key is not None:
            self._values["secrets_encryption_key"] = secrets_encryption_key
        if service_ipv4_cidr is not None:
            self._values["service_ipv4_cidr"] = service_ipv4_cidr
        if default_profile is not None:
            self._values["default_profile"] = default_profile
        if cloud_watch_monitoring_options is not None:
            self._values["cloud_watch_monitoring_options"] = cloud_watch_monitoring_options
        if external_dns_options is not None:
            self._values["external_dns_options"] = external_dns_options
        if external_secrets_options is not None:
            self._values["external_secrets_options"] = external_secrets_options
        if logging_options is not None:
            self._values["logging_options"] = logging_options

    @builtins.property
    def version(self) -> aws_cdk.aws_eks.KubernetesVersion:
        '''The Kubernetes version to run in the cluster.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(aws_cdk.aws_eks.KubernetesVersion, result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Name for the cluster.

        :default: - Automatically generated name
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[builtins.bool]:
        '''Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        :default: false
        '''
        result = self._values.get("output_cluster_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output_config_command(self) -> typing.Optional[builtins.bool]:
        '''Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        :default: true
        '''
        result = self._values.get("output_config_command")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        :default: - A role is automatically created for you
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''Security Group to use for Control Plane ENIs.

        :default: - A security group is automatically created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''The VPC in which to create the Cluster.

        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        '''Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following:

        ``vpcSubnets: [{ subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }]``

        :default: - All public and private subnets
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]], result)

    @builtins.property
    def alb_controller(self) -> typing.Optional[aws_cdk.aws_eks.AlbControllerOptions]:
        '''Install the AWS Load Balancer Controller onto the cluster.

        :default: - The controller is not installed.

        :see: https://kubernetes-sigs.github.io/aws-load-balancer-controller
        '''
        result = self._values.get("alb_controller")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.AlbControllerOptions], result)

    @builtins.property
    def cluster_handler_environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables when interacting with the EKS endpoint to manage the cluster lifecycle.

        :default: - No environment variables.
        '''
        result = self._values.get("cluster_handler_environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cluster_handler_security_group(
        self,
    ) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''A security group to associate with the Cluster Handler's Lambdas.

        The Cluster Handler's Lambdas are responsible for calling AWS's EKS API.

        Requires ``placeClusterHandlerInVpc`` to be set to true.

        :default: - No security group.
        '''
        result = self._values.get("cluster_handler_security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def cluster_logging(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_eks.ClusterLoggingTypes]]:
        '''The cluster log types which you want to enable.

        :default: - none
        '''
        result = self._values.get("cluster_logging")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_eks.ClusterLoggingTypes]], result)

    @builtins.property
    def core_dns_compute_type(
        self,
    ) -> typing.Optional[aws_cdk.aws_eks.CoreDnsComputeType]:
        '''Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        '''
        result = self._values.get("core_dns_compute_type")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.CoreDnsComputeType], result)

    @builtins.property
    def endpoint_access(self) -> typing.Optional[aws_cdk.aws_eks.EndpointAccess]:
        '''Configure access to the Kubernetes API server endpoint..

        :default: EndpointAccess.PUBLIC_AND_PRIVATE

        :see: https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html
        '''
        result = self._values.get("endpoint_access")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.EndpointAccess], result)

    @builtins.property
    def kubectl_environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables for the kubectl execution.

        Only relevant for kubectl enabled clusters.

        :default: - No environment variables.
        '''
        result = self._values.get("kubectl_environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kubectl_layer(self) -> typing.Optional[aws_cdk.aws_lambda.ILayerVersion]:
        '''An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-kubectl" SAR application which is available in all
        commercial regions.

        To deploy the layer locally, visit
        https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md
        for instructions on how to prepare the .zip file and then define it in your
        app as follows::

           const layer = new lambda.LayerVersion(this, 'kubectl-layer', {
              code: lambda.Code.fromAsset(`${__dirname}/layer.zip`),
              compatibleRuntimes: [lambda.Runtime.PROVIDED],
           });

        :default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.

        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        '''
        result = self._values.get("kubectl_layer")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.ILayerVersion], result)

    @builtins.property
    def kubectl_memory(self) -> typing.Optional[aws_cdk.Size]:
        '''Amount of memory to allocate to the provider's lambda function.

        :default: Size.gibibytes(1)
        '''
        result = self._values.get("kubectl_memory")
        return typing.cast(typing.Optional[aws_cdk.Size], result)

    @builtins.property
    def masters_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        :default:

        - a role that assumable by anyone with permissions in the same
        account will automatically be defined

        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        '''
        result = self._values.get("masters_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def on_event_layer(self) -> typing.Optional[aws_cdk.aws_lambda.ILayerVersion]:
        '''An AWS Lambda Layer which includes the NPM dependency ``proxy-agent``.

        This layer
        is used by the onEvent handler to route AWS SDK requests through a proxy.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-node-proxy-agent" SAR application which is available in all
        commercial regions.

        To deploy the layer locally define it in your app as follows::

           const layer = new lambda.LayerVersion(this, 'proxy-agent-layer', {
              code: lambda.Code.fromAsset(`${__dirname}/layer.zip`),
              compatibleRuntimes: [lambda.Runtime.NODEJS_14_X],
           });

        :default: - a layer bundled with this module.
        '''
        result = self._values.get("on_event_layer")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.ILayerVersion], result)

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[builtins.bool]:
        '''Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        :default: false
        '''
        result = self._values.get("output_masters_role_arn")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def place_cluster_handler_in_vpc(self) -> typing.Optional[builtins.bool]:
        '''If set to true, the cluster handler functions will be placed in the private subnets of the cluster vpc, subject to the ``vpcSubnets`` selection strategy.

        :default: false
        '''
        result = self._values.get("place_cluster_handler_in_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether Kubernetes resources added through ``addManifest()`` can be automatically pruned.

        When this is enabled (default), prune labels will be
        allocated and injected to each resource. These labels will then be used
        when issuing the ``kubectl apply`` operation with the ``--prune`` switch.

        :default: true
        '''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secrets_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''KMS secret for envelope encryption for Kubernetes secrets.

        :default:

        - By default, Kubernetes stores all secret object data within etcd and
        all etcd volumes used by Amazon EKS are encrypted at the disk-level
        using AWS-Managed encryption keys.
        '''
        result = self._values.get("secrets_encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def service_ipv4_cidr(self) -> typing.Optional[builtins.str]:
        '''The CIDR block to assign Kubernetes service IP addresses from.

        :default:

        - Kubernetes assigns addresses from either the
        10.100.0.0/16 or 172.20.0.0/16 CIDR blocks

        :see: https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigRequest.html#AmazonEKS-Type-KubernetesNetworkConfigRequest-serviceIpv4Cidr
        '''
        result = self._values.get("service_ipv4_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_profile(self) -> typing.Optional[aws_cdk.aws_eks.FargateProfileOptions]:
        '''Fargate Profile to create along with the cluster.

        :default:

        - A profile called "default" with 'default' and 'kube-system'
        selectors will be created if this is left undefined.
        '''
        result = self._values.get("default_profile")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.FargateProfileOptions], result)

    @builtins.property
    def cloud_watch_monitoring_options(
        self,
    ) -> typing.Optional["CloudWatchMonitoringOptions"]:
        result = self._values.get("cloud_watch_monitoring_options")
        return typing.cast(typing.Optional["CloudWatchMonitoringOptions"], result)

    @builtins.property
    def external_dns_options(self) -> typing.Optional["ExternalDnsOptions"]:
        result = self._values.get("external_dns_options")
        return typing.cast(typing.Optional["ExternalDnsOptions"], result)

    @builtins.property
    def external_secrets_options(self) -> typing.Optional["ExternalSecretsOptions"]:
        result = self._values.get("external_secrets_options")
        return typing.cast(typing.Optional["ExternalSecretsOptions"], result)

    @builtins.property
    def logging_options(self) -> typing.Optional["FargateLoggingOptions"]:
        result = self._values.get("logging_options")
        return typing.cast(typing.Optional["FargateLoggingOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsIntegratedFargateClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.eks_patterns.CloudWatchMonitoringOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CloudWatchMonitoringOptions:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWatchMonitoringOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchMonitoringOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.eks_patterns.ExternalDnsOptions",
    jsii_struct_bases=[],
    name_mapping={"domain_filter": "domainFilter", "enabled": "enabled"},
)
class ExternalDnsOptions:
    def __init__(
        self,
        *,
        domain_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain_filter: 
        :param enabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalDnsOptions.__init__)
            check_type(argname="argument domain_filter", value=domain_filter, expected_type=type_hints["domain_filter"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {}
        if domain_filter is not None:
            self._values["domain_filter"] = domain_filter
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def domain_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("domain_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDnsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.eks_patterns.ExternalSecretsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "create_namespace": "createNamespace",
        "enabled": "enabled",
        "name": "name",
        "namespace": "namespace",
    },
)
class ExternalSecretsOptions:
    def __init__(
        self,
        *,
        create_namespace: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_namespace: 
        :param enabled: 
        :param name: 
        :param namespace: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretsOptions.__init__)
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.eks_patterns.FargateLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group": "logGroup",
        "log_stream_prefix": "logStreamPrefix",
        "retention": "retention",
    },
)
class FargateLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        log_stream_prefix: typing.Optional[builtins.str] = None,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
    ) -> None:
        '''
        :param enabled: Controls whether logging will be set up for pods using the default Fargate provide on the EKS cluster. Default: true
        :param log_group: The CloudWatch log group where Farget container logs will be sent.
        :param log_stream_prefix: The prefix to add to the start of log streams created by the Fargate logger.
        :param retention: The number of days logs sent to CloudWatch from Fluent Bit should be retained before they are automatically removed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLoggingOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_prefix", value=log_stream_prefix, expected_type=type_hints["log_stream_prefix"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_stream_prefix is not None:
            self._values["log_stream_prefix"] = log_stream_prefix
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Controls whether logging will be set up for pods using the default Fargate provide on the EKS cluster.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''The CloudWatch log group where Farget container logs will be sent.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def log_stream_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix to add to the start of log streams created by the Fargate logger.'''
        result = self._values.get("log_stream_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''The number of days logs sent to CloudWatch from Fluent Bit should be retained before they are automatically removed.'''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsIntegratedFargateCluster",
    "AwsIntegratedFargateClusterProps",
    "CloudWatchMonitoringOptions",
    "ExternalDnsOptions",
    "ExternalSecretsOptions",
    "FargateLoggingOptions",
]

publication.publish()
