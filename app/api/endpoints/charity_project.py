from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_edit,
                                check_project_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investing_in_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_in_project(new_project, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_edit(
        project_id, obj_in, session
    )
    project = await charity_project_crud.update(project, obj_in, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(
        project_id, session
    )
    project = await charity_project_crud.remove(project, session)
    return project
