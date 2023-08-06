from typing import Dict, List, Optional

from beam.base import AbstractDataLoader
from beam.serializer import (
    RestAPITrigger,
    CronJobTrigger,
    WebhookTrigger,
)
from beam.types import Types


class TriggerType:
    Webhook = "webhook"
    RestAPI = "rest_api"
    CronJob = "cron_job"


class TriggerManager(AbstractDataLoader):
    def __init__(self) -> None:
        self.webhooks: List[
            WebhookTrigger,
        ] = []
        self.cron_jobs: List[CronJobTrigger] = []
        self.rest_apis: List[RestAPITrigger] = []

    def _validate_trigger_groupings(self):
        """
        NOTE: For the time being, the Beam APP can only accept one trigger during the alpha
        stages. Later we will allow multiple trigger types for webhooks (Slack, Twitter, etc)
        """
        triggers = self.webhooks + self.cron_jobs + self.rest_apis

        if len(triggers) > 1:
            raise ValueError("App can only have 1 trigger at a time")

    def Webhook(self, inputs: Dict[str, Types], handler: str, **_):
        """
        Arguments:
            handler: specify what method in which file to use as the entry point
            inputs: dictionary specifying how to serialize/deserialize input arguments
        """
        self.webhooks.append(WebhookTrigger(inputs=inputs, handler=handler))
        self._validate_trigger_groupings()

    def CronJob(self, cron_schedule: str, handler: str, **_):
        """
        Arguments:
            handler: specify what method in which file to use as the entry point
            cron_schedule: CRON string to indicate the schedule in which the job is to run
                - https://en.wikipedia.org/wiki/Cron \
        """
        self.cron_jobs.append(
            CronJobTrigger(cron_schedule=cron_schedule, handler=handler),
        )
        self._validate_trigger_groupings()

    def RestAPI(
        self,
        inputs: Dict[str, Types],
        outputs: Dict[str, Types],
        handler: str,
        loader: Optional[str] = None,
        **_,
    ):
        """
        Arguments:
            handler: specify what method in which file to use as the entry point
            inputs: dictionary specifying how to serialize/deserialize input arguments
            outputs: dictionary specifying how to serialize/deserialize return values
        """
        self.rest_apis.append(
            RestAPITrigger(
                inputs=inputs, outputs=outputs, handler=handler, loader=loader
            )
        )
        self._validate_trigger_groupings()

    def dumps(self):
        # To make this backwards compatible in the future after switching back to
        # multiple triggers, we will make this a list that currently will only have 1 trigger
        self._validate_trigger_groupings()
        triggers = []

        if len(self.webhooks) != 0:
            triggers.append(self.webhooks[0].validate_and_dump())
        elif len(self.cron_jobs) != 0:
            triggers.append(self.cron_jobs[0].validate_and_dump())
        elif len(self.rest_apis) != 0:
            triggers.append(self.rest_apis[0].validate_and_dump())

        return triggers

    def from_config(self, triggers):
        if triggers is None:
            return

        for t in triggers:
            trigger_type = t.get("trigger_type")
            inputs = {}
            outputs = {}

            if t.get("inputs"):
                inputs = Types.load_schema(t.get("inputs"))
                del t["inputs"]

            if t.get("outputs"):
                outputs = Types.load_schema(t.get("outputs"))
                del t["outputs"]

            if trigger_type == TriggerType.Webhook:
                self.Webhook(**t, inputs=inputs)
            elif trigger_type == TriggerType.CronJob:
                self.CronJob(**t, inputs=inputs)
            elif trigger_type == TriggerType.RestAPI:
                self.RestAPI(**t, inputs=inputs, outputs=outputs)
            else:
                raise ValueError(
                    f"Found an unknown trigger type in config: {trigger_type}"
                )
