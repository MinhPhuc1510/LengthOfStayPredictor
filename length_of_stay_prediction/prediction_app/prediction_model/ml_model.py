import itertools
import pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer

GENDER = ['M', 'F']
ADMISSION_TYPE = ["EMERGENCY", "NEWBORN", "ELECTIVE", "URGENT"]
INSURANCE = ["Medicare", "Private", "Medicaid", "Government", "Self Pay"]
ETHNICITY = ["WHITE", 
            "OTHER/UNKNOWN", 
            "BLACK/AFRICAN AMERICAN",
            "HISPANIC/LATINO", 
            "ASIAN"]
MARITAL_STATUS = ["MARRIED", 
                  "SINGLE", 
                  "UNKNOWN (DEFAULT)", 
                  "WIDOWED", 
                  "DIVORCED", 
                  "SEPARATED", 
                  "LIFE PARTNER"]
AGE = ["senior", "middle_adult", "newborn", "young_adult"]
AGE_RANGES = {"newborn": (0, 13), 
              "young_adult":(13, 36), 
              "middle_adult": (36, 56), 
              "senior": (56, 100)}
FIRST_CAREUNIT = ["ICU", "NICU"]
RELIGION = ["RELIGIOUS", "NOT SPECIFIED", "UNOBTAINABLE"]
DIAGNOSIS = ['blood', 'circulatory', 'congenital', 'digestive', 'endocrine',
       'genitourinary', 'infectious', 'injury', 'mental', 'misc', 'muscular',
       'neoplasms', 'nervous', 'pregnancy', 'prenatal', 'respiratory', 'skin']
