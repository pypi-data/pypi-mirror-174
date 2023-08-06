import logging
from typing import List, Optional

from kognic.io.model.input.input_entry import Input
from kognic.io.model.input.invalidated_reason_input import InvalidatedReasonInput
from kognic.io.resources.abstract import IOResource
from kognic.io.util import filter_none

log = logging.getLogger(__name__)


class InputResource(IOResource):
    """
    Resource exposing Kognic Inputs
    """

    def invalidate_inputs(self, input_uuids: List[str], invalidated_reason: InvalidatedReasonInput) -> None:
        """
        Invalidates inputs, and removes them from all input lists

        :param input_uuids: The input uuids to invalidate
        :param invalidated_reason: An Enum describing why inputs were invalidated
        """
        invalidated_json = dict(inputIds=input_uuids, invalidatedReason=invalidated_reason)
        self._client.post("v1/inputs/actions/invalidate", json=invalidated_json, discard_response=True)

    def get_inputs(
        self,
        project: str,
        batch: Optional[str] = None,
        include_invalidated: bool = False,
        external_ids: Optional[List[str]] = None,
    ) -> List[Input]:
        """
        Gets inputs for project, with option to filter for invalidated inputs

        :param project: Project (identifier) to filter
        :param batch: Batch (identifier) to filter
        :param invalidated: Returns invalidated inputs if True, otherwise valid inputs
        :param external_id: External ID to filter input on
        :param paginate: Only returns the first page if set to false
        :return List: List of Inputs
        """

        payload = {
            "project": project,
            "batch": batch,
            "includeInvalidated": include_invalidated,
            "externalIds": external_ids,
        }

        endpoint = "v1/inputs/fetch"

        inputs = list()
        for js in self._paginate_post(endpoint, json=filter_none(payload)):
            inputs.append(Input.from_json(js))
        return inputs

    def add_annotation_type(self, input_uuid: str, annotation_type: str) -> None:
        """
        Adds annotation-type to the input, which informs the Kognic Platform
        to produce a corresponding annotation for the annotation-type. Only
        possible if the annotation-type is available in the corresponding batch
        of the input (use method `get_annotation_types` to check).
        """

        self._client.post(f"v1/inputs/{input_uuid}/actions/add-annotation-type/{annotation_type}", discard_response=True)

    def remove_annotation_types(self, input_uuid: str, annotation_types: List[str]) -> None:
        """
        Removes annotation types from the input, which informs the Kognic Platform
        that a corresponding annotation should not be produced for the annotation types. Only
        possible if the annotation type is available for the input (use method `get_inputs_by_uuids` to check).
        Note: If multiple annotation types are configured to be annotated at the same time, i.e. on the same request,
        all of these annotation types need to be provided.
        """
        body = dict(annotationTypes=annotation_types)
        self._client.post(f"v1/inputs/{input_uuid}/annotation-types/actions/remove", json=body, discard_response=True)

    def get_inputs_by_uuids(self, input_uuids: List[str]) -> List[Input]:
        """
        Gets inputs using input uuids

        :param input_uuids: A UUID to filter inputs on
        :return List: List of Inputs
        """

        body = dict(uuids=input_uuids)
        json_resp = self._client.post("v1/inputs/query", json=body)
        return [Input.from_json(js) for js in json_resp]
