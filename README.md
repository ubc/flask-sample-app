# Flask Sample App with Tests

This is a simple Flask web application with unit tests. The application provides a basic REST API for managing a list of items. It serves as a starting point for learning how to create a Flask application and write tests for it.

## Project Structure

The project is organized as follows:

- `app/`: Contains the Flask application and routes.
- `tests/`: Houses unit tests for the application.
- `run.py`: A script to run the Flask application.

## Getting Started

To get the Flask app up and running on your local machine, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd flask_sample_app
   ```

2. **Set Up a Virtual Environment:**

   It's recommended to create a virtual environment to isolate project dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Install the necessary dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   Start the Flask application:

   ```bash
   python run.py
   ```

   The app will be available at [http://localhost:5000](http://localhost:5000).

5. **Run Tests:**

   To run the unit tests, execute the following command:

   ```bash
   python -m unittest discover tests
   ```

   This command will discover and run all tests in the `tests` directory.

## Application Routes

The application provides the following routes:

- `GET /`: Returns a simple greeting message.
- `GET /items`: Returns a list of items. Pass the optional `search` query parameter to filter by a partial, case-insensitive name.
- `GET /items/{item_id}`: Returns the details of a specific item.
- `POST /items`: Adds a new item to the list.

## Testing

Unit tests are provided in the `tests` directory. They cover the basic functionality of the application, including route handling and response validation. You can use these tests as a reference to write your own tests or to verify the correctness of the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribute

Feel free to contribute to this project by opening issues or submitting pull requests. We welcome any improvements, bug fixes, or additional features.

## Author

- Pan Luo

## Acknowledgments

- This project was created as a sample Flask application for educational purposes.
- Special thanks to the Flask community for providing a fantastic web framework.

Enjoy experimenting with the Flask sample app! If you have any questions or need further assistance, please don't hesitate to reach out.
