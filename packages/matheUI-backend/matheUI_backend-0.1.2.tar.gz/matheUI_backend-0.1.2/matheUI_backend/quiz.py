from typing import Union

import pandas as pd

from matheUI_backend.config import QUIZ_DATA_FILES, QUIZ_DATA_FOLDER

from .abstractGame import AbstactGame


class Quiz(AbstactGame):
    """ Quiz backend """

    def __init__(self, data_folder_path: str = QUIZ_DATA_FOLDER, data_files: dict[str, str] = QUIZ_DATA_FILES):
        """
        @params:
            data_folder_path: path to the folder with the quiz data (Form: '/....../')
            data_files: dictionary with name of the quiz category and file name of the data (Form: {'physics': 'quiz_physics.csv'})
        """
        self.data_folder_path = data_folder_path
        self.data_files = data_files

        self.quiz_categories: dict[str, pd.DataFrame] = {}
        for category in list(data_files.keys()):
            self.quiz_categories[category] = self._load_csv_dataframe(data_folder_path+data_files[category])

    def data_report(self):
        print(f"{len(self.get_categories())} categories:")
        for category in self.get_categories():
            print(f"    {category}: {len(self.get_df(category))}")

    def get_categories(self) -> list[str]:
        return list(self.quiz_categories.keys())

    def get_df(self, category: str) -> pd.DataFrame:
        return self.quiz_categories[category]

    def add_question(
        self,
        category: str,
        question: str,
        solution: str,
        fake_answer1: str,
        fake_answer2: str,
        fake_answer3: str,
        info: str,
    ):
        question_df = Quiz.create_questions_df([question], [solution], [fake_answer1], [fake_answer2], [fake_answer3], [info])
        self.add_questions(category, question_df)

    def add_questions(self, category: str, question_df: pd.DataFrame):
        self.quiz_categories[category] = self.quiz_categories[category].append(question_df, ignore_index=True)

    def delete_question(self, category: str, row_index: int):
        self.quiz_categories[category].drop(index=row_index, inplace=True)
        self.quiz_categories[category].reset_index(inplace=True, drop=True)

    @staticmethod
    def create_questions_df(
        questions: list[str],
        solutions: list[str],
        fake_answers1: list[str],
        fake_answers2: list[str],
        fake_answers3: list[str],
        infos: list[str],
    ) -> pd.DataFrame:
        df = pd.DataFrame(columns=["QUESTION", "SOLUTION", "FAKE_ANSWER_1", "FAKE_ANSWER_2", "FAKE_ANSWER_3", "INFO"])
        df["QUESTION"] = questions
        df["SOLUTION"] = solutions
        df["FAKE_ANSWER_1"] = fake_answers1
        df["FAKE_ANSWER_2"] = fake_answers2
        df["FAKE_ANSWER_3"] = fake_answers3
        df["INFO"] = infos
        return df

    def update_data_files(self):
        """ function to update the data files with self.quiz_categories content """
        print("Do you want to save the following data? (yes/no)")
        self.data_report()
        print("answer:")
        answer = input()
        if answer == "yes":
            for category in self.get_categories():
                self._save_dataframe(self.quiz_categories[category], self.data_folder_path+self.data_files[category])
            print("data files updated")
        else:
            print("process stopped")

    def generate_round(self, question_number: int = 10, categories: Union[str, list] = "all") -> pd.DataFrame:
        """
        @params:
            question_number: how many questions shall be picked (if number is greater than max questions for the categories, the maximum will be used)
            categories: from which categories shall the question be picked. List of categories or name of category (if 'all', use all available categories)

        @return:
            pandas Dataframe with picked questions and columns "QUESTION", "SOLUTION", "FAKE_ANSWER_1", "FAKE_ANSWER_2", "FAKE_ANSWER_3", "INFO"
        """
        if categories == "all":
            categories = self.get_categories()
        elif type(categories) == str:
            categories = [categories]

        possible_questions: pd.DataFrame = pd.DataFrame(columns=["QUESTION", "SOLUTION", "FAKE_ANSWER_1", "FAKE_ANSWER_2", "FAKE_ANSWER_3", "INFO"])
        for category in categories:
            possible_questions= possible_questions.append(self.quiz_categories[category], ignore_index=True)

        if question_number > len(possible_questions):
            print(f"INFO: there only {len(possible_questions)} questions available -> will use all")
            question_number = len(possible_questions)

        questions = possible_questions.sample(n=question_number, ignore_index=True)

        return questions
