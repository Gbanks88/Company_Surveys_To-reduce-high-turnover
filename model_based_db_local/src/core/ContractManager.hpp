#pragma once

#include <string>
#include <vector>
#include <memory>
#include <nlohmann/json.hpp>
#include <QObject>

namespace eco {
namespace core {

class Contract;
class ContractTemplate;
class ContractClause;

class ContractManager : public QObject {
    Q_OBJECT

public:
    static ContractManager& getInstance() {
        static ContractManager instance;
        return instance;
    }

    // Contract management
    std::shared_ptr<Contract> createContract(const std::string& name, 
                                           const std::string& type,
                                           const std::string& templateId = "");
    void deleteContract(const std::string& contractId);
    std::shared_ptr<Contract> getContract(const std::string& contractId);
    std::vector<std::shared_ptr<Contract>> getAllContracts() const;

    // Template management
    std::shared_ptr<ContractTemplate> createTemplate(const std::string& name,
                                                   const std::string& type);
    void deleteTemplate(const std::string& templateId);
    std::shared_ptr<ContractTemplate> getTemplate(const std::string& templateId);
    std::vector<std::shared_ptr<ContractTemplate>> getAllTemplates() const;

    // Document operations
    void exportContract(const std::string& contractId, 
                       const std::string& format,
                       const std::string& path);
    void importContract(const std::string& path);

signals:
    void contractCreated(const QString& contractId);
    void contractUpdated(const QString& contractId);
    void contractDeleted(const QString& contractId);
    void templateCreated(const QString& templateId);
    void templateUpdated(const QString& templateId);
    void templateDeleted(const QString& templateId);

private:
    ContractManager() = default;
    ~ContractManager() = default;
    ContractManager(const ContractManager&) = delete;
    ContractManager& operator=(const ContractManager&) = delete;

    std::vector<std::shared_ptr<Contract>> contracts_;
    std::vector<std::shared_ptr<ContractTemplate>> templates_;
};

class Contract {
public:
    Contract(const std::string& name, const std::string& type);

    // Basic properties
    std::string getId() const { return id_; }
    std::string getName() const { return name_; }
    std::string getType() const { return type_; }
    std::string getStatus() const { return status_; }

    // Content management
    void addClause(const ContractClause& clause);
    void removeClause(const std::string& clauseId);
    std::vector<ContractClause> getClauses() const;

    // Version control
    void createVersion();
    void revertToVersion(const std::string& versionId);
    std::vector<std::string> getVersionHistory() const;

    // Workflow
    void submit();
    void approve();
    void reject(const std::string& reason);
    void finalize();

    // Export
    nlohmann::json toJson() const;
    std::string toMarkdown() const;
    std::string toPdf() const;

private:
    std::string id_;
    std::string name_;
    std::string type_;
    std::string status_;
    std::vector<ContractClause> clauses_;
    std::vector<nlohmann::json> versionHistory_;
};

class ContractTemplate {
public:
    ContractTemplate(const std::string& name, const std::string& type);

    // Basic properties
    std::string getId() const { return id_; }
    std::string getName() const { return name_; }
    std::string getType() const { return type_; }

    // Template management
    void addClause(const ContractClause& clause);
    void removeClause(const std::string& clauseId);
    std::vector<ContractClause> getClauses() const;

    // Variables
    void addVariable(const std::string& name, const std::string& type);
    void removeVariable(const std::string& name);
    std::map<std::string, std::string> getVariables() const;

    // Export/Import
    nlohmann::json toJson() const;
    void fromJson(const nlohmann::json& json);

private:
    std::string id_;
    std::string name_;
    std::string type_;
    std::vector<ContractClause> clauses_;
    std::map<std::string, std::string> variables_;
};

class ContractClause {
public:
    ContractClause(const std::string& title, const std::string& content);

    // Properties
    std::string getId() const { return id_; }
    std::string getTitle() const { return title_; }
    std::string getContent() const { return content_; }

    // Variable handling
    void setVariable(const std::string& name, const std::string& value);
    std::string getVariable(const std::string& name) const;
    std::map<std::string, std::string> getAllVariables() const;

    // Export
    nlohmann::json toJson() const;
    std::string toMarkdown() const;

private:
    std::string id_;
    std::string title_;
    std::string content_;
    std::map<std::string, std::string> variables_;
};

} // namespace core
} // namespace eco
