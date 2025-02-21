# Model-Based Requirements Database

A comprehensive system for managing model-based development, UML diagrams, and requirements traceability.

## Features

- **Model Management**
  - Create and manage different types of models (domain, system, component)
  - Version control and status tracking
  - Hierarchical model organization
  - Metadata support

- **UML Diagram Support**
  - Class diagrams
  - Sequence diagrams
  - Component diagrams
  - State diagrams
  - Requirements diagrams
  - PlantUML integration
  - Graphviz support

- **Requirements Management**
  - Requirement creation and organization
  - Traceability matrix generation
  - Status tracking and history
  - Validation rules
  - Acceptance criteria
  - Metadata support

- **Integration Features**
  - RESTful API
  - Database persistence
  - UML generation
  - Requirements validation
  - Traceability analysis

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   # Create PostgreSQL database
   createdb modeldb
   
   # Set environment variables
   export DATABASE_URL="postgresql://user:password@localhost:5432/modeldb"
   ```

4. Initialize the database:
   ```python
   from src.database import DatabaseService
   
   db = DatabaseService("postgresql://user:password@localhost:5432/modeldb")
   db.create_database()
   ```

## Usage

1. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Creating a Model

```python
import requests

# Create a new model
model_data = {
    "name": "User Authentication",
    "description": "User authentication system model",
    "type": "system",
    "version": "1.0.0",
    "status": "draft",
    "metadata": {
        "author": "John Doe",
        "department": "Security"
    }
}

response = requests.post("http://localhost:8000/models/", json=model_data)
model = response.json()
```

### Adding a UML Diagram

```python
# Add a class diagram
class_diagram = {
    "name": "Authentication Classes",
    "classes": [
        {
            "name": "User",
            "attributes": [
                {"name": "id", "type": "UUID", "visibility": "private"},
                {"name": "username", "type": "str", "visibility": "private"}
            ],
            "methods": [
                {
                    "name": "authenticate",
                    "return_type": "bool",
                    "parameters": [
                        {"name": "password", "type": "str"}
                    ]
                }
            ]
        }
    ],
    "relationships": [
        {
            "from": "User",
            "to": "Role",
            "type": "association"
        }
    ]
}

response = requests.post(
    f"http://localhost:8000/models/{model['id']}/uml",
    json=class_diagram
)
```

### Managing Requirements

```python
# Create a requirement
requirement_data = {
    "name": "User Authentication",
    "description": "System must authenticate users securely",
    "type": "functional",
    "priority": "high",
    "status": "draft",
    "acceptance_criteria": "1. Users can log in with username/password\n2. Passwords are encrypted",
    "model_ids": [model['id']]
}

response = requests.post("http://localhost:8000/requirements/", json=requirement_data)
requirement = response.json()

# Get requirement trace
response = requests.get(f"http://localhost:8000/requirements/{requirement['id']}/trace")
trace = response.json()
```

## Project Structure

```
model_based_db/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database service
│   ├── uml_service.py    # UML generation service
│   └── requirements_service.py  # Requirements management
├── models/
│   ├── uml/             # Generated UML diagrams
│   └── requirements/    # Requirements artifacts
├── tests/              # Test files
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
