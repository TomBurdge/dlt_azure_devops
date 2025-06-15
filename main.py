from azure.devops.connection import Connection

from msrest.authentication import OAuthTokenAuthentication
from dotenv import load_dotenv
import os

import msal


def load_oauth_token(
    client_id: str, client_secret: str, authority: str, scope: str, endpoint: str
) -> str:
    # adapted from:
    # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/1.22.0/sample/confidential_client_secret_sample.py
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
        # token_cache=...  # Default cache is in memory only.
        # You can learn how to use SerializableTokenCache from
        # https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
    )

    # The pattern to acquire a token looks like this.
    result = None

    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    result = app.acquire_token_silent(scope, account=None)

    if not result:
        result = app.acquire_token_for_client(scopes=scope)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError(
            f"""Exception:
Error: {result.get("error")}
Error description: {result.get("error_description")}
Error correlation id: {result.get("correlation_id")}
        """
        )


if __name__ == "__main__":
    # Load secret configs
    load_dotenv()

    personal_access_token = os.environ["devops_pat"]
    pipeline_name = os.environ["pipeline_name"]
    project_name = os.environ["project_name"]
    org_name = os.environ["org_name"]
    organization_url = f"https://dev.azure.com/{org_name}"
    token = os.environ["token"]
    client_id = os.environ["client_id"]
    client_secret = os.environ["client_secret"]

    pipeline_name = "pn-pdap-product-core"

    # Load credetials
    # credentials = BasicAuthentication("", personal_access_token)
    credentials = OAuthTokenAuthentication(client_id=client_id, token=token)

    # Load client connection
    connection = Connection(base_url=organization_url, creds=credentials)
    pipelines_client = connection.clients.get_pipelines_client()
    pipelines = pipelines_client.list_pipelines(project=project_name)
    for i, pipeline in enumerate(pipelines):
        print(pipeline)
        if i == 5:
            break
