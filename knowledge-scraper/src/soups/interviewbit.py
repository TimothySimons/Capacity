import re
from bs4 import BeautifulSoup
from src.soup import ISoup


class Soup(ISoup):

    def __init__(self, csv_path, html_file_path):
        with open(html_file_path, 'r') as html_file:
            contents = html_file.read()
            soup = BeautifulSoup(contents, 'lxml')
        super().__init__(csv_path, soup=soup)

    def find_questionnaire_elements(self):
        questions_container_element = self.soup.find("section", class_="ibpage-mcq-problems")
        questionnaire_elements = questions_container_element.find_all("section", class_="ibpage-mcq-problems__item")
        return questionnaire_elements

    def find_question_element(self, questionnaire_element):
        question_header_element = questionnaire_element.find("div", class_="ibpage-mcq-problems__header")
        question_element = question_header_element.find("p")
        return question_element

    def find_option_elements(self, questionnaire_element):
        questionnaire_elements = questionnaire_element.find_all("div", class_="ibpage-mcq-problems__options")
        option_elements = [questionnaire_element.find("p") for questionnaire_element in questionnaire_elements]
        return option_elements

    def find_answer_elements(self, questionnaire_element):
        option_element = questionnaire_element.find("div", {"data-correct": "true"})
        answer_elements = [option_element.p]
        return answer_elements

    def get_question(self, question_element):
        question = question_element.get_text().strip()
        return question

    def get_options(self, option_elements):
        options = ",".join([option_element.get_text().strip() for option_element in option_elements])
        return options

    def get_answers(self, answer_elements):
        answers = answer_elements[0].get_text().strip()
        return answers
