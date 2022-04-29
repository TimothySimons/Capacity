import csv
import requests
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class ISoup(ABC):

    def __init__(self, csv_path, url=None, soup=None):
        self.csv_path = csv_path
        self.csv_headers = ["questions", "options", "answers"]

        if url:
            page = requests.get(url)
            self.soup = BeautifulSoup(page.content, "lxml")
        else:
            self.soup = soup

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
    def get_question(self, question_element):
        pass

    @abstractmethod
    def get_options(self, option_elements):
        pass

    @abstractmethod
    def get_answers(self, answer_elements):
        pass

    def soup_to_csv(self):
        with open(self.csv_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.csv_headers)

            questionnaire_elements = self.find_questionnaire_elements()
            for questionnaire_element in questionnaire_elements:
                question_element = self.find_question_element(questionnaire_element)
                option_elements = self.find_option_elements(questionnaire_element)
                answer_elements = self.find_answer_elements(questionnaire_element)

                question = self.get_question(question_element)
                options = self.get_options(option_elements)
                answers = self.get_answers(answer_elements)

                csv_writer.writerow([question, options, answers])
