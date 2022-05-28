import csv
import requests
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

# TODO: create assertions that will ensure csv constraints are satisfied
#       such as answer is one of the options etc.
# TODO: create some abstract methods to do some cleaning, etc.


class ISoup(ABC):

    def __init__(self, csv_path, url=None, html=None):
        self.csv_path = csv_path
        if url:
            page = requests.get(url)
            self.soup = BeautifulSoup(page.content, "lxml")
        else:
            with open(html) as html_file:
                self.soup = BeautifulSoup(html_file, "html.parser")

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
    def find_answer_elements(self, questionnaire_element):
        pass

    @abstractmethod
    def find_explanation_element(self, questionnaire_elements):
        pass

    @abstractmethod
    def get_question(self, question_element):
        pass

    @abstractmethod
    def get_options(self, option_elements):
        pass

    @abstractmethod
    def get_answers(self, answer_elements):
        pass

    @abstractmethod
    def get_explanation(self, explanation_element):
        pass

    def soup_to_csv(self, mode):
        with open(self.csv_path, mode) as csv_file:
            csv_writer = csv.writer(csv_file)

            questionnaire_elements = self.find_questionnaire_elements()
            for questionnaire_element in questionnaire_elements:
                question_element = self.find_question_element(questionnaire_element)
                option_elements = self.find_option_elements(questionnaire_element)
                answer_elements = self.find_answer_elements(questionnaire_element)
                explanation_element = self.find_explanation_element(questionnaire_element)

                question = self.get_question(question_element)
                options = self.get_options(option_elements)
                answers = self.get_answers(answer_elements)
                explanation = self.get_explanation(explanation_element)

                csv_writer.writerow([question, options, answers, explanation])
