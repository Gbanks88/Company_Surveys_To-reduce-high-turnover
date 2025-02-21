#pragma once

#include "db/DatabaseManager.hpp"
#include <string>

namespace reqdb {
namespace api {

// Simple HTTP request/response classes
class Request {
public:
    std::string getBody() const { return body_; }
    void setBody(const std::string& body) { body_ = body; }
private:
    std::string body_;
};

class Response {
public:
    void setStatus(int status) { status_ = status; }
    void setBody(const std::string& body) { body_ = body; }
private:
    int status_;
    std::string body_;
};

class APIHandlers {
public:
    explicit APIHandlers(db::DatabaseManager& dbManager);

    void handleGetRequirements(const Request& req, Response& res);
    void handleCreateRequirement(const Request& req, Response& res);
    void handleGetUMLDiagrams(const Request& req, Response& res);
    void handleCreateUMLDiagram(const Request& req, Response& res);

private:
    db::DatabaseManager& dbManager_;
};

} // namespace api
} // namespace reqdb
