# Order Processing System

## Description
The Order Processing System is designed to streamline the management of customer orders, from placement to delivery. It automates the workflow, ensuring efficiency and accuracy throughout the order fulfillment process.

## Installation

To get the Order Processing System up and running, follow these steps:

1. Clone this Repo.

2. Ensure you have Python installed on your system. This project requires Python 3.6 or later.

3. Set up a virtual environment: python3 -m venv venv

4. Activate the virtual environment:
````
- On Windows: `venv\Scripts\activate`
- On Unix or MacOS: `source venv/bin/activate`
````
5. Install the required packages:

```
- pip install -r requirements.txt
```


## Environment Setup

Before running the application, you need to set up the following environment variables in a `.env` file at the root of your project:
````
STRIPE_TEST_PUBLISHABLE_KEY=your_stripe_test_publishable_key_here 
STRIPE_TEST_SECRET_KEY=your_stripe_test_secret_key_here 
DATABASE_URL=postgresql://username:password@localhost:5432/database_name 
APP_PASSWORD_Gmail=your_app_password_for_gmail_here 
SECRET_KEY=your_secret_key_here 
SECRET=your_secret_here
````

Flask run

`This will start the Flask server, and you should be able to access the application on `http://127.0.0.1:5000/`.`

## Docker Setup

My application is containerized for easy setup and deployment. You can pull the Docker image from Docker Hub and run the app on your local machine with the following commands:

1. Pull the Docker image:

    `docker pull nassermohamed3222/flask_order`


2. Run the Docker container:

    `docker run -d -p 5000:5000 --env-file .env nassermohamed3222/flask_order`


* Make sure you have Docker installed on your system.
* After running the container, the application should be accessible on `http://localhost:5000`.
* You should make sure postgres installed if not you can create postgres container using docker-compose file,
* Be certain to set your password, username and database correctly using:

    `docker compose up`

## Deployment and API Documentation

- **Website URL**: Order Processing System
- **API Documentation**: To understand how each endpoint works, visit http://54.234.104.100:5000/api/docs.
- **Admin Credentials**:
    - Email: `q@gmail.com`
    - Password: `123456`
- You can use admin credentials to add products as illustrated in docs.
