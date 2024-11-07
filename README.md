# Solon Labs

**Solon Labs** is a web application designed to streamline the interaction between doctors and patients. Patients can upload their medical records, test results, and prescriptions to the platform, which doctors can access, review, and update. The platform also includes Machine Learning models for providing a second opinion on specific conditions like skin cancer, lung cancer, and eye problems, helping doctors make more informed decisions.

## Features

- **Patient Portal**: Patients can securely upload test results, prescriptions, and other medical records.
- **Doctor Portal**: Doctors have access to patients' uploaded records and can make updates as needed.
- **Machine Learning Models**: Integrated ML models to provide second opinions on diagnoses related to skin cancer, lung cancer, eye conditions, and more.
- **Efficient Report Management**: All medical records are stored in an organized manner, making it easy for patients to manage their health information.
- **Secure Communication**: Allows doctors and patients to communicate and share updates securely.

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Frontend**: Bootstrap
- **Machine Learning Models**: Skin cancer, lung cancer, eye problems

## Installation

To set up the application locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Rithish-Sripaul/solonLabs.git
   cd Solon-Labs
   ```

2. **Install dependencies**:
   Ensure you have Python and MySQL installed, then install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database**:

   - Create a new MySQL database for the project.
   - Configure the database credentials in the application (typically in a configuration file like `config.py`).

4. **Run the application**:
   To start the application:
   ```bash
   flask --app app run
   ```
   For debug mode:
   ```bash
   flask --app app run --debug
   ```

## Usage

1. **Patient Login and Uploads**:

   - Patients can log in and upload their test results and prescriptions for easy storage and sharing.

2. **Doctor Access and Updates**:

   - Doctors can log in, review patient records, and update details as required.
   - They can also utilize the integrated ML models to gain additional insights into patient conditions.

3. **ML Model Insights**:
   - The platform’s ML models are designed to detect conditions like skin cancer, lung cancer, and eye issues. This feature provides doctors with a preliminary assessment, helping in faster decision-making.

## Future Enhancements

- **Notification System**: Implementing notifications to alert patients and doctors of updates.
- **Multilingual Support**: Expanding the platform to support multiple languages.
- **Real-Time Chat**: Adding a real-time chat feature for patients and doctors.

## License

This project is licensed under the MIT License.
