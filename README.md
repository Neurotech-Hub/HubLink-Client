# HubLink Client

This Python script retrieves S3 credentials from a specified URL and lists the first-level directories in an Amazon S3 bucket.

## Prerequisites

- Python 3.6 or higher
- [pip](https://pip.pypa.io/en/stable/installation/) installed

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine.

```bash
$ git clone <repository_url>
$ cd <repository_folder>
```

### 2. Create and Activate a Virtual Environment

It is recommended to create a Python virtual environment to manage dependencies.

```bash
# Create a virtual environment named 'venv'
$ python3 -m venv venv

# Activate the virtual environment
# On Windows
$ venv\Scripts\activate

# On macOS/Linux
$ source venv/bin/activate
```

### 3. Install the Required Packages

Install the required packages using `pip`:

```bash
$ pip install -r requirements.txt
```

### 4. Set Up the Environment Variables

Create a `.env` file in the project root directory and add the following:

```env
SECRET_URL=https://hublink.cloud/...
```

This URL contains the necessary credentials for accessing Amazon S3.

## Running the Script

To run the script, ensure your virtual environment is activated and execute the following command:

```bash
$ python client.py
```

The script will retrieve the S3 credentials and list the first-level directories in the specified bucket.

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:

```bash
$ deactivate
```

## License

This project is licensed under the MIT License.

