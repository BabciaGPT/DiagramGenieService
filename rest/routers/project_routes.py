from fastapi import APIRouter, Depends

from firebase.repositories.ProjectRepo import ProjectsRepo
from rest.middleware.token_middleware import verify_token
from rest.models.Message import Message
from rest.models.Project import Project
from rest.models.ProjectResponse import ProjectResponse
from rest.models.ProjectsResponse import ProjectsResponse
from rest.models.ProjectRequest import ProjectRequest
from rest.models.ProjectCreateRequest import ProjectCreateRequest

project_router = APIRouter(prefix="/projects", tags=["Projects"])
projects_repo = ProjectsRepo()


@project_router.get("/fetchAllForUser", response_model=ProjectsResponse)
async def fetch_all_for_user(user: dict = Depends(verify_token)):
    projects = projects_repo.get_projects_by_user(
        user["user_id"],
    )
    return ProjectsResponse(projects=projects)


@project_router.post(
    "/fetchProject",
    response_model=ProjectResponse,
    dependencies=[Depends(verify_token)],
)
async def fetch_project(request: ProjectRequest):
    project_id, project = projects_repo.fetch_user_project(request.project_id)
    print(project)
    return ProjectResponse(project_id=project_id, project=Project(**project))


@project_router.delete(
    "/deleteProject",
    response_model=bool,
    dependencies=[Depends(verify_token)],
)
async def delete_project(request: ProjectRequest):
    result = projects_repo.delete_project(request.project_id)
    return result


@project_router.post(
    "/createProject",
    response_model=ProjectResponse,
    dependencies=[Depends(verify_token)],
)
async def create_project(
    request: ProjectCreateRequest, user: dict = Depends(verify_token)
):
    project = projects_repo.create_project(
        user_id=user["user_id"],
        title=request.title,
        description=request.description,
    )
    project["diagrams"] = []
    return ProjectResponse(project_id=project["id"], project=Project(**project))


@project_router.post(
    "/appendMessageToDiagrams",
    response_model=bool,
    dependencies=[Depends(verify_token)],
)
async def append_message_to_diagrams(
    request: ProjectRequest, message: Message, user: dict = Depends(verify_token)
):
    result = projects_repo.append_message_to_diagrams(
        project_id=request.project_id,
        message=message.dict(),
    )
    return result
