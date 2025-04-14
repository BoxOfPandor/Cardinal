# Cardinal

Cardinal is a flexible and extensible API developed in Python with FastAPI, allowing dynamic addition, modification, or deletion of API endpoints through a module system.

## 🌟 Vision

Create a modular API in continuous development where you only need to add Python files to automatically extend functionality, without service interruption or modification of existing code.

## 🔑 Key Features

- **Modular architecture**: Easy addition of new functionalities via independent modules
- **Automatic discovery**: The core automatically detects and integrates new modules
- **Continuous development**: Add APIs infinitely without touching existing code
- **Auto-generated documentation**: Automatically generated Swagger interface for all modules
- **Module isolation**: Each module can evolve independently

## 🏗️ Architecture

Cardinal consists of two main components:

### Core
The application kernel that provides:
- Automatic module detection and loading
- Request routing to appropriate modules
- Centralized error handling and logging
- Global configuration

### Modules
Independent components that:
- Register automatically with the core
- Define their own API endpoints
- Implement their specific business logic
- Can be added/modified/deleted on the fly

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/username/cardinal.git
cd cardinal

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ✨ Creating a New Module

1. Create a new folder in `modules/` (e.g., `modules/my_module/`)
2. Add the necessary files:
   - `__init__.py` - For auto-discovery
   - `routes.py` - To define your endpoints
   - `models.py` - For Pydantic data models
   - `services.py` - For business logic

Example module structure:
```python
# modules/my_module/__init__.py
from .routes import router  # For module_loader to find the router

# modules/my_module/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-module", tags=["My Module"])

@router.get("/")
async def read_root():
    return {"message": "Hello from my module!"}
```

The core will automatically detect your module and add its routes to the API!

## 🧪 Tests

```bash
# Run tests
pytest
```

## 📘 Documentation

Complete documentation is automatically generated and accessible at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔄 Continuous Development

Cardinal is designed for continuous development:
- Add new modules at any time
- Modify existing modules
- The core takes care of integrating them without requiring restart

## 📄 License

This project is licensed under the [MIT](LICENSE) license