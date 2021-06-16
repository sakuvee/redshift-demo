from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core


class GlobalArgs():
    """
    Helper to define global statics
    """

    ENVIRONMENT = "production"
    REPO_NAME = "redshift-demo"
    VERSION = "2021-06-16"


class VpcStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        stack_log_level: str,
        from_vpc_name=None,
        ** kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        if from_vpc_name is not None:
            self.vpc = _ec2.Vpc.from_lookup(
                self, "vpc",
                vpc_name=from_vpc_name
            )
        else:
            self.vpc = _ec2.Vpc(
                self,
                "RedshiftDemoVpc",
                cidr="10.128.0.0/21",
                max_azs=2,
                nat_gateways=0,
                enable_dns_support=True,
                enable_dns_hostnames=True,
                subnet_configuration=[
                    _ec2.SubnetConfiguration(
                        name="public", cidr_mask=24, subnet_type=_ec2.SubnetType.PUBLIC
                    ),
                    # _ec2.SubnetConfiguration(
                    #     name="app", cidr_mask=24, subnet_type=_ec2.SubnetType.PRIVATE
                    # ),
                    _ec2.SubnetConfiguration(
                        name="db", cidr_mask=24, subnet_type=_ec2.SubnetType.ISOLATED
                    )
                ]
            )

    # properties to share with other stacks
    @property
    def get_vpc(self):
        return self.vpc

    @property
    def get_vpc_public_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=_ec2.SubnetType.PUBLIC
        ).subnet_ids

    @property
    def get_vpc_private_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=_ec2.SubnetType.PRIVATE
        ).subnet_ids
