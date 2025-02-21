#include "gui/DiagramEditor.hpp"
#include <QVBoxLayout>
#include <QToolBar>
#include <QGraphicsScene>
#include <QGraphicsView>

namespace reqdb {
namespace gui {

DiagramEditor::DiagramEditor(QWidget* parent)
    : QWidget(parent)
    , scene_(new QGraphicsScene(this))
    , view_(new QGraphicsView(scene_, this)) {
    setupUi();
}

void DiagramEditor::setupUi() {
    auto* layout = new QVBoxLayout(this);
    
    // Create toolbar
    auto* toolbar = new QToolBar(this);
    toolbar->addAction(tr("Select"), this, &DiagramEditor::selectMode);
    toolbar->addAction(tr("Class"), this, &DiagramEditor::addClass);
    toolbar->addAction(tr("Association"), this, &DiagramEditor::addAssociation);
    toolbar->addAction(tr("Inheritance"), this, &DiagramEditor::addInheritance);
    layout->addWidget(toolbar);
    
    // Add graphics view
    layout->addWidget(view_);
    
    // Configure view
    view_->setRenderHint(QPainter::Antialiasing);
    view_->setViewportUpdateMode(QGraphicsView::FullViewportUpdate);
    view_->setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
    view_->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
    view_->setDragMode(QGraphicsView::RubberBandDrag);
}

void DiagramEditor::selectMode() {
    // TODO: Implement select mode
}

void DiagramEditor::addClass() {
    // TODO: Implement add class
}

void DiagramEditor::addAssociation() {
    // TODO: Implement add association
}

void DiagramEditor::addInheritance() {
    // TODO: Implement add inheritance
}

} // namespace gui
} // namespace reqdb
