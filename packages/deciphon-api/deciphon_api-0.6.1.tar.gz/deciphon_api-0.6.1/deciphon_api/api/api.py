from fastapi import APIRouter, Request
from starlette.status import HTTP_200_OK

from deciphon_api.api import dbs, hmms, jobs, prods, scans, sched, seqs
from deciphon_api.core.responses import PrettyJSONResponse

router = APIRouter()

router.include_router(dbs.router)
router.include_router(hmms.router)
router.include_router(jobs.router)
router.include_router(prods.router)
router.include_router(scans.router)
router.include_router(sched.router)
router.include_router(seqs.router)


@router.get(
    "/",
    summary="list of all endpoints",
    response_class=PrettyJSONResponse,
    status_code=HTTP_200_OK,
    name="root:list-of-endpoints",
)
def root(request: Request):
    routes = sorted(request.app.routes, key=lambda x: x.name)
    urls = {route.name: route.path for route in routes}
    return PrettyJSONResponse(urls)
