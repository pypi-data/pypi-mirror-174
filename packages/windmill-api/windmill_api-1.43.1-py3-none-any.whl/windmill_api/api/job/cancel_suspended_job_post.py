from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.cancel_suspended_job_post_json_body import CancelSuspendedJobPostJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    workspace: str,
    id: str,
    resume_id: int,
    signature: str,
    json_body: CancelSuspendedJobPostJsonBody,
    approver: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/cancel/{id}/{resume_id}/{signature}".format(
        client.base_url, workspace=workspace, id=id, resume_id=resume_id, signature=signature
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "approver": approver,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    id: str,
    resume_id: int,
    signature: str,
    json_body: CancelSuspendedJobPostJsonBody,
    approver: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        signature=signature,
        json_body=json_body,
        approver=approver,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    workspace: str,
    id: str,
    resume_id: int,
    signature: str,
    json_body: CancelSuspendedJobPostJsonBody,
    approver: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        signature=signature,
        json_body=json_body,
        approver=approver,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
