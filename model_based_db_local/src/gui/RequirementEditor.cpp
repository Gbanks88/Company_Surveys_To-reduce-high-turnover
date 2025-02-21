#include "gui/RequirementEditor.hpp"
#include <QVBoxLayout>
#include <QFormLayout>
#include <QLineEdit>
#include <QTextEdit>
#include <QComboBox>
#include <QPushButton>
#include <QLabel>

namespace reqdb {
namespace gui {

RequirementEditor::RequirementEditor(QWidget* parent)
    : QWidget(parent) {
    setupUi();
}

void RequirementEditor::setupUi() {
    auto* mainLayout = new QVBoxLayout(this);
    
    // Form layout for requirement fields
    auto* formLayout = new QFormLayout;
    
    // Title
    titleEdit_ = new QLineEdit(this);
    formLayout->addRow(tr("Title:"), titleEdit_);
    
    // Description
    descriptionEdit_ = new QTextEdit(this);
    formLayout->addRow(tr("Description:"), descriptionEdit_);
    
    // Status
    statusCombo_ = new QComboBox(this);
    statusCombo_->addItems({
        tr("Draft"),
        tr("In Review"),
        tr("Approved"),
        tr("Implemented"),
        tr("Verified"),
        tr("Rejected")
    });
    formLayout->addRow(tr("Status:"), statusCombo_);
    
    // Priority
    priorityCombo_ = new QComboBox(this);
    priorityCombo_->addItems({
        tr("Low"),
        tr("Medium"),
        tr("High"),
        tr("Critical")
    });
    formLayout->addRow(tr("Priority:"), priorityCombo_);
    
    // Assignee
    assigneeEdit_ = new QLineEdit(this);
    formLayout->addRow(tr("Assignee:"), assigneeEdit_);
    
    mainLayout->addLayout(formLayout);
    
    // Buttons
    auto* buttonLayout = new QHBoxLayout;
    
    auto* saveButton = new QPushButton(tr("Save"), this);
    connect(saveButton, &QPushButton::clicked, this, &RequirementEditor::save);
    
    auto* cancelButton = new QPushButton(tr("Cancel"), this);
    connect(cancelButton, &QPushButton::clicked, this, &RequirementEditor::cancel);
    
    buttonLayout->addWidget(saveButton);
    buttonLayout->addWidget(cancelButton);
    
    mainLayout->addLayout(buttonLayout);
}

void RequirementEditor::save() {
    // TODO: Implement save functionality
    emit requirementSaved();
}

void RequirementEditor::cancel() {
    // TODO: Implement cancel functionality
    emit editingCanceled();
}

void RequirementEditor::setRequirement(const core::Requirement& requirement) {
    titleEdit_->setText(QString::fromStdString(requirement.getTitle()));
    descriptionEdit_->setText(QString::fromStdString(requirement.getDescription()));
    // TODO: Set other fields
}

core::Requirement RequirementEditor::getRequirement() const {
    core::Requirement requirement;
    requirement.setTitle(titleEdit_->text().toStdString());
    requirement.setDescription(descriptionEdit_->toPlainText().toStdString());
    // TODO: Get other fields
    return requirement;
}

} // namespace gui
} // namespace reqdb
