# Developer Guide: Requirements Management System

## 1. Development Environment Setup

### 1.1 Prerequisites
```bash
# macOS (using Homebrew)
brew install cmake
brew install conan
brew install qt@6
brew install sqlite3
brew install openssl

# Add Qt to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="/opt/homebrew/opt/qt@6/bin:$PATH"
```

### 1.2 Clone and Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd model_based_db_local

# Install dependencies and build
./scripts/build.sh
```

## 2. Running the Application

### 2.1 GUI Mode
```bash
# From project root
./build/bin/reqdb_app
```

### 2.2 Server Mode
```bash
# From project root
./build/bin/reqdb_app --server-only
```

### 2.3 Development Mode
```bash
# Run with debug logging
SPDLOG_LEVEL=debug ./build/bin/reqdb_app

# Run with specific database file
./build/bin/reqdb_app --db-path=./dev.db
```

## 3. Making Changes

### 3.1 Adding a New Requirement Field

1. Update the Requirement class header:
```cpp
// include/core/Requirement.hpp
class Requirement {
    // Add new field
    std::string category_;
    
public:
    // Add getter/setter
    void setCategory(const std::string& category);
    std::string getCategory() const;
};
```

2. Implement in source file:
```cpp
// src/core/Requirement.cpp
void Requirement::setCategory(const std::string& category) {
    category_ = category;
}

std::string Requirement::getCategory() const {
    return category_;
}
```

3. Update database schema:
```cpp
// src/db/DatabaseManager.cpp
const char* CREATE_REQUIREMENTS_TABLE = R"(
    ALTER TABLE requirements 
    ADD COLUMN category TEXT;
)";
```

4. Update repository:
```cpp
// src/db/RequirementRepository.cpp
bool RequirementRepository::createRequirement(const core::Requirement& req) {
    const char* sql = R"(
        INSERT INTO requirements 
        (title, description, category) 
        VALUES (?, ?, ?);
    )";
    // Bind parameters...
}
```

5. Update GUI:
```cpp
// src/gui/RequirementEditor.cpp
void RequirementEditor::setupUi() {
    categoryComboBox_ = new QComboBox(this);
    layout_->addRow("Category:", categoryComboBox_);
}
```

### 3.2 Adding a New API Endpoint

1. Define handler:
```cpp
// include/api/APIHandlers.hpp
class APIHandlers {
public:
    void handleCategoryStats(http::request<>& req, http::response<>& res);
};
```

2. Implement handler:
```cpp
// src/api/APIHandlers.cpp
void APIHandlers::handleCategoryStats(http::request<>& req, http::response<>& res) {
    auto stats = requirementRepo_->getCategoryStats();
    res.body() = nlohmann::json(stats).dump();
    res.prepare_payload();
}
```

3. Register endpoint:
```cpp
// src/api/RESTServer.cpp
void RESTServer::setupRoutes() {
    router_.GET("/api/v1/stats/categories", 
        std::bind(&APIHandlers::handleCategoryStats, 
        &handlers_, std::placeholders::_1, std::placeholders::_2));
}
```

### 3.3 Adding a New Test

```cpp
// tests/core/requirement_test.cpp
TEST(RequirementTest, CategoryManagement) {
    Requirement req;
    req.setCategory("Security");
    EXPECT_EQ(req.getCategory(), "Security");
}
```

## 4. Common Development Tasks

### 4.1 Database Migration
1. Create migration file:
```cpp
// src/db/migrations/002_add_category.cpp
bool Migration002::up() {
    const char* sql = "ALTER TABLE requirements ADD COLUMN category TEXT;";
    return db_->execute(sql);
}
```

2. Register migration:
```cpp
// src/db/DatabaseManager.cpp
void DatabaseManager::registerMigrations() {
    migrations_.push_back(std::make_unique<Migration002>());
}
```

### 4.2 Adding a New Feature

1. Create feature branch:
```bash
git checkout -b feature/requirement-categories
```

2. Implement changes following TDD:
   - Write failing test
   - Implement feature
   - Make test pass
   - Refactor

3. Update documentation:
   - Add new API endpoints to docs/api/README.md
   - Update user manual in docs/user/README.md
   - Update implementation report

4. Submit PR:
   - Ensure all tests pass
   - Update CHANGELOG.md
   - Request review

### 4.3 Debugging

1. Enable debug logging:
```cpp
spdlog::set_level(spdlog::level::debug);
spdlog::debug("Processing requirement: {}", req.getId());
```

2. Use Qt Debug Tools:
```cpp
// Set environment variable
QT_DEBUG_PLUGINS=1

// Use qDebug
qDebug() << "Widget state:" << widget->state();
```

3. Database debugging:
```cpp
// Enable SQLite debug
sqlite3_trace(db_, [](void*, const char* sql) {
    spdlog::debug("SQL: {}", sql);
}, nullptr);
```

## 5. Build System

### 5.1 Adding New Source Files

1. Update CMakeLists.txt:
```cmake
# src/CMakeLists.txt
target_sources(reqdb_core PRIVATE
    core/NewFeature.cpp
)
```

2. Update include directories:
```cmake
target_include_directories(reqdb_core PUBLIC
    ${CMAKE_SOURCE_DIR}/include/new_feature
)
```

### 5.2 Adding New Dependencies

1. Update conanfile.txt:
```txt
[requires]
new_package/1.0.0
```

2. Update CMakeLists.txt:
```cmake
find_package(new_package REQUIRED)
target_link_libraries(reqdb_core PRIVATE new_package::new_package)
```

### 5.3 Building Different Configurations

```bash
# Debug build
cmake -DCMAKE_BUILD_TYPE=Debug ..

# Release build
cmake -DCMAKE_BUILD_TYPE=Release ..

# With sanitizers
cmake -DENABLE_SANITIZER=ON ..
```

## 6. Troubleshooting

### 6.1 Common Issues

1. Build Failures:
```bash
# Clean build
rm -rf build/*
./scripts/build.sh

# Update dependencies
conan remove -f '*'
./scripts/build.sh
```

2. Runtime Issues:
```bash
# Check logs
tail -f logs/reqdb.log

# Check database
sqlite3 requirements.db ".tables"
sqlite3 requirements.db "SELECT * FROM requirements;"
```

3. GUI Issues:
```bash
# Reset Qt settings
rm ~/Library/Preferences/com.reqdb.app.plist
```

### 6.2 Getting Help

1. Check logs:
```bash
cat logs/reqdb.log
```

2. Enable verbose mode:
```bash
REQDB_VERBOSE=1 ./build/bin/reqdb_app
```

3. Generate debug info:
```bash
./scripts/collect-debug-info.sh
```

## 7. Best Practices

1. Code Style
- Follow existing formatting
- Use clang-format
- Document public APIs
- Write meaningful commit messages

2. Testing
- Write unit tests for new features
- Update integration tests
- Run full test suite before committing

3. Performance
- Profile code changes
- Monitor memory usage
- Test with large datasets

4. Security
- Validate all inputs
- Use prepared statements
- Follow OWASP guidelines
- Regular security audits
