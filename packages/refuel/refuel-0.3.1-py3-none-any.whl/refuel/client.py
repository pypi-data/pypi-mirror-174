import concurrent.futures as pyfutures
import json
import math
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd
from loguru import logger
from requests_futures.sessions import FuturesSession

from refuel.types import DatasetEvent, Event, EventBatch
from refuel.utils import DATE_FOURTEEN_DAYS_AGO, DATE_TOMORROW


class RefuelClient:
    # Default config settings
    API_BASE_URL = "https://api.refuel.ai"
    API_KEY_ENV_VARIABLE = "REFUEL_API_KEY"
    TIMEOUT_SECS = 15
    MAX_RETRIES = 3
    MAX_WORKERS = 4 * os.cpu_count()
    DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    MAX_BYTES_PER_BATCH = 3000000  # 3 MB
    MAX_EVENTS_PER_BATCH = 100
    DEFAULT_QUEUE_NAME = "default"
    DEFAULT_DATASET_NAME = "default"
    DEFAULT_ORDERING = "recent"
    DEFAULT_MAX_QUERY_EVENTS = 1000000
    QUERY_STEP_SIZE = 100

    def __init__(
        self,
        api_key: str = None,
        api_base_url: str = API_BASE_URL,
        timeout: int = TIMEOUT_SECS,
        max_retries: int = MAX_RETRIES,
        max_workers: int = MAX_WORKERS,
    ) -> None:
        """
        Args:
            api_key (str, optional): Refuel API Key. Defaults to None.
            api_base_url (str, optional): Base URL of the Refuel API endpoints. Defaults to API_BASE_URL.
            timeout (int, optional): Timeout (secs) for a given API call. Defaults to TIMEOUT_SECS.
            max_retries (int, optional): Max num retries. Defaults to MAX_RETRIES.
            max_workers (int, optional): Max number of concurrent tasks in the ThreadPoolExecutor
        """
        # initialize variables
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV_VARIABLE)
        self._api_base_url = api_base_url
        self._timeout = timeout
        self._header = {"Content-Type": "application/json", "x-api-key": self._api_key}
        # initialize request session
        adapter_kwargs = {"max_retries": max_retries}
        self._session = FuturesSession(
            max_workers=max_workers, adapter_kwargs=adapter_kwargs
        )

        # Get initialization context from Refuel
        if not self._api_key or not isinstance(self._api_key, str):
            logger.error(f"API Key is absent or invalid: {self._api_key}. logged")
            self._init_context = {}
        else:
            init_response = self._get(url=self._api_base_url + "/init").result()
            self._init_context = init_response.json()

    def _get(self, url: str, params: Dict = None) -> pyfutures.Future:
        # print(self._session.get(url, headers=self._header, params=params).url())
        return self._session.get(url, headers=self._header, params=params)

    def _post(self, url: str, body: str) -> pyfutures.Future:
        return self._session.post(
            url, headers=self._header, timeout=self._timeout, data=body
        )

    def _chunkify_events(self, events: List) -> List:
        if len(events) == 0:
            return []
        # approximate how large is each event
        bytes_per_event = len(json.dumps(events[0]).encode("utf-8"))
        # calculate num events in each chunk
        nbytes = bytes_per_event * len(events)
        nchunks = math.floor(nbytes / self.MAX_BYTES_PER_BATCH) + 1
        width = math.floor(len(events) / nchunks) + 1
        width = min(width, self.MAX_EVENTS_PER_BATCH)
        # chunkify
        return [events[i : i + width] for i in range(0, len(events), width)]

    def log(
        self,
        model_name: str,
        x: Dict,
        y_pred: Dict,
        y_true: Dict = None,
        metadata: Dict = None,
        dataset_name: str = DEFAULT_DATASET_NAME,
    ) -> pyfutures.Future:
        """
        Log individual events to the Refuel platform.

        Args:
            model_name (str): _description_
            dataset_name (str): _description_
            x (dict): _description_
            y_pred (dict): _description_
            y_true (dict, optional): _description_. Defaults to None.
            metadata (dict, optional): _description_. Defaults to None.

        Returns:
            pyfutures.Future: _description_
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        event = Event(
            model_name, dataset_name, client_timestamp, x, y_pred, y_true, metadata
        )
        return self._post(url=self._api_base_url + "/log", body=event.serialize())

    def log_batch(
        self, model_name: str, events: List, dataset_name: str = DEFAULT_DATASET_NAME
    ) -> List[pyfutures.Future]:
        """_summary_

        Args:
            model_name (str): _description_
            dataset_name (str): _description_
            events (List): _description_

        Returns:
            List[pyfutures.Future]: _description_
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        chunks = self._chunkify_events(events)
        futures = []
        for chunk in chunks:
            batch = EventBatch(model_name, dataset_name, client_timestamp, chunk)
            futures.append(
                self._post(
                    url=self._api_base_url + "/log_batch", body=batch.serialize()
                )
            )
        return futures

    def log_dataset(
        self, model_name: str, dataset_name: str, s3_uri: str, dataset_config: dict
    ) -> pyfutures.Future:
        """Log dataset to the Refuel platform.

        Args:
            model_name (str): model to log dataset to
            dataset_name (str): name of dataset
            s3_uri (str): s3 uri or presigned url to dataset
            dataset_config (dict): configuration for the dataset

        Returns:
            pyfutures.Future:
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)

        dataset_event = DatasetEvent(
            model_name, dataset_name, client_timestamp, s3_uri, dataset_config
        )

        return self._post(
            url=self._api_base_url + "/log_dataset", body=dataset_event.serialize()
        )

    def _query_helper(self, url: str, params: Dict = None) -> pd.DataFrame:
        model_name = params.get("model_name", None)
        max_events = params.get("max_events")
        offset = params.get("offset", 0)

        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        events = []
        while len(events) < max_events:
            params["offset"] = len(events) + offset
            params["max_events"] = (
                min(max_events - len(events), RefuelClient.QUERY_STEP_SIZE),
            )

            response = self._get(url=url, params=params).result()

            if response.status_code != 200:
                logger.error(
                    "Status code: {} received with response: {}",
                    response.status_code,
                    response.text,
                )
                return None

            json_response = response.json()
            result = json_response.get("result", [])
            if len(result) == 0:
                break

            events += result

            # check if API sends a `count` value and break when number of events exceeds the count
            if json_response.get("count") and len(events) + offset >= json_response.get(
                "count"
            ):
                break

        return pd.DataFrame.from_records(events)

    def query_events(
        self,
        model_name: str,
        dataset_name: str = DEFAULT_DATASET_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        order_by: str = DEFAULT_ORDERING,
        offset: int = 0,
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
        include_embeddings: bool = False,
        embedding_column: str = None,
    ) -> pd.DataFrame:
        """
        Query events from the Refuel platform.

        Args:
            model_name (str): Refuel model to query
            dataset_name (str): dataset within model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        if (
            dataset_name
            not in self._init_context.get("datasets", {model_name: []})[model_name]
        ):
            logger.error(
                f"Dataset name: {dataset_name} does not exist for model {model_name}"
            )
            return None
        
        params = {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "time_start": time_start,
            "time_end": time_end,
            "order_by": order_by,
            "offset": offset,
            "max_events": max_events,
            "filters": json.dumps(filters),
            "include_embeddings": include_embeddings,
        }
        if embedding_column:
            params["embedding_column"] = embedding_column
        return self._query_helper(url=self._api_base_url + "/query", params=params)

    def query_annotation_queue(
        self,
        model_name: str,
        queue_name: str = DEFAULT_QUEUE_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        order_by: str = DEFAULT_ORDERING,
        offset: int = 0,
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
    ) -> pd.DataFrame:
        """
        Query events from the review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        params = {
            "model_name": model_name,
            "queue_name": queue_name,
            "time_start": time_start,
            "time_end": time_end,
            "order_by": order_by,
            "offset": offset,
            "max_events": max_events,
            "filters": json.dumps(filters),
        }
        return self._query_helper(
            url=self._api_base_url + "/query_annotation_queue", params=params
        )

    def query_similar_events(
        self,
        model_name: str,
        refuel_uuid: str,
        embedding_column: str = None,
        dataset_name: str = DEFAULT_DATASET_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
    ) -> pd.DataFrame:
        """
        Query events from the review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        if (
            dataset_name
            not in self._init_context.get("datasets", {model_name: []})[model_name]
        ):
            logger.error(
                f"Dataset name: {dataset_name} does not exist for model {model_name}"
            )
            return None

        params = {
            "model_name": model_name,
            "refuel_uuid": refuel_uuid,
            "embedding_column": embedding_column,
            "dataset_name": dataset_name,
            "time_start": time_start,
            "time_end": time_end,
            "max_events": max_events,
            "fitlers": json.dumps(filters),
        }
        return self._query_helper(
            url=self._api_base_url + "/query_similar_events", params=params
        )
