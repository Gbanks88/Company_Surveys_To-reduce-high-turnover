#pragma once

#include <string>
#include <vector>
#include <memory>
#include <map>
#include "Requirement.hpp"

namespace Core {

class SystemVDocument {
public:
    enum class DocumentType {
        ConOps,        // Concept of Operations
        SyDD,         // System Design Document
        SSDD,         // Software System Design Document
        IDD,          // Interface Design Document
        SRS,          // Software Requirements Specification
        IRS,          // Interface Requirements Specification
        ATP,          // Acceptance Test Plan
        STP           // System Test Plan
    };

    SystemVDocument(DocumentType type, const std::string& name);
    ~SystemVDocument() = default;

    // Document management
    void setContent(const std::string& content);
    void addSection(const std::string& title, const std::string& content);
    void updateSection(const std::string& title, const std::string& content);
    
    // Requirements linkage
    void linkRequirement(const std::shared_ptr<Requirement>& req);
    void unlinkRequirement(const std::shared_ptr<Requirement>& req);
    std::vector<std::shared_ptr<Requirement>> getLinkedRequirements() const;

    // SysML integration
    void linkSysMLModel(const std::string& modelId);
    void unlinkSysMLModel(const std::string& modelId);
    std::vector<std::string> getLinkedSysMLModels() const;

    // Getters
    DocumentType getType() const { return type_; }
    std::string getName() const { return name_; }
    std::string getContent() const { return content_; }
    std::map<std::string, std::string> getSections() const { return sections_; }

    // Document validation
    bool validate() const;
    std::vector<std::string> getValidationErrors() const;

private:
    DocumentType type_;
    std::string name_;
    std::string content_;
    std::map<std::string, std::string> sections_;
    std::vector<std::shared_ptr<Requirement>> linkedRequirements_;
    std::vector<std::string> linkedSysMLModels_;
    std::vector<std::string> validationErrors_;
};

} // namespace Core
