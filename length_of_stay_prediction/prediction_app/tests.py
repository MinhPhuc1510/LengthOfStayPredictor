from django.test import TestCase
import pandas as pd
from prediction_app.prediction_model.ml_model import LosModel

class LosModelTestCase(TestCase):
    def setUp(self):
        # Create a sample dataset
        self.sample_data = {
            'DIAGNOSIS': ['blood', 'circulatory', 'digestive', 'infectious'],
            'GENDER': ['M', 'F', 'M', 'F'],
            'ADMISSION_TYPE': ['EMERGENCY', 'ELECTIVE', 'URGENT', 'NEWBORN'],
            'INSURANCE': ['Medicare', 'Private', 'Medicaid', 'Self Pay'],
            'RELIGION': ['RELIGIOUS', 'NOT SPECIFIED', 'UNOBTAINABLE', 'RELIGIOUS'],
            'ETHNICITY': ['WHITE', 'BLACK/AFRICAN AMERICAN', 'HISPANIC/LATINO', 'ASIAN'],
            'MARITAL_STATUS': ['MARRIED', 'SINGLE', 'DIVORCED', 'WIDOWED'],
            'AGE': [25, 45, 65, 75],
            'FIRST_CAREUNIT': ['ICU', 'NICU', 'ICU', 'NICU']
        }

        # Convert to DataFrame
        self.sample_df = pd.DataFrame(self.sample_data)

    def test_model_training(self):
        # Instantiate the model
        los_model = LosModel()
        
        # Preprocess the sample data
        los_model.__preprocess(self.sample_df)
        
        # Save the model after training
        los_model.__save_model()
        
        # You can add assertions here to verify the model is saved correctly
        self.assertIsNotNone(los_model.selected_pipe)  # Check if the model pipeline is created