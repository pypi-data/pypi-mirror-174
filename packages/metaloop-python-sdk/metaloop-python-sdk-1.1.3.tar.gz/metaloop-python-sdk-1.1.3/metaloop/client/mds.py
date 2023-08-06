"""The implementation of the metaloop data service."""

import logging
import re
import time
from typing import List

from metaloop.client.cloud_storage import CloudClient
from metaloop.client.requests import Client
from metaloop.client.x_api import X_API
from metaloop.dataset import Dataset
from metaloop.exception import *

logger = logging.getLogger(__name__)
DEFAULT_BRANCH = "main"


class MDS:
    """:class:`MDS` defines the initial client to interact with MetaLoop.

    :class:`MDS` provides some operations on dataset level such as
    :meth:`MDS.create_dataset` :meth:`MetaLoop.get_dataset` and :meth:`MetaLoop.delete_dataset`.

    Arguments:
        access_key: User's access key.
        url: The host URL of the MetaLoop website.

    """

    def __init__(self, access_key: str, url: str = 'http://data.deepglint.com/') -> None:
        self._client = Client(access_key, url)
        self._cloud_client = CloudClient()
        self._x_api = X_API(self._client)

    @property
    def cloud_client(self):
        return self._cloud_client

    @property
    def x_api(self):
        return self._x_api

    def create_dataset(
            self,
            name: str,
            data_type: str,
            tags: List[str],
            space: Optional[str] = "",
            comment: Optional[str] = "",
    ) -> Dataset:
        """Create a MetaLoop dataset with given name.

        Arguments:
            name: Name of the dataset, unique for platform.
            data_type: Type of the dataset, support 'image', 'video' or 'none'.
            tags: Tags of the dataset, used for dataset searching.
            space: Space where the dataset is belonged to, default is empty means personal dataset.
            comment: Comment of the dataset, default is "".

        Returns:
            The created :class:`~metaloop.dataset.dataset.Dataset` instance.

        """
        if len(name) > 35:
            raise InvalidParamsError(message="length of name cannot exceed 35")

        if not re.match("^[A-Za-z0-9-_\u4e00-\u9fa5]+$", name):
            raise InvalidParamsError(message="invalid name, only support A-Z, a-z, 0-9, -, _ and Chinese")

        if data_type not in {"image", "video", "none"}:
            raise InvalidParamsError(param_name="data_type", param_value=data_type)

        try:
            self._x_api.get_dataset_name(name)
            raise NameConflictError(resource="dataset", identification=name)
        except ResourceNotExistError:
            pass

        if space:
            self._x_api.get_space(space)

        tag_ids = []
        for item in tags:
            try:
                tag = self._x_api.get_tag(item)
                tag_ids.append(tag["id"])
            except IndexError:
                pass

        post_data = {
            "name": name,
            "data_type": data_type,
            "project": space,
            "tags": tag_ids,
            "comment": comment,
        }

        info = self._x_api.create_dataset(post_data)
        dataset_id = info["id"]
        version = info["version"]
        created_user = info["created_user"]
        created_time = int(time.time() * 1e3)
        versions = {0: dataset_id}

        return Dataset(
            self,
            name,
            data_type,
            space,
            dataset_id,
            version,
            tags=tags,
            created_user=created_user,
            create_timestamp=created_time,
            versions=versions,
            comment=comment
        )

    def _info_to_dataset(self, info) -> Dataset:
        name = info["name"]
        data_type = info["data_type"]
        space = info["project"]
        tags = info["tag_names"]
        created_user = info["created_user"]
        create_timestamp = info["create_timestamp"]
        versions = info["versions"]
        source = info["source"]
        meta_comment = info["comment"]

        if len(versions) == 0:
            raise InternalServerError

        version_info: Dict[int, str] = {}
        for version in versions:
            version_info[int(version["version"])] = version["id"]

        dataset_info = versions[0]
        dataset_id = dataset_info["id"]
        comment = dataset_info["comment"]
        data_count = dataset_info["data_count"]
        version = dataset_info["version"]
        annotation_status = dataset_info["annotation_status"]
        last_import_status = dataset_info["last_import_status"]
        last_data_clean_status = dataset_info["last_data_clean_status"]
        attachment_url = dataset_info["attachment_url"] if "attachment_url" in dataset_info else ""

        return Dataset(
            self,
            name,
            data_type,
            space,
            dataset_id,
            version,
            tags=tags,
            created_user=created_user,
            create_timestamp=create_timestamp,
            versions=version_info,
            source=source,
            meta_comment=meta_comment,
            comment=comment,
            data_count=data_count,
            annotation_status=annotation_status,
            last_import_status=last_import_status,
            last_data_clean_status=last_data_clean_status,
            attachment_url=attachment_url
        )

    def get_dataset(self, name: str) -> Dataset:
        """Get a dataset with given name.

        Arguments:
            name: The name of the requested dataset.

        Returns:
            The requested :class:`~metaloop.dataset.dataset.Dataset` instance

        """
        info = self._x_api.get_dataset(name)
        return self._info_to_dataset(info)

    def list_dataset(self, name: Optional[str] = "") -> List[Dataset]:
        """List datasets

        Arguments:
            name: The name of the requested dataset.

        Returns:
            The requested : List[class]:`~metaloop.dataset.dataset.Dataset` instance

        """
        ds = List[Dataset]
        response = self._x_api.list_datasets(name)
        try:
            total_count = response["total_count"]
            count = response["count"]
            for i in range(count):
                ds.append(self._info_to_dataset(response["data"][i]))
        except IndexError as error:
            raise ResourceNotExistError(resource="dataset", identification=name) from error
        return ds

    def delete_dataset(
            self,
            name: str,
            version_number: Optional[int] = None
    ) -> None:
        """Delete a MetaLoop dataset with given name and given version number.
        If the version number is not specified, the whole dataset will be removed.

        Arguments:
            name: Name of the dataset.
            version_number: Version number of the dataset.

        """
        dataset = self.get_dataset(name)
        if version_number:
            dataset.delete_version(version_number)
            return

        for dataset_id in dataset.versions.values():
            self._client.open_api_do("DELETE", "", dataset_id)

        dataset._id = None
        dataset._version = -1

    def create_s3_storage_config(
            self,
            identifier: str,
            endpoint: str,
            access_key_id: str,
            secret_access_key: str,
            default_bucket: str
    ) -> None:
        """Create a s3 auth storage config.

        Arguments:
            identifier: Custom identifier of the s3 config.
            endpoint: Endpoint of the s3.
            access_key_id: access_key_id of the s3.
            secret_access_key: secret_access_key of the s3.
            default_bucket: The authorized or default bucket of s3.

        """
        self._cloud_client.set_s3_config(
            identifier,
            endpoint,
            access_key_id,
            secret_access_key,
            default_bucket
        )
