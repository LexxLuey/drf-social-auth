# Django Rest Framework API Setup Guide

This guide provides step-by-step instructions to set up the Django Rest Framework API project locally. 

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Docker Setup](#docker-setup)

## Prerequisites
Since there are two ways you can setup this project, this section is divided into two for the local (non docker) setup and docker setup.

### Local Setup Prerequisites
Before you begin, make sure you have the following installed:

- Python (3.10 or later)
- Poetry or pip (Python package manager)
- PostgreSQL
- Redis
- (Optional) Google OAuth Client Key ([https://console.cloud.google.com/](https://console.cloud.google.com/))
- (Optional) Apple Developer Account and keys ([https://docs.allauth.org/en/latest/socialaccount/providers/apple.html](https://docs.allauth.org/en/latest/socialaccount/providers/apple.html))


### Docker Setup Prerequisites
Before you begin, make sure you have the following installed:

- Docker
- Docker-Compose
- (Optional) Google OAuth Client Key ([https://console.cloud.google.com/](https://console.cloud.google.com/))
- (Optional) Apple Developer Account and keys ([https://docs.allauth.org/en/latest/socialaccount/providers/apple.html](https://docs.allauth.org/en/latest/socialaccount/providers/apple.html))

## Local Setup (Using a command line terminal)

1. Clone the project.
```bash
git clone https://github.com/LexxLuey/drf-social-auth/
```

2. Enter the cloned projects directory
```bash
cd drf-social-auth
```

3. Create a virtual environment, activate it and install dependencies using either pip or poetry:

```bash title="using pip"
python3 -m venv venv
source venv/bin/activate  
# On Windows: 
# venv\Scripts\activate

pip install -r requirements.dev.txt
```

```bash title="using poetry"
poetry install
poetry shell
```

4. Create a PostgreSQL database

5. Create .env file with variables like the ones in the .env.sample file.

6. Get a Google OAuth keys for your app.

7. Get an Apple OAuth keys for your app.

8. Update the .env file with your database credentials, google and apple oauth keys.


9. Apply migrations:

```bash

python manage.py migrate
```

10. Run the Django development server:

```bash

python manage.py runserver
```

11. Access the Django API at [8000](http://localhost:8000)

### Running Tests

12. (OPTIONAL) Run tests by doing:
```bash
python manage.py test cinema.test
```
### Starting Celery workers

13. Start the worker using the following command in a new terminal.
```bash
celery -A core worker -l info
```

14. Start the beat by running the following command in a new terminal 
```bash
celery -A core beat -l info
```

NOTE: Please update the `id_token` and `access_tokens` with actual values gotten from google oauth playground and apple oauth playground appropriately whenever testing accounts app.


## Docker Setup 

This repository contains a Django web application configured to run with Docker using Docker Compose. It includes services for Django, PostgreSQL, Redis, Celery worker, and Celery beat.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

## Setup

1. Clone this repository:

```bash
git clone https://github.com/LexxLuey/drf-social-auth/
cd drf-social-auth
```

2. Create a `.env` file in the project root directory and add your environment variables:

```bash
DEBUG=1
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
```

3. If it is your **FIRST** time of running this app, **DO THIS** otherwise you can skip to next step: 

```bash
docker-compose up db # Wait until you see 'database system is ready to accept connections'
docker-compose up redis # Wait until you see 'Ready to accept connections'
docker-compose up
```
run each command in a separate terminal.

4. Get docker containers up and running: 

```bash
docker-compose up
```

5. Access the application at `http://localhost:8000`.

### Running Commands

You can run Django management commands and Celery tasks using Docker Compose.

#### Django Management Commands

To run Django management commands, use the `docker-compose exec` command. For example, to create migrations:

```bash
docker-compose exec web python manage.py makemigrations
```

### API Tests

To run tests, use the `docker-compose exec` command as well. For example, to start testing the cinema app:

```bash
docker-compose exec web python manage.py test cinema.tests
```


---

# Q & A

## 1 - How would you design and implement content-based and collaborative filtering recommendation algorithms? What databases would you use for efficient storage and querying of user preferences and movie metadata?

To implement collaborative filtering in Python, you first need a dataset containing user-item interactions. These interactions could be explicit, such as ratings, or implicit, like views or time spent on an item. Typically, this data is organized in a matrix format, with users represented in rows, items in columns, and the interactions as the matrix entries. Since this matrix is often sparse, meaning most entries are empty due to users not interacting with most items, efficient storage and handling are crucial.

For storage and querying of user preferences and movie metadata, several databases can be used:

1. **MongoDB or PostgreSQL for Metadata**: MongoDB is suitable for flexible schema design, while PostgreSQL offers robust relational database features, suitable if metadata has a more structured format. Personally, I prefer structured databases and would go with Postgres.

2. **Graph Database for Relationships**: Neo4j can be useful if you need to represent relationships between entities such as actors, directors, and movies in a graph format.

3. **Key-Value Stores for User Preferences**: Redis or Apache Cassandra are efficient for storing user preferences as key-value pairs, especially when dealing with large volumes of data.

4. **Data Warehouses for Analytics**: Amazon Redshift, Google BigQuery, or Snowflake are useful for performing analytics on large datasets, such as identifying trends in user preferences or evaluating recommendation algorithms' performance.

5. **Distributed File Systems for Large-Scale Data Storage**: Hadoop Distributed File System (HDFS) or Apache HBase are suitable for storing and processing large volumes of data, especially for user interactions or metadata.

To implement collaborative filtering algorithms, you need to follow these steps:

1. **Find Similar Users or Items**: Determine which users or items are similar based on their interactions. This can be done using similarity metrics such as cosine similarity or Pearson correlation coefficient.

2. **Predict Ratings for Unseen Items**: Once similar users or items are identified, predict ratings for items that the user has not interacted with. This can be done using techniques like k-nearest neighbors (k-NN) or matrix factorization.

3. **Evaluate Accuracy**: Measure the accuracy of the predictions using metrics like Root Mean Square Error (RMSE) or Mean Absolute Error (MAE) to assess the performance of the recommendation system.

By using Python libraries such as Surprise, which provides implementations of various collaborative filtering algorithms and evaluation metrics, you can easily build and analyze recommendation systems. Libraries like Surprise simplify tasks such as loading data, configuring algorithms, and evaluating performance, making it easier to experiment with different approaches and optimize the recommendation system for accuracy and efficiency.

## 2 - How would you optimize database performance for a social networking platform using Postgres, Neo4j, and Qdrant for structured, graph-based, and similarity search data?

To optimize database performance for a social networking platform utilizing Postgres, Neo4j, and Qdrant for structured, graph-based, and similarity search data, I'd adopt several strategies tailored to each database type:

**For Postgres (Structured Data):**

1. **Schema Optimization:** Ensure the database schema is well-designed, normalized, and indexed appropriately. This includes minimizing redundant data, choosing appropriate data types, and creating indexes on frequently queried columns.

2. **Query Optimization:** Analyze and optimize frequently executed queries by using query plans, indexing, and query rewriting techniques. I'd focus on optimizing complex joins, aggregations, and subqueries to improve query performance.

3. **Connection Pooling:** Implement connection pooling to efficiently manage database connections and reduce overhead associated with establishing and tearing down connections frequently.

4. **Partitioning:** Utilize table partitioning to horizontally split large tables into smaller, more manageable chunks based on certain criteria such as date ranges or user IDs. This helps improve query performance and maintenance tasks like data archiving.

5. **Regular Maintenance:** Perform routine maintenance tasks such as vacuuming, analyzing, and reindexing to optimize database performance and prevent issues like table bloat and index fragmentation.

**For Neo4j (Graph-Based Data):**

1. **Indexing:** Create indexes on properties that are frequently used for node and relationship lookups to speed up graph traversal and pattern matching queries.

2. **Cypher Query Optimization:** Craft efficient Cypher queries by leveraging Neo4j's query planner, profiling, and query hints. I'd focus on minimizing the number of traversal steps, reducing redundant operations, and optimizing filter conditions.

3. **Schema Design:** Design an appropriate node and relationship schema that reflects the domain model and query patterns. This includes defining node labels, relationship types, and property keys to ensure efficient data access and traversal.

4. **Cache Configuration:** Configure Neo4j's caching settings to optimize memory usage and minimize disk I/O. Tuning cache sizes, eviction policies, and cache concurrency can significantly improve query performance, especially for frequently accessed data.

5. **Cluster Configuration:** Utilize Neo4j's clustering features to distribute the graph database across multiple servers for horizontal scalability and fault tolerance. Properly configuring clustering settings, replication factors, and load balancing ensures optimal performance under varying workloads.

**For Qdrant (Similarity Search Data):**

1. **Vector Indexing:** Utilize Qdrant's vector indexing capabilities to efficiently store and query high-dimensional vector data, such as embeddings representing user profiles or content features.

2. **Index Configuration:** Configure index settings such as dimensionality, distance metrics, and indexing methods based on the specific requirements of similarity search queries. Choosing the appropriate indexing parameters can significantly impact search performance.

3. **Batch Insertion:** Optimize data ingestion by using batch insertion techniques to efficiently index large volumes of vector data into Qdrant. This involves batching similar vectors together for more efficient indexing and reducing the overhead of individual insertions.

4. **Query Optimization:** Craft queries that leverage Qdrant's efficient search algorithms, such as approximate nearest neighbor (ANN) search, to quickly retrieve relevant vectors based on similarity criteria. I'd focus on tuning query parameters such as search radius and accuracy thresholds to balance search speed and result quality.

5. **Scale-Out Architecture:** Design a scalable architecture for Qdrant by deploying it in a distributed manner across multiple nodes or clusters. This allows for horizontal scalability and improved query throughput by distributing indexing and query processing tasks across multiple resources.

By implementing these optimization strategies tailored to each database type, I can ensure that the social networking platform operates efficiently and delivers optimal performance for structured, graph-based, and similarity search data.

## 3 - Describe using Celery for asynchronous task processing in a Django application, ensuring reliability and fault tolerance, especially for tasks that may fail or need to be retried.

Using Celery for asynchronous task processing in my Django application ensures that tasks like sending daily email notifications to users by a given time are handled reliably and with fault tolerance. Here's how I'd set it up to ensure reliability and fault tolerance:

1. **Task Definition:** I'd define a Celery task for sending email notifications. This task would contain the logic for fetching the list of users who need to receive notifications and sending emails to each user.

2. **Error Handling:** To handle potential errors during task execution, I'd implement error handling within the task itself. This could include catching exceptions and logging error messages to aid in debugging.

3. **Retries:** For tasks that may fail or encounter transient errors, I'd configure Celery to automatically retry the task a certain number of times with a delay between retries. This ensures that if a task fails initially, it has a chance to succeed on subsequent retries.

4. **Backoff Strategy:** To prevent overwhelming the system in case of persistent failures, I'd implement a backoff strategy where the delay between retries increases exponentially with each retry attempt. This helps alleviate load on the system and gives it time to recover from transient issues.

5. **Dead Letter Queue (DLQ):** In scenarios where a task consistently fails after multiple retries, I'd configure Celery to move the task to a Dead Letter Queue (DLQ) or a separate error queue. This allows me to manually inspect and handle failed tasks, such as investigating the root cause of the failure or taking corrective actions.

6. **Monitoring and Alerting:** I'd set up monitoring and alerting mechanisms to notify me of any failures or issues with Celery tasks. This could involve integrating Celery with monitoring tools like Prometheus or Sentry to track task execution metrics and receive alerts for abnormal behavior.

By following these steps, I can ensure that asynchronous tasks in my Django application, such as sending daily email notifications, are processed reliably and with fault tolerance. Celery's robust features for error handling, retries, and monitoring help me maintain the integrity and performance of my application's background task processing system.

---

# TODO

- Make docker image of app slimmer by reducing number of layers
- Integrate authentication into cinema app
- Image and File storage to third party service such s3, cloudinary etc
