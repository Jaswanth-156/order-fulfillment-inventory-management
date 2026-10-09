\# Order Fulfillment and Inventory Management Platform



A REST API built with \*\*FastAPI, Python, PostgreSQL, SQLAlchemy, and Alembic\*\* to manage products, warehouses, inventory, orders, returns, and fulfillment operations.



\## Features



\- JWT authentication and refresh-token management

\- Role-based access control for Admin, Warehouse Manager, Fulfillment Agent, and Customer

\- Product and category management

\- Warehouse and warehouse-user management

\- Inventory tracking, adjustments, reservations, and transfers

\- Order creation, assignment, status tracking, and cancellation

\- Returns management

\- Notifications and audit logs

\- Idempotency support for preventing duplicate order requests

\- Dashboard and reporting endpoints

\- PostgreSQL database migrations using Alembic

\- Automated tests using Pytest

\- Docker and Docker Compose support



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Backend programming |

| FastAPI | REST API framework |

| PostgreSQL | Relational database |

| SQLAlchemy | ORM and database access |

| Alembic | Database migrations |

| Pydantic | Data validation and settings |

| Pytest | Automated testing |

| Docker Compose | Containerized application and database |



\## Project Structure



```text

Order\_Fulfillment\_and\_Inventory\_Management\_Platform/

├── app/

│   ├── core/

│   ├── db/

│   ├── models/

│   ├── routers/

│   ├── schemas/

│   └── main.py

├── alembic/

│   └── versions/

├── tests/

├── docs/

│   └── diagrams/

│       ├── er-diagram.png

│       └── architecture.png

├── .env.example

├── .gitignore

├── Dockerfile

├── docker-compose.yml

├── postman\_collection.json

├── requirements.txt

└── README.md

```



\*Adjust the structure above if any directory names differ from your actual project.\*



\## Prerequisites



\- Python 3.12

\- PostgreSQL, if running without Docker

\- Docker Desktop and Docker Compose, if running with Docker



\## Environment Configuration



Create a local `.env` file using `.env.example` as a template.



Configure the following variables:



```dotenv

DATABASE\_URL=your\_database\_connection\_url

SECRET\_KEY=your\_secret\_key

ALGORITHM=HS256

ACCESS\_TOKEN\_EXPIRE\_MINUTES=30

REFRESH\_TOKEN\_EXPIRE\_DAYS=7

POSTGRES\_PASSWORD=your\_database\_password

POSTGRES\_PASSWORD\_URLENCODED=your\_url\_encoded\_database\_password

```



Use new secret values for your own environment. Never commit `.env` or real credentials to GitHub.



\## Run with Docker



Start Docker Desktop, then run:



```bash

docker compose up --build -d

```



Apply database migrations:



```bash

docker compose exec web alembic upgrade head

```



Check container status:



```bash

docker compose ps

```



Stop the containers:



```bash

docker compose down

```



The PostgreSQL data volume is preserved when using the command above. Do not use `-v` unless you intentionally want to remove the volume.



\## Run Locally



Create and activate a virtual environment, then install dependencies.



Windows:



```cmd

py -m venv .venv

.venv\\Scripts\\activate

py -m pip install -r requirements.txt

```



Create a PostgreSQL database and configure your local `DATABASE\_URL` in `.env`.



Apply migrations:



```cmd

py -m alembic upgrade head

```



Start the API:



```cmd

py -m uvicorn app.main:app --reload

```



\## API Documentation



When the application is running, open:



\- Swagger UI: `http://localhost:8000/docs`

\- ReDoc: `http://localhost:8000/redoc`

\- OpenAPI JSON: `http://localhost:8000/openapi.json`



Available endpoints depend on the routers registered in the application.



\## Automated Testing



Run the test suite:



```cmd

py -m pytest -v

```



The most recently reported test result was \*\*45 passed, 1 deprecation warning\*\*.



\## Postman Collection



Import `postman\_collection.json` into Postman.



Set `base\_url` to:



```text

http://localhost:8000

```



Authenticate first and supply a valid access token for protected requests. Verify request paths, payloads, and response formats against Swagger UI before using the collection.



\## Database Design



The database uses SQLAlchemy models and Alembic migrations to manage schema changes.



\### Entity Relationship Diagram



!\[Entity Relationship Diagram](docs/diagrams/er-diagram.png)



\### System Architecture



!\[System Architecture](docs/diagrams/architecture.png)



\## Database Migration Commands



Create a new migration after changing models:



```cmd

py -m alembic revision --autogenerate -m "describe your change"

```



Apply migrations:



```cmd

py -m alembic upgrade head

```



Review generated migration scripts before applying them. Do not edit an already-applied migration without considering existing databases.



\## Security Notes



\- Passwords must be stored as hashes.

\- Protected endpoints require appropriate authentication and authorization.

\- Keep secrets in environment variables.

\- Exclude `.env`, virtual environments, caches, and other local files from Git.

\- Use HTTPS and appropriate production settings when deploying publicly.



\## Future Improvements



Potential improvements include CI/CD automation, structured logging, metrics, rate limiting, and additional integration and concurrency tests.



\## License



Add the license required by your project or assignment before distributing the repository.



