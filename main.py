#!/usr/bin/env python
from cdktf import App, TerraformStack
from constructs import Construct


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here


app = App()
MyStack(app, "cdktf-awsscripts")

app.synth()
