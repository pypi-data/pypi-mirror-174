from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_microservice_library.integrations.fact import get_fact_endpoint
from ehelply_microservice_library.integrations.logging import Log

from ehelply_bootstrapper.utils.state import State

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json


class UsageType(BaseModel):
    """
    Usage_type_key: The string usage type key name
    Scaling: The default amount of scaling to apply to a particular usage type. This will help remove the constant
        need for *1000000 for usage types that dont need that level of precision
    """
    usage_type_key: str
    scaling: int = 1


class UsageMQ(BaseModel):
    project_uuid: str
    usage_key: str
    quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth


class Monitor(Integration):
    """
    Monitor integration is used to talk to the ehelply-meta microservice
    """

    def __init__(self, supported_usage_types: list[UsageType]) -> None:
        super().__init__("monitor")

        self.sqs = State.aws.make_client("sqs")
        self.supported_usage_types: dict[str, int] = {
            item.usage_type_key: item.scaling for item in supported_usage_types
        }

    def load(self):
        pass

    def add_usage(self, usage: UsageMQ) -> bool:
        """
        Add usage to a project

        NOTE: Quantity formats represented by a x10000000 integer. Precision to the millonth

        :return:
        """
        if usage.usage_key not in self.supported_usage_types:
            State.logger.warning(
                f"Usage type has not been registered. Override get_usage_types() in service.py and add {usage.usage_key} there."
            )
        else:
            usage.quantity *= self.supported_usage_types[usage.usage_key]

        if usage.project_uuid == 'ehelply-resources' or usage.project_uuid == 'ehelply-cloud':
            return False

        self.sqs.send_message(
            QueueUrl=get_fact_endpoint("mq-usage"),
            MessageBody=json.dumps(jsonable_encoder(usage.dict()))
        )

        return True
