import dataclasses

from typing import List, Optional, Union
from marshmallow import validate
from marshmallow_dataclass import dataclass

from beam.types import PythonVersion, OutputType, MountType
from beam.base import BaseSerializer, BaseTriggerSerializer
from beam import validators


@dataclass
class AppSpecConfiguration(BaseSerializer):
    name: str = dataclasses.field(metadata={"validate": validate.Length(max=128)})
    cpu: str
    gpu: int
    memory: str
    apt_install: List[str]
    python_version: str = dataclasses.field(
        metadata={
            "validate": validate.OneOf(
                choices=[version[1] for version in PythonVersion.Types]
            ),
        }
    )
    python_packages: Union[str, List[str]]
    workspace: str


@dataclass
class RestAPITrigger(BaseTriggerSerializer):
    inputs: validators.TypeSerializerDict
    outputs: validators.TypeSerializerDict
    handler: str = dataclasses.field(metadata={"validate": validators.IsFileMethod()})
    loader: Optional[str]
    trigger_type: str = "rest_api"


@dataclass
class CronJobTrigger(BaseTriggerSerializer):
    # TODO: Validation step needs to be handled somewhere
    cron_schedule: str
    handler: str = dataclasses.field(metadata={"validate": validators.IsFileMethod()})
    trigger_type: str = "cron_job"


@dataclass
class WebhookTrigger(BaseTriggerSerializer):
    inputs: validators.TypeSerializerDict
    handler: str = dataclasses.field(metadata={"validate": validators.IsFileMethod()})
    trigger_type: str = "webhook"


@dataclass
class FileConfiguration(BaseSerializer):
    path: str
    name: str
    output_type: str = dataclasses.field(
        metadata={
            "validate": validate.OneOf(
                choices=[version[1] for version in OutputType.Types]
            )
        }
    )


@dataclass
class VolumeConfiguration(BaseSerializer):
    name: str
    app_path: str
    mount_type: str = dataclasses.field(
        metadata={"validate": validate.OneOf(choices=[t[1] for t in MountType.Types])}
    )
    checksum: str = None
    local_path: str = None