class LosModel:
    def __init__(self):
        self.selected_pipe = None
        self.new_train_pipe = None

    def load_model(self, model_file="tabular_best_pipe.bin"):
        self.model_file = model_file
        with open(self.model_file, 'rb') as file:
            self.selected_pipe = pickle.load(file)
        print(f"Model loaded from {self.model_file}")
        return self

    @staticmethod
    def __encode(x, category):
        if isinstance(x, list) or category==FIRST_CAREUNIT:
            mlb = MultiLabelBinarizer(classes=category)
            vector = mlb.fit_transform([x]).flatten()
        
        else:
            lb = LabelBinarizer()
            lb.fit(category)
        
            vector = lb.transform([x]).flatten()
        return vector
    
    @staticmethod
    def __age_to_category(age):
        return next((cat for cat, (start, end) in AGE_RANGES.items() if start <= age < end), "senior")

    def __preprocess(self, X:pd.Series):
        dia_vector = self.__encode(X["DIAGNOSIS"], DIAGNOSIS)
        gender_vector = self.__encode(X["GENDER"], GENDER)
        type_vector = self.__encode(X["ADMISSION_TYPE"], ADMISSION_TYPE)
        insurance_vector = self.__encode(X["INSURANCE"], INSURANCE)
        rel_vector = self.__encode(X["RELIGION"], RELIGION)

        ethnicity_vector = self.__encode(X["ETHNICITY"], ETHNICITY)
        marital_vector = self.__encode(X["MARITAL_STATUS"], MARITAL_STATUS)
        age_vector = self.__encode(self.__age_to_category(X["AGE"]), AGE)
        careunit_vector = self.__encode(X["FIRST_CAREUNIT"], FIRST_CAREUNIT)
        # print(dia_vector.shape)
        # print(gender_vector.shape)
        # print(careunit_vector.shape)

        # print(type_vector.shape)
        # print(insurance_vector.shape)
        # print(rel_vector.shape)
        # print(ethnicity_vector.shape)
        # print(age_vector.shape)

        # print(marital_vector.shape)

        # Concatenate all vectors
        X = np.concatenate(
            [
                dia_vector, 
                gender_vector, 
                careunit_vector,
                type_vector, 
                insurance_vector, 
                rel_vector,
                ethnicity_vector, 
                age_vector,
                marital_vector,
                rel_vector      
            ]
        )
        
        return X

    def predict(self, X: pd.Series):
        X = self.__preprocess(X).reshape(1, -1)
        if self.selected_pipe is None:
            raise ValueError("Model is not loaded or trained. Please load or train a model first.")

        y_pred = self.selected_pipe.predict(X).flatten()
        return y_pred # array([1])

    # Functions for Training
    def __init_train_pipeline(self):
        # Define methods for scaling, reducing, normalizing, and classifying
        self.scalers = {"MinMaxScaler": MinMaxScaler()}
        self.reducers = {"PCA": PCA()}
        self.normalizers = {"Normalization": MinMaxScaler()}
        self.classifiers = {
            "MultinomialNB": MultinomialNB(),
            "RandomForestClassifier": RandomForestClassifier(),
            "LogisticRegression": LogisticRegression(max_iter=2000, solver='saga'),
            "SVC": SVC(max_iter=1000),
        }

        self.pipe_steps = [
            ('scaler', self.scalers),
            ('reducers', self.reducers),
            ('normalizers', self.normalizers),
            ('classifier', self.classifiers),
        ]

        self.parameters = {
            "PCA__n_components": [0.95, 0.90],
            "LogisticRegression__C": [0.01, 0.1, 1, 10],
            "SVC__kernel": ['rbf', 'linear'],
            "SVC__C": [0.1, 1, 10],
            "MultinomialNB__alpha": [0.01, 0.1],
            "MultinomialNB__fit_prior": [True, False],
            "RandomForestClassifier__n_estimators": [100, 200],
            "RandomForestClassifier__max_depth": [10, 20, None],
        }
    
    def train(self, X_train:pd.DataFrame, y_train:pd.Series):
        self.__init_train_pipeline()
        print("Generating pipelines...")
        pipe_config = [list(step.items()) for _, step in self.pipe_steps]
        pipe_config = list(itertools.product(*pipe_config))
        pipe_names = list(map(lambda steps: [name for name, _ in steps], pipe_config))
        pipe_names = list(map(lambda L: ">".join(L), pipe_names))
        pipes = [Pipeline(cfg) for cfg in pipe_config]
        pipe_mapper = dict(zip(pipe_names, pipes))

        print("Starting hyperparameter tuning...")
        best_pipes = {}
        results = []

        for idx, pipe_name in enumerate(pipe_mapper.keys()):
            print(f"{idx + 1}. Tuning pipe: {pipe_name}")

            param_grid = {}
            for step_name in pipe_name.split('>'):
                for param_name in self.parameters.keys():
                    if param_name.startswith(step_name):
                        param_grid[param_name] = self.parameters[param_name]

            pipe = pipe_mapper[pipe_name]
            finder = GridSearchCV(pipe, param_grid=param_grid, cv=5, scoring="accuracy", refit=True)
            finder.fit(X_train, y_train)

            print(f"\t Best Params: {finder.best_params_}")
            print(f"\t Best Score (Accuracy): {finder.best_score_:0.2f}")

            best_pipes[pipe_name] = finder.best_estimator_

            rs_item = {"Method": pipe_name, "Accuracy": finder.best_score_}
            for key, value in finder.best_params_.items():
                rs_item[key] = value
            results.append(rs_item)

        tuned_table = pd.DataFrame(results)
        tuned_table.to_csv("tabular_tuned_results.csv", sep=";")

        best_method = tuned_table[tuned_table["Accuracy"] == tuned_table["Accuracy"].max()]
        selected_pipe_name = best_method["Method"][tuned_table["Accuracy"].argmax()]
        print(f"Selected Best Pipeline: {selected_pipe_name}")

        self.new_train_pipe = best_pipes[selected_pipe_name]
        return tuned_table

    def approve_model(self):
        self.__save_model()
        return self.load_model(self.model_file)

    def __save_model(self):
        if self.new_train_pipe is None:
            raise ValueError("No model to save. Train or load a model first.")

        with open(self.model_file, 'wb') as file:
            pickle.dump(self.selected_pipe, file)
        print(f"Model saved to {self.model_file}")
        


