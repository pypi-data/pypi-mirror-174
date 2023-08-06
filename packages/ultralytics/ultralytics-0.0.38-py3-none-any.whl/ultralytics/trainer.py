import requests

from .config import HUB_API_ROOT
from .hub_logger import HUBLogger
from .yolov5_utils.hub_utils import check_dataset_disk_space, smart_post
from .yolov5_wrapper import YOLOv5Wrapper as YOLOv5


class Trainer:

    def __init__(self, model_id, auth):
        self.auth = auth
        self.model = self._get_model(model_id)
        if self.model is not None:
            self._connect_callbacks()

    def _get_model_by_id(self):
        # return a specific model
        return

    def _get_next_model(self):
        # return next model in queue
        return

    def _get_model(self, model_id):
        """
        Returns model from database by id
        """
        api_url = f"{HUB_API_ROOT}/model"
        payload = {"modelId": model_id, **self.auth.get_auth_string()}

        try:
            r = smart_post(api_url, json=payload, thread=False, code=0)
            data = r.json()["data"]
            assert data['data'], 'ERROR: Dataset may still be processing. Please wait a minute and try again.'  # RF fix
            self.model_id = data["id"]
            return data
        except requests.exceptions.ConnectionError as e:
            raise Exception('ERROR: The HUB server is not online. Please try again later.') from e

    def _connect_callbacks(self):
        callback_handler = YOLOv5.new_callback_handler()
        hub_logger = HUBLogger(self.model_id, self.auth)
        callback_handler.register_action("on_pretrain_routine_start", "HUB", hub_logger.on_pretrain_routine_start)
        callback_handler.register_action("on_pretrain_routine_end", "HUB", hub_logger.on_pretrain_routine_end)
        callback_handler.register_action("on_fit_epoch_end", "HUB", hub_logger.on_fit_epoch_end)
        callback_handler.register_action("on_model_save", "HUB", hub_logger.on_model_save)
        callback_handler.register_action("on_train_end", "HUB", hub_logger.on_train_end)
        self.callbacks = callback_handler

    def start(self):
        # Checks
        if not check_dataset_disk_space(self.model['data']):
            return

        # Train
        YOLOv5.train(self.callbacks, **self.model)
