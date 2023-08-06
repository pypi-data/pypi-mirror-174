import json
from typing import Dict, Any, Optional, List

from requests_toolbelt import MultipartEncoder
from s3transfer.constants import MB

from metaloop.client.requests import Client
from metaloop.exception import ResourceNotExistError, InvalidParamsError, InternalServerError
from urllib import parse


class X_API:
    def __init__(self, client: Client):
        self._client = client

    def create_dataset(
            self,
            post_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._client.open_api_do("POST", "", json=post_data).json()
        return response["data"][0]

    def delete_dataset(
            self,
            dataset_id: str
    ) -> None:
        self._client.open_api_do("DELETE", "", dataset_id)

    def get_version(
            self,
            dataset_id: str
    ) -> Dict[str, Any]:
        response = self._client.open_api_do("GET", "", dataset_id).json()
        return response["data"][0]

    def get_dataset(
            self,
            name: str
    ) -> Dict[str, Any]:
        if not name:
            raise InvalidParamsError(param_name="dataset", param_value=name)

        response = self.list_datasets(name=name)

        try:
            info = response["data"][0]
        except IndexError as error:
            raise ResourceNotExistError(resource="dataset", identification=name) from error

        return info

    def list_datasets(
            self,
            name: Optional[str] = None,
            offset: int = 0,
            limit: int = 128,
    ) -> Dict[str, Any]:
        post_data: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
        }
        if name:
            post_data["name"] = [name]

        response = self._client.open_api_do("POST", "search/dataset", json=post_data)
        return response.json()

    def get_space(self, name: str) -> Dict[str, Any]:
        if not name:
            raise InvalidParamsError(param_name="space", param_value=name)

        response = self.list_spaces(name=name)

        try:
            info = response["data"][0]
        except IndexError as error:
            raise ResourceNotExistError(resource="space", identification=name) from error

        return info

    def list_spaces(
            self,
            name: Optional[str] = None,
            offset: int = 0,
            limit: int = 128,
    ) -> Dict[str, Any]:
        post_data: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
        }
        if name:
            post_data["name"] = [name]

        response = self._client.open_api_do("POST", "search/space", json=post_data)
        return response.json()

    def get_tag(self, name: str) -> Dict[str, Any]:
        if not name:
            raise InvalidParamsError(param_name="tag", param_value=name)

        try:
            response = self.list_tags(name=name)
            info = response["data"][0]
        except IndexError as error:
            raise ResourceNotExistError(resource="tag", identification=name) from error

        return info

    def list_tags(
            self,
            name: Optional[str] = None,
            offset: int = 0,
            limit: int = 128,
    ) -> Dict[str, Any]:
        post_data: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "accurate": True
        }
        if name:
            post_data["name"] = [name]

        response = self._client.open_api_do("POST", "search/tag", json=post_data)
        return response.json()

    def get_authorized_s3_config(
            self,
            name: Optional[str] = "",
            storage_type: Optional[str] = ""
    ) -> Dict[str, Any]:
        if not name and not storage_type:
            raise InvalidParamsError(message="name and type of cloud storage need at least one")

        bucket_or_type = ''
        if name:
            bucket_or_type = name
        elif storage_type:
            bucket_or_type = storage_type

        response = self._client.open_api_do("GET", "api_s3_storage_config?bucket=" + bucket_or_type).json()

        try:
            s3_resp = response["data"]["s3"]
            s3_parsed = parse.urlparse(s3_resp)
            query = parse.parse_qs(s3_resp)
            endpoint = 'http://'
            if 'sslmode' in query and query['sslmode'] == "enable":
                endpoint = 'https://'
            endpoint = endpoint + s3_parsed.hostname
            if s3_parsed.port > 0 and s3_parsed.port != 80:
                endpoint = endpoint + ":" + str(s3_parsed.port)
            info: Dict[str, Any] = {
                "name": bucket_or_type,
                "endpoint": endpoint,
                "access_key": s3_parsed.username,
                "bucket": s3_parsed.path.strip('/'),
                "secret_key": s3_parsed.password
            }
        except IndexError:
            raise ResourceNotExistError(resource="cloud storage config", identification=f"{name}({storage_type})")

        return info

    def post_import(
            self,
            dataset_id: str,
            post_data: str
    ) -> None:
        self._client.open_api_do("POST", "import", dataset_id, json=post_data)

    def get_import_status(
            self,
            dataset_id: str
    ) -> Dict[str, Any]:
        response = self._client.open_api_do("GET", "import", dataset_id).json()

        try:
            info = response["data"][0]
        except IndexError as error:
            raise InternalServerError(message="cannot get import status from server") from error

        return info

    def post_export(
            self,
            dataset_id: str,
            post_data: str
    ) -> None:
        self._client.open_api_do("POST", "export", dataset_id, json=post_data)

    def get_export_status(
            self,
            dataset_id: str
    ) -> Dict[str, Any]:
        response = self._client.open_api_do("GET", "export", dataset_id).json()

        try:
            info = response["data"][0]
        except IndexError as error:
            raise InternalServerError(message="cannot get export status from server") from error

        return info

    def get_export_catalog(
            self,
            url: str
    ) -> List[str]:
        if url.find("abaddonapi") > -1:
            section = url.split("abaddonapi/v1/")[1]
            response = self._client.open_api_do("GET", section, "", stream=True)
        else:
            response = self._client.do("GET", url)

        export_list: List[Any] = []
        for line in response.iter_lines(chunk_size=1 * MB):
            export_list.append(json.loads(line))

        return export_list

    def post_multipart_formdata(
            self,
            data: Dict[str, Any]
    ) -> str:
        multipart = MultipartEncoder(data)

        try:
            response = self._client.open_api_do(
                "POST",
                "upload",
                data=multipart,
                headers={"Content-Type": multipart.content_type},
            ).json()
            info = response["data"][0]
        except IndexError as error:
            raise InternalServerError(message="cannot get upload status from server") from error

        return info["upload_id"]

    def get_stream_data(
            self,
            url: str,
            file_path: str
    ) -> None:
        response = self._client.open_api_do("GET", url, "", stream=True)

        with open(file_path, "wb") as f:
            for ch in response:
                f.write(ch)
            f.close()
