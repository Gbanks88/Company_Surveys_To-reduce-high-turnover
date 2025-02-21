#include "gui/ProjectView.hpp"
#include <QVBoxLayout>
#include <QTreeView>
#include <QStandardItemModel>
#include <QHeaderView>

namespace reqdb {
namespace gui {

ProjectView::ProjectView(QWidget* parent)
    : QWidget(parent)
    , treeView_(new QTreeView(this))
    , model_(new QStandardItemModel(this)) {
    setupUi();
}

void ProjectView::setupUi() {
    auto* layout = new QVBoxLayout(this);
    
    // Configure tree view
    treeView_->setModel(model_);
    treeView_->header()->setSectionResizeMode(QHeaderView::ResizeToContents);
    treeView_->setSelectionMode(QAbstractItemView::SingleSelection);
    treeView_->setEditTriggers(QAbstractItemView::NoEditTriggers);
    
    // Set up model headers
    model_->setHorizontalHeaderLabels({
        tr("Name"),
        tr("Type"),
        tr("Status"),
        tr("Modified")
    });
    
    layout->addWidget(treeView_);
}

void ProjectView::setProject(const core::Project& project) {
    model_->clear();
    
    // Add root item for project
    auto* projectItem = new QStandardItem(QString::fromStdString(project.getTitle()));
    model_->appendRow(projectItem);
    
    // Add requirements folder
    auto* requirementsFolder = new QStandardItem(tr("Requirements"));
    projectItem->appendRow(requirementsFolder);
    
    // Add UML diagrams folder
    auto* umlFolder = new QStandardItem(tr("UML Diagrams"));
    projectItem->appendRow(umlFolder);
    
    // Expand project item
    treeView_->expand(model_->indexFromItem(projectItem));
}

void ProjectView::addRequirement(const core::Requirement& requirement) {
    // Find requirements folder
    auto items = model_->findItems(tr("Requirements"), Qt::MatchRecursive);
    if (items.isEmpty()) {
        return;
    }
    
    auto* folder = items.first();
    
    // Add requirement item
    QList<QStandardItem*> row;
    row << new QStandardItem(QString::fromStdString(requirement.getTitle()));
    row << new QStandardItem(tr("Requirement"));
    // TODO: Add status and modified date
    
    folder->appendRow(row);
}

void ProjectView::addUMLDiagram(const core::UMLDiagram& diagram) {
    // Find UML diagrams folder
    auto items = model_->findItems(tr("UML Diagrams"), Qt::MatchRecursive);
    if (items.isEmpty()) {
        return;
    }
    
    auto* folder = items.first();
    
    // Add diagram item
    QList<QStandardItem*> row;
    row << new QStandardItem(QString::fromStdString(diagram.getName()));
    row << new QStandardItem(tr("UML Diagram"));
    // TODO: Add type and modified date
    
    folder->appendRow(row);
}

} // namespace gui
} // namespace reqdb
