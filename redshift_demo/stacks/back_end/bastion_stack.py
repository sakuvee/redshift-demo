from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal

class GlobalArgs():
    """
    Helper to define global statics
    """

    ENVIRONMENT = "production"
    REPO_NAME = "redshift-demo"
    VERSION = "2021-06-16"

class BastionStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct, id: str,
        vpc,
        ec2_instance_type: str,
        stack_log_level: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Security Group
        sg = _ec2.SecurityGroup(
            self,
            id="Redshift_bastion_sg",
            vpc=vpc.get_vpc,
            allow_all_outbound=True,
            security_group_name=f"redshift_bastion_sg_{id}",
            description="Security Group for Redshift Bastion"
        )

        # IAM Role (S3FullAccess)
        role = Role(
            self,
            id="rolle",
            assumed_by=ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )

        self.bastion = _ec2.BastionHostLinux(
            self,
            "bastion",
            vpc=vpc.get_vpc,
            subnet_selection=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            ),
            instance_name="bastion",
            instance_type=_ec2.InstanceType(instance_type_identifier=ec2_instance_type),
        )
        self.bastion.instance.instance.add_property_override("KeyName", "rs-demo-bastion")
        self.bastion.connections.allow_from_any_ipv4(_ec2.Port.tcp(22), "Internet access SSH")

    # properties to share with other stacks
    @property
    def get_bastion_sgs(self):
        return self.bastion.connections.security_groups
        