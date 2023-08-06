import json
from typing import List, Optional

import boto3
import click
from rich import print

from ..utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default="Coiled",
    help="Name of the AMP workspace to create",
)
@click.option(
    "--region",
    default=None,
    help="Region of the AMP workspace to create (doesn't need to match region of cluster sending metrics)",
)
@click.option(
    "--profile",
    default=None,
    envvar="AWS_PROFILE",
    help="AWS profile to use from your local AWS credentials file",
)
def aws_amp_setup(
    name: str,
    region: Optional[str],
    profile: Optional[str],
):
    session = boto3.Session(profile_name=profile, region_name=region)
    iam = session.client("iam")
    sts = session.client("sts")

    identity = sts.get_caller_identity()
    account = identity.get("Account")

    amp_arn, amp_endpoint = make_amp_workspace(session, name, region)

    user_policy_name = f"PrometheusWrite-{name}"

    from .aws import (
        attach_policy,
        create_or_update_policy,
        create_user,
        make_access_key,
    )

    create_user(iam, user_policy_name)
    policy_arn = create_or_update_policy(
        iam, account, user_policy_name, amp_write_policy_doc([amp_arn])
    )
    attach_policy(iam, user_policy_name, policy_arn)
    key, secret = make_access_key(iam, user_policy_name)

    prom_write = dict(
        endpoint=amp_endpoint,
        auth={
            "sigv4": {
                "region": region,
                "access_key": key,
                "secret_key": secret,
            }
        },
    )

    backend_options = dict(prometheus_write=prom_write)

    print(
        f"Put this in your [bold]backend_options[/bold] to send metrics to the [bold]{name}[/bold] workspace:"
    )
    print(json.dumps(backend_options))


def make_amp_workspace(session, name, region):
    amp = session.client("amp")

    # check for existing workspace matching the name
    result = None
    existing = amp.list_workspaces().get("workspaces", [])
    for workspace in existing:
        if workspace["alias"] == name:
            result = workspace
            break

    if not result:
        result = amp.create_workspace(alias=name)

    workspace_id = result["workspaceId"]
    endpoint = f"https://aps-workspaces.{region}.amazonaws.com/workspaces/{workspace_id}/api/v1/remote_write"
    return result["arn"], endpoint


def amp_write_policy_doc(workspace_arns: List[str]) -> str:
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CoiledPrometheusWrite",
                "Effect": "Allow",
                "Action": ["aps:RemoteWrite"],
                "Resource": workspace_arns,
            }
        ],
    }
    return json.dumps(policy)
