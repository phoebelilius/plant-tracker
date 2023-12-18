Certainly! Here's an updated version of the README.md file with instructions for spinning up the Docker container and setting environment variables for MongoDB connection details:

```markdown
# Plant Tracker CLI App

A command-line interface (CLI) application for tracking plants using Python and MongoDB.

## Features

- Add, edit, delete, and water plants with specified attributes.
- View a list of all plants and their details.
- Utilizes MongoDB for data storage.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/plant-tracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd plant-tracker
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root and set the following environment variables for MongoDB connection:

```dotenv
MONGODB_HOSTNAME=host.docker.internal
MONGODB_PORT=27017
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_DATABASE=your_database
```

Replace `your_username`, `your_password`, `your_database` with your MongoDB credentials. If your MongoDB server is running on a different host or port, adjust `MONGODB_HOSTNAME` and `MONGODB_PORT` accordingly.

## Usage with Docker

Build the Docker image:

```bash
docker build -t plant-tracker .
```

Run the Docker container with environment variables for MongoDB connection:

```bash
docker run -it --rm \
  -e MONGODB_HOSTNAME=$MONGODB_HOSTNAME \
  -e MONGODB_PORT=$MONGODB_PORT \
  -e MONGODB_USERNAME=$MONGODB_USERNAME \
  -e MONGODB_PASSWORD=$MONGODB_PASSWORD \
  -e MONGODB_DATABASE=$MONGODB_DATABASE \
  plant-tracker
```

Replace `$MONGODB_HOSTNAME`, `$MONGODB_PORT`, `$MONGODB_USERNAME`, `$MONGODB_PASSWORD`, and `$MONGODB_DATABASE` with the actual values from your `.env` file.
Or use:
```bash
docker run -it --rm --env-file .env plant-tracker
```
## Usage

Run the application using the following command:

```bash
python plant_tracker/main.py <command>
```

Replace `<command>` with one of the available commands:

- `add`: Add a new plant.
- `edit`: Edit an existing plant.
- `delete`: Delete a plant.
- `show`: Show a list of all plants.
- `water`: Water a plant.

### Examples

#### Add a new plant:

```bash
python plant_tracker/main.py add
```

#### Show all plants:

```bash
python plant_tracker/main.py show
```

#### Water a plant:

```bash
python plant_tracker/main.py water
```

## Running Tests

To run tests, use the following command:

```bash
python -m unittest tests.test_main
```

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

These instructions now include guidance on configuring environment variables for MongoDB connection details and spinning up the Docker container with these variables. Adjust the values as needed for your specific MongoDB setup.