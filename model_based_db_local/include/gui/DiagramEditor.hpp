#pragma once

#include <QWidget>

class QGraphicsScene;
class QGraphicsView;

namespace reqdb {
namespace gui {

class DiagramEditor : public QWidget {
    Q_OBJECT

public:
    explicit DiagramEditor(QWidget* parent = nullptr);

private slots:
    void selectMode();
    void addClass();
    void addAssociation();
    void addInheritance();

private:
    void setupUi();

    QGraphicsScene* scene_;
    QGraphicsView* view_;
};

} // namespace gui
} // namespace reqdb
