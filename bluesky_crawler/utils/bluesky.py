from datetime import date, datetime

from atproto import CAR, AtUri
from atproto.xrpc_client import models
from loguru import logger


def get_date_from_commit(commit: models.ComAtprotoSyncSubscribeRepos.Commit) -> date:
    created_at = datetime.strptime(commit.time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return created_at.date()


def get_commit_as_dict(commit: models.ComAtprotoSyncSubscribeRepos.Commit) -> dict:  # noqa: C901
    car = CAR.from_bytes(commit.blocks)
    response = {
        "seq": commit.seq,
        "time": commit.time,
        "repo": commit.repo,
        "commit": str(commit.commit),
        "prev": str(commit.prev),
        "operations": [],
    }

    for op in commit.ops:
        if op.action == 'update':
            # logger.warning(f"Update action is not supported. ({op})")
            continue

        uri = AtUri.from_str(f'at://{commit.repo}/{op.path}')
        operation = {
            "collection": uri.collection,
            "action": op.action,
            "uri": str(uri),
        }

        if op.action == 'create':
            if not op.cid:
                continue
            record_raw_data = car.blocks.get(op.cid)
            if not record_raw_data:
                continue
            operation["cid"] = str(op.cid)
            operation["raw_data"] = record_raw_data
        response["operations"].append(operation)
    return response
