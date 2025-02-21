#pragma once

#include <string>
#include <vector>
#include <memory>
#include <map>
#include "Requirement.hpp"
#include "SystemVDocument.hpp"

namespace Core {

class SysMLIntegration {
public:
    enum class DiagramType {
        Block,
        Internal_Block,
        Package,
        Requirements,
        Parametric,
        Activity,
        Sequence,
        State_Machine,
        Use_Case
    };

    SysMLIntegration();
    ~SysMLIntegration() = default;

    // Model management
    bool createModel(const std::string& name, const std::string& description);
    bool importModel(const std::string& filePath);
    bool exportModel(const std::string& modelId, const std::string& filePath);

    // Diagram operations
    std::string createDiagram(DiagramType type, const std::string& name);
    bool updateDiagram(const std::string& diagramId, const std::string& content);
    bool deleteDiagram(const std::string& diagramId);

    // Requirements integration
    void linkRequirementToDiagram(const std::string& diagramId, 
                                const std::shared_ptr<Requirement>& req);
    void unlinkRequirementFromDiagram(const std::string& diagramId, 
                                    const std::shared_ptr<Requirement>& req);

    // Document integration
    void linkDocumentToDiagram(const std::string& diagramId, 
                             const std::shared_ptr<SystemVDocument>& doc);
    void unlinkDocumentFromDiagram(const std::string& diagramId, 
                                 const std::shared_ptr<SystemVDocument>& doc);

    // Traceability
    std::vector<std::string> getRelatedDiagrams(const std::shared_ptr<Requirement>& req) const;
    std::vector<std::shared_ptr<Requirement>> getDiagramRequirements(const std::string& diagramId) const;
    std::vector<std::shared_ptr<SystemVDocument>> getDiagramDocuments(const std::string& diagramId) const;

    // Model validation
    bool validateModel(const std::string& modelId);
    std::vector<std::string> getValidationErrors(const std::string& modelId) const;

private:
    std::map<std::string, std::string> models_;  // modelId -> content
    std::map<std::string, DiagramType> diagrams_;  // diagramId -> type
    std::map<std::string, std::vector<std::shared_ptr<Requirement>>> diagramRequirements_;
    std::map<std::string, std::vector<std::shared_ptr<SystemVDocument>>> diagramDocuments_;
    std::map<std::string, std::vector<std::string>> validationErrors_;  // modelId -> errors
};

} // namespace Core
