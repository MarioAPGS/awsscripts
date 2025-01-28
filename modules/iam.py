#!/usr/bin/env python
import json

from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws import (
    AwsProvider,
    IamGroup,
    IamGroupPolicyAttachment,
    IamPolicy,
)
from constructs import Construct


class IAMStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Configura el proveedor de AWS
        AwsProvider(self, "AWS", region="us-west-2")

    def create_iam_group_with_policies(
            self,
            group_name: str,
            account_id: str,
            policy_name_list: list[str]
    ):
        """
        Crea un grupo de IAM y adjunta una lista de políticas
        """
        # Define el grupo de IAM
        iam_group = IamGroup(
            self,
            group_name,
            name=group_name
        )

        # Adjunta cada política al grupo
        for idx, policy_name in enumerate(policy_name_list):
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            IamGroupPolicyAttachment(self,
                                     f"{group_name}-policy-attachment-{idx}",
                                     group=iam_group.name,
                                     policy_arn=policy_arn)

    def create_iam_policy(self, name: str, description: str, policy: dict):
        """
        Crea una política de IAM
        """
        # Convierte el dict de la política a JSON
        policy_document_json = json.dumps(policy)

        # Define la política de IAM
        IamPolicy(self, name,
                  name=name,
                  description=description,
                  policy=policy_document_json)

    def delete_iam_group_and_detach_policies(self, group_name: str):
        """
        Para eliminar un grupo, remueve el recurso de la configuración
        y ejecuta `cdktf deploy` nuevamente.
        """
        print(
            f"Para eliminar el grupo {group_name},"
            "remuévelo de la configuración y ejecuta `cdktf deploy`."
        )

    def delete_iam_policy(self, account_id: str, policy_name: str):
        """
        Para eliminar una política, remueve el recurso de la configuración
        y ejecuta `cdktf deploy` nuevamente.
        """
        print(
            f"Para eliminar la política {policy_name},"
            f"remuévela de la configuración y ejecuta `cdktf deploy`."
        )

# Configuración de la aplicación
app = App()
stack = IAMStack(app, "cdktf-iam-stack")

# Ejemplo de uso de las funciones del stack para crear grupos y políticas
# Crear un grupo y adjuntar políticas
stack.create_iam_group_with_policies(
    group_name="example-group",
    account_id="123456789012",
    policy_name_list=["AmazonS3ReadOnlyAccess", "AmazonEC2ReadOnlyAccess"]
)

# Crear una política personalizada
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "*"
        }
    ]
}
stack.create_iam_policy(
    name="customPolicy",
    description="Custom policy for listing S3 buckets",
    policy=policy_document
)

app.synth()
