# Quick Start Guide

## 1. First Time Setup

```bash
# Install prerequisites (macOS)
brew install cmake conan qt@6 sqlite3 openssl

# Clone and build
git clone <repository-url>
cd model_based_db_local
./scripts/build.sh
```

## 2. Running the Application

### GUI Mode (Default)
```bash
./build/bin/reqdb_app
```

### Server Mode
```bash
./build/bin/reqdb_app --server-only
```

## 3. Quick Development Workflow

1. Make changes to code
2. Rebuild:
```bash
./scripts/build.sh
```
3. Run tests:
```bash
cd build && ctest
```

## 4. Common Tasks

### Adding a New Requirement
1. Open the application
2. Click "New Requirement" button
3. Fill in the form
4. Click "Save"

### Viewing Requirements
1. Use the Project View tree on the left
2. Filter using the search bar
3. Double-click to edit

### Using the API
```bash
# List all requirements
curl http://localhost:8080/api/v1/requirements

# Create new requirement
curl -X POST http://localhost:8080/api/v1/requirements \
  -H "Content-Type: application/json" \
  -d '{"title": "New Feature", "description": "Description"}'
```

## 5. Getting Help

- Full documentation in `docs/`
- Developer guide in `docs/dev/DEVELOPER_GUIDE.md`
- API documentation in `docs/api/README.md`
- Implementation details in `IMPLEMENTATION_REPORT.md`

## 6. Troubleshooting

### Build Issues
```bash
# Clean build
rm -rf build/*
./scripts/build.sh
```

### Runtime Issues
```bash
# Check logs
tail -f logs/reqdb.log

# Run with debug logging
SPDLOG_LEVEL=debug ./build/bin/reqdb_app
```
