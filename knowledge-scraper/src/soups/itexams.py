import re

from src.soup import ISoup

# > account details <
# ===================
# username: deleteme
# password: password


class Soup(ISoup):

    def find_questionnaire_elements(self, beautiful_soup):
        questions_container_element = beautiful_soup.find("div", class_="questions_container")
        questionnaire_elements = questions_container_element.find_all("div", class_="card")
        return questionnaire_elements

    def find_question_element(self, questionnaire_element):
        question_element = questionnaire_element.find("div", "question_text").p
        return question_element

    def find_option_elements(self, questionnaire_element):
        option_elements = questionnaire_element.find_all("li")
        return option_elements

    def find_answer_elements(self, questionnaire_element):
        answer_elements = [questionnaire_element.find("div", {'class': re.compile(r'answer_block*')}).p.strong]
        return answer_elements

    def find_explanation_element(self, questionnaire_elements):
        return ""

    def get_question(self, question_element):
        question = question_element.get_text().strip()
        return question

    def get_options(self, option_elements):
        options = [option_element.get_text().strip() for option_element in option_elements]
        return options

    def get_answers(self, answer_elements):
        answers = answer_elements[0].get_text().strip().split(",")
        return answers

    def get_explanation(self, explanation_element):
        return ""

    def process(self, question, options, answers, explanation):
        answers = [option for option in options if option[0] in answers]
        options = [option[3:] for option in options]  # e.g. remove "B.*space*" from "B.*space*rsyslog"
        answers = [answer[3:] for answer in answers]
        return question, options, answers, explanation

