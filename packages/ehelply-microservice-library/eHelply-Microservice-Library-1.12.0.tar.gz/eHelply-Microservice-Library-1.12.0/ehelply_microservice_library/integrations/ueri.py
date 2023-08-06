from __future__ import annotations
from typing import Callable
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_bootstrapper.utils.service import ServiceMeta
from ehelply_microservice_library.integrations.fact import get_fact_endpoint
from ehelply_microservice_library.integrations.logging import Log

from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.drivers.fast_api_utils import responses

from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json
from ehelply_microservice_library.utils.ehelply_cloud import (
    ehelply_cloud_access,
    CloudParticipantAuthRequest,
    CloudParticipantResponse,
    KeysDB,
    ProjectDB,
    ProjectMembersDB,
    ProjectCredentialDB,
    ProjectMemberRoleEnum,
    ProjectStatus,
    is_allowed
)


class UeriModel(BaseModel):
    company: str
    product: str
    logical_group: str
    location: str
    service: str
    service_type: str
    type_id: str
    drill_segments: list[str]


class Ueri(Integration):
    """
    Monitor integration is used to talk to the ehelply-meta microservice
    """

    def __init__(
            self, service_meta: ServiceMeta, handlers: dict[str, Callable[[str], BaseModel | dict | list]],
            custom_drill: Callable[[list[str], BaseModel | dict | list], any] | None = None,
    ) -> None:
        super().__init__("ueri")
        self.service_meta = service_meta
        self.handlers = handlers
        self.custom_drill = custom_drill

    def load(self):
        pass

    def parse_ueri(self, ueri: str, exception_if_invalid: bool = True) -> UeriModel | None:
        ueri_components: list[str] = ueri.split(":")
        if len(ueri_components) < 8 or len(ueri_components) > 9:
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400, detail="Invalid ueri"
                )
            else:
                return None

        if ueri_components[0] != "ueri":
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400, detail="Invalid ueri format"
                )
            else:
                return None

        drill_segments: list[str] = []
        if len(ueri_components) == 9:
            drill_segments = ueri_components[8].split("/")

        ueri_model: UeriModel = UeriModel(
            company=ueri_components[1],
            product=ueri_components[2],
            logical_group=ueri_components[3],
            location=ueri_components[4],
            service=ueri_components[5],
            service_type=ueri_components[6],
            type_id=ueri_components[7],
            drill_segments=drill_segments
        )

        if ueri_model.company != "ehelply":
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400, detail="This ueri endpoint can only handle company values of: ehelply"
                )
            else:
                return None
        if ueri_model.product != "superstack":
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400, detail="This ueri endpoint can only handle product values of: superstack"
                )
            else:
                return None
        if ueri_model.location != "ca-01":
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400, detail="This ueri endpoint can only handle location values of: ca-01"
                )
            else:
                return None
        if ueri_model.service != self.service_meta.key:
            if exception_if_invalid:
                raise HTTPException(
                    status_code=400,
                    detail=f"This ueri endpoint can only handle service values of: {self.service_meta.key}"
                )
            else:
                return None

        return ueri_model

    def handle(self, cloud_participant: CloudParticipantResponse, ueri: UeriModel) -> BaseModel | dict | list:
        is_allowed(
            cloud_participant=cloud_participant,
            project_uuid=ueri.logical_group,
            # allow_privileged=True
        )

        if ueri.service_type not in self.handlers:
            raise HTTPException(
                status_code=400,
                detail=f"This ueri endpoint can only handle service type values of: {self.handlers.keys()}"
            )

        return self.handlers[ueri.service_type](ueri.type_id)

    def __default_drill(self, drill_segments: list[str], result: BaseModel | dict | list) -> any:
        for segment in drill_segments:
            if segment.isdigit():
                segment = int(segment)
            result = result[segment]
        return result

    def drill(self, ueri: UeriModel, result: BaseModel | dict | list) -> any:
        try:
            drill = self.__default_drill
            if self.custom_drill:
                drill = self.custom_drill
            return drill(ueri.drill_segments, result)
        except:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid drill segments"
            )
