import csv
import os
import requests
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class ISoup(ABC):

    def __init__(self):
        self.beautiful_soups = []

    def add_ingredient(self, url=None, html=None):
        if url:
            page = requests.get(url)
            beautiful_soup = BeautifulSoup(page.content, "lxml")
            self.beautiful_soups.append(beautiful_soup)
        elif html:
            with open(html, "r") as html_file:
                beautiful_soup = BeautifulSoup(html_file, "html.parser")
            self.beautiful_soups.append(beautiful_soup)

    @abstractmethod
    def find_questionnaire_elements(self, beautiful_soup):
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

    @abstractmethod
    def process(self, question, options, answers, explanation):
        pass

    def pour(self, csv_path):
        try:
            for beautiful_soup in self.beautiful_soups:
                self.soup_to_csv(beautiful_soup, csv_path, "a")
        except Exception as exception:
            _clean_up(csv_path)
            raise exception

    def soup_to_csv(self, beautiful_soup, csv_path, mode):
        with open(csv_path, mode) as csv_file:
            csv_writer = csv.writer(csv_file)

            questionnaire_elements = self.find_questionnaire_elements(beautiful_soup)
            for questionnaire_element in questionnaire_elements:
                question_element = self.find_question_element(questionnaire_element)
                option_elements = self.find_option_elements(questionnaire_element)
                answer_elements = self.find_answer_elements(questionnaire_element)
                explanation_element = self.find_explanation_element(questionnaire_element)

                question = self.get_question(question_element)
                options = self.get_options(option_elements)
                answers = self.get_answers(answer_elements)
                explanation = self.get_explanation(explanation_element)
                question, options, answers, explanation = self.process(question, options, answers, explanation)
                _validate(question, options, answers, explanation)

                options = ",".join(options)
                answers = ",".join(answers)
                csv_writer.writerow([question, options, answers, explanation])


def _clean_up(csv_path):
    if os.path.exists(csv_path):
        os.remove(csv_path)


def _validate(question, options, answers, explanation):
    if not type(question) == str:
        raise ValueError(f"question expects type str\nquestion: {question}")
    elif not all(type(option) == str for option in options):
        raise ValueError(f"options expects a list of type str\noptions: {options}")
    elif not all(type(answer) == str for answer in answers):
        raise ValueError(f"answers expects a list of type str\nanswers: {answers}")
    elif not type(explanation) == str:
        raise ValueError(f"explanation expects type str\nexplanation: {explanation}")
    elif not question:
        raise ValueError("question must not be an empty string")
    elif not all(answer in options for answer in answers):
        raise ValueError(f"options must contain all answers\noptions: {options}\nanswers: {answers}")
