from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    workspace: str,
    flow_job_id: str,
    node_id: str,
    skip_direct: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/result_by_id/{flow_job_id}/{node_id}".format(
        client.base_url, workspace=workspace, flow_job_id=flow_job_id, node_id=node_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "skip_direct": skip_direct,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    workspace: str,
    flow_job_id: str,
    node_id: str,
    skip_direct: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        flow_job_id=flow_job_id,
        node_id=node_id,
        skip_direct=skip_direct,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    workspace: str,
    flow_job_id: str,
    node_id: str,
    skip_direct: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        flow_job_id=flow_job_id,
        node_id=node_id,
        skip_direct=skip_direct,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
