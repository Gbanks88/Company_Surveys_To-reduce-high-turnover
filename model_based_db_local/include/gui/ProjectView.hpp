#pragma once

#include "core/Project.hpp"
#include "core/Requirement.hpp"
#include "core/UMLDiagram.hpp"
#include <QWidget>

class QTreeView;
class QStandardItemModel;

namespace reqdb {
namespace gui {

class ProjectView : public QWidget {
    Q_OBJECT

public:
    explicit ProjectView(QWidget* parent = nullptr);

    void setProject(const core::Project& project);
    void addRequirement(const core::Requirement& requirement);
    void addUMLDiagram(const core::UMLDiagram& diagram);

private:
    void setupUi();

    QTreeView* treeView_;
    QStandardItemModel* model_;
};

} // namespace gui
} // namespace reqdb
