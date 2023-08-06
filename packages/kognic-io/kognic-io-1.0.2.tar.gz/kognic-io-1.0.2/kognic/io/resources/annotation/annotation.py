from typing import Optional, Generator

from kognic.io.model.annotation.client_annotation import Annotation, PartialAnnotation
from kognic.io.resources.abstract import IOResource


class AnnotationResource(IOResource):

    def get_project_annotations(self, project: str, annotation_type: str, batch: Optional[str] = None) -> Generator[Annotation, None, None]:
        url = f"v1/annotations/projects/{project}/"
        if batch:
            url += f"batch/{batch}/"

        url += f"annotation-type/{annotation_type}/search"

        for js in self._paginate_get(url):
            partial_annotation = PartialAnnotation.from_json(js)
            content = self._file_client.get_json(partial_annotation.uri)
            yield partial_annotation.to_annotation(content)

    def get_annotation(self, input_uuid: str, annotation_type: str) -> Annotation:
        json_resp = self._client.get(f"v1/annotations/inputs/{input_uuid}/annotation-type/{annotation_type}")
        annotation = Annotation.from_json(json_resp)
        return annotation
