import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List
from data_operator import RecipesClient
from html_generator import get_html


class ClientFacade(ABC):
    dst_path: str

    @abstractmethod
    def get_recipes(self, ingredients: List[str], exclude: List[str] = []) -> Any:
        pass


class RecipesClientFacade(ClientFacade):
    def __init__(self, dst_path: Path = os.getcwd()):
        self.dst_path = dst_path

    def get_recipes(self, ingredients: List[str], exclude: List[str] = []) -> Any:
        if not exclude:
            exclude = ['plums']

        if 'plums' in ingredients:
            exclude.remove('plums')

        include_ingr: str = ",".join(sorted(ingredients))
        exclude_ingr: str = ",".join(sorted(exclude))

        data_manager = RecipesClient()
        data = data_manager.make_request_or_get_db(data_manager.give_hash_key(include_ingr, exclude_ingr), include_ingr, exclude_ingr)
        get_html(data)

#Example of using program
#RecipesClientFacade().get_recipes(['honey'])

