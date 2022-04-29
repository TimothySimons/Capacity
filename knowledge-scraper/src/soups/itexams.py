import re

from src.soup import ISoup

# > account details <
# ===================
# username: deleteme
# password: password


class Soup(ISoup):

    def find_questionnaire_elements(self):
        questions_container_element = self.soup.find("div", class_="questions_container")
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

    def get_question(self, question_element):
        question = question_element.get_text().strip()
        print(f"question: {question}")
        return question

    def get_options(self, option_elements):
        options = ",".join([option_element.get_text().strip() for option_element in option_elements])
        print(f"options: {options}")
        return options

    def get_answers(self, answer_elements):
        answers = answer_elements[0].get_text().strip()
        print(f"answers : {answers}")
        return answers
