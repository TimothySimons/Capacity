import requests
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Soup(ABC):

    def __init__(self, url):
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, "lxml")

    @abstractmethod
    def find_questionnaire_elements(self):
        pass

    @abstractmethod
    def find_question_element(self, questionnaire_element):
        pass

    @abstractmethod
    def find_option_elements(self, questionnaire_element):
        pass

    @abstractmethod
    def find_answer_element(self, questionnaire_element):
        pass

    @abstractmethod
    def get_question(self, question_element):
        pass

    @abstractmethod
    def get_options(self, option_element):
        pass

    @abstractmethod
    def get_answer(self, answer_element):
        pass

    def soup_to_csv(self):
        questionnaire_elements = self.find_questionnaire_elements()