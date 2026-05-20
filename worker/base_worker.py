# -*- coding: utf-8 -*-
import abc

class BaseWorker(abc.ABC):
    def __init__(self, campaign_id):
        self.campaign_id = campaign_id
    @abc.abstractmethod
    def run(self):
        pass
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")
