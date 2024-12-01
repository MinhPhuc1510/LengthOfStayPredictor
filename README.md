# Length of Stay Prediction App

This project is a Django web application for predicting the length of hospital stays based on patient demographics and illness type using the Random Forest algorithm.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)

## Features

- Input patient demographics: gender, age, and illness.
- Predict the length of hospital stay (Short Term, Medium Term, Long Term).
- User-friendly interface with form validation.

## Technologies Used

- Python
- Django
- scikit-learn (for Random Forest algorithm)
- SQLite (default database)
- HTML, CSS (for frontend)

## Setup Instructions

To set up and run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/LengthOfStayPredictor.git
   cd length_of_stay_prediction
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Open your web browser and go to:**

   ```
   http://127.0.0.1:8000/
   ```

## Usage

- Fill in the form with patient details: gender, age, and illness.
- Click on the "Predict" button to get the predicted length of stay..

