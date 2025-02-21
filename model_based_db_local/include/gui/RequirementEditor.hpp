#pragma once

#include "core/Requirement.hpp"
#include <QWidget>

class QLineEdit;
class QTextEdit;
class QComboBox;

namespace reqdb {
namespace gui {

class RequirementEditor : public QWidget {
    Q_OBJECT

public:
    explicit RequirementEditor(QWidget* parent = nullptr);

    void setRequirement(const core::Requirement& requirement);
    core::Requirement getRequirement() const;

signals:
    void requirementSaved();
    void editingCanceled();

private slots:
    void save();
    void cancel();

private:
    void setupUi();

    QLineEdit* titleEdit_;
    QTextEdit* descriptionEdit_;
    QComboBox* statusCombo_;
    QComboBox* priorityCombo_;
    QLineEdit* assigneeEdit_;
};

} // namespace gui
} // namespace reqdb
