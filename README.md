# 🏡🏠PROPERTY MANAGEMENT API 🏡🏠

---

> The Community Housing Property Management API provides endpoints to manage a rental property system, including: Creating, reading, updating, and deleting property managers, properties, support workers, tenancies, and tenants.
Linking tenants to tenancies and support workers (many-to-many relationships). Retrieving nested relational data efficiently using SQLAlchemy ORM and Marshmallow schemas. The API is designed using a modular structure, with separate files for models, schemas, controllers, and database commands.

## Table of Contents

- [Description](#description)
- [Background & Planning](#background--planning)
- [Features](#features)
- [Installation & Requirements](#installation-and-requirements)
- [Entity Relationship Diagram](#entity-relationship-diagram-erd)
- [Database](#database)
- [Seed Data](#seed-data)
- [API Endpoints](#api-endpoints)
- [API URL](#api-url)
- [Testing](#testing)
- [API Requests](#api-requests)
- [Project Structure](#project-structure)
- [Libraries & Licencing](#libraries--licencing)
- [Acknowledgments](#acknowledgments)
- [Author](#author)

## Description

A RESTful API built with Flask, SQLAlchemy, and Marshmallow for managing properties, tenants, tenancies, and support workers. This project demonstrates modular API design, relational database modeling, and best practices in Python web development.

## Background & Planning

The planning phase of this project had two requirements:

1. Choose an appropriate database system.
2. Design an Entity Relationship Diagram (ERD) to map the database tables.

For more details, see [Planning Documentation.](/Planning_Document.md)

## Features

- Full CRUD operations for all entities.
- Many-to-many relationship management:
    - Tenants ↔ Tenancies
    - Tenants ↔ Support Workers
- Nested schemas for relational queries:
    - Fetch tenants with their tenancies
    - Fetch property managers with properties
    - Fetch tenancies with properties and tenants
- Seed data for rapid testing.
- Configurable via .env and environment-specific configuration classes.

## Installation and requirements

### Requirements:

- Python 3.12 – Programming language used for the application.
- Flask – Lightweight web framework for building the API.
- Flask CLI – Provides command-line interface for database management and seeding commands.
- SQLAlchemy – Object-relational mapping (ORM) tool for database interactions.
- Marshmallow – Library for serialization and deserialization of database models.
- PostgreSQL – Relational database used for data storage.
- psycopg2-binary – PostgreSQL database adapter for Python.
- python-dotenv – Loads environment variables from .env file.
- gunicorn – Production WSGI server for running the Flask application.

### Installation:

1. Clone the repository:

```py
git clone https://github.com/yourusername/property_management_api_build.git
cd property_management_api_build
```

2. Create a virtual environment:

```py
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```py
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file based on `.env.example`:

```py
DATABASE_URL="postgresql+psycopg2://user:password@host:port/database_name"
FLASK_ENV="development"
```

5. Create the database:

- Connect to PostgreSQL

```py
sudo -u postgres psql
```

- Create the databse

```py
CREATE DATABASE property_management_db;
```

- Connect to the database

```py
\c property_management_db;
```

- Create the user role

```py
CREATE USER admin_pmdb WITH PASSWORD 'password';
```

- Grant the user required privileges

```py
GRANT ALL PRIVILEGES ON DATABASE property_management_db TO admin_pmdb;
```

- Grant the user access to the current/future schema

```py
GRANT ALL ON SCHEMA public TO admin_pmdb;
```

6. Manage the database:

- Create and seed the tables

```py
flask db drop
flask db create
flask db seed
```

- Reconnect to databse

```py
sudo -u admin_pmdb psql -d property_management_db -h localhost
```

- Lookup all databases

```py
\l
```

- Lookup all users

```py
\du
```

- Lookup tables in the current database

```py
\dt
```

- Lookup all all results within a table

```py
SELECT * FROM table_name;
```

7. Run the application:

```py
flask run
```

8. API will be available at `http://localhost:5000`.

## Entity Relationship Diagram (ERD)

![ERD](/Images/ERD_Final.png)

![ERD Relationship Table](/Images/Relationship_Table_Final.png)

## Database

| Table            | Relationships                                                   |
|-----------------|-----------------------------------------------------------------|
| PropertyManager  | One-to-many → Property                                           |
| Property         | One-to-many → Tenancy; Many-to-one → PropertyManager           |
| SupportWorker    | Many-to-many ↔ Tenant via TenantSupportWorker                  |
| Tenant           | Many-to-many ↔ Tenancy via TenantTenancy; Many-to-many ↔ SupportWorker |
| Tenancy          | Many-to-many ↔ Tenant via TenantTenancy; Many-to-one → Property |

## Seed Data

The database is pre-seeded using the flask db seed command:

- 3 x Property Managers
- 3 x Properties
- 3 x Support Workers
- 3 x Tenancies
- 3 x Tenants
- Tenant-Tenancy and Tenant-Support-Worker links

## API Endpoints

Note: 'id' refers to the id of the entity being accessed, unless specifically noted 'worker_id' etc.


### Property Managers

- **GET /property_managers/** – Retrieve all property managers  
- **GET /property_managers/id/** – Retrieve a single property manager  
- **GET /property_managers/properties/** – Retrieve property managers with their properties  
- **POST /property_managers/** – Create a new property manager  
- **PUT /property_managers/id/** – Update a property manager  
- **DELETE /property_managers/id/** – Delete a property manager  

### Properties

- **GET /properties/** – Retrieve all properties  
- **GET /properties/id/** – Retrieve a single property  
- **GET /properties/property_manager/** – Retrieve properties with their manager  
- **POST /properties/** – Create a property  
- **PUT /properties/id/** – Update a property  
- **DELETE /properties/id/** – Delete a property  

### Support Workers

- **GET /support_workers/** – Retrieve all support workers  
- **GET /support_workers/id/** – Retrieve a single support worker  
- **GET /support_workers/tenants/** – Retrieve support workers with tenants  
- **POST /support_workers/** – Create a support worker  
- **PUT /support_workers/id/** – Update a support worker  
- **DELETE /support_workers/id/** – Delete a support worker  

### Tenancies

- **GET /tenancies/** – Retrieve all tenancies  
- **GET /tenancies/id/** – Retrieve a single tenancy  
- **GET /tenancies/properties/** – Retrieve tenancies with properties  
- **GET /tenancies/tenants/** – Retrieve tenancies with tenants  
- **GET /tenancies/search?status=&start_date=&end_date=** – Filter tenancies  
- **POST /tenancies/** – Create a new tenancy  
- **PUT /tenancies/id/** – Update a tenancy  
- **DELETE /tenancies/id/** – Delete a tenancy  
- **POST /tenancies/id/link_tenant/tenant_id/** – Link tenant to tenancy  

### Tenants

- **GET /tenants/** – Retrieve all tenants  
- **GET /tenants/id/** – Retrieve a single tenant  
- **GET /tenants/tenancies/** – Retrieve tenants with tenancies  
- **GET /tenants/support_workers/** – Retrieve tenants with support workers  
- **POST /tenants/** – Create a new tenant  
- **PUT /tenants/id/** – Update a tenant  
- **DELETE /tenants/id/** – Delete a tenant  
- **POST /tenants/id/link_tenancy/tenancy_id/** – Link tenant to tenancy  
- **POST /tenants/id/link_support_worker/worker_id/** – Link tenant to support worker  

## API URL

The database for this project is hosted Neon, and the production version of the API is hosted on Render at the below url:

URL = 

## Testing

API can be tested via Postman or Insomnia [(below)](#api-requests).

Optional: implement unit tests with pytest.

## API Requests

API endpoints were tested via API requests in Insomnia. See example output below, or [example requests](/Images/Example_API_Requests/):

### GET


### POST


### PUT


### DELETE







## Project Structure

![Project Structure](Images/Project_Structure_1.png)
![Project Structure Con.](Images/Project_Structure_2.png)

## Libraries & Licencing

This project is licenced under an MIT Licence. For more information please see [Licence Document](/LICENSE).

## Acknowledgments

This project has been generated for the purpose of a Web Development assignment - all data has been generated for the purpose of this project, and does not identify any real renters, property managers, or properties.

Some idea generation, library/licence comparisons, and guidance on document structure were provided by ChatGPT (GPT-4o, OpenAI, 2025).

## Author

Developed by ✨BeeGeeEss✨

<https://github.com/beegeeess>
