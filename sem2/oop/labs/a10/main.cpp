#include <QApplication>
#include "MainWindow.h"
#include "FileRepository.h"
#include "Service.h"

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    app.setStyleSheet(R"(
    QMainWindow, QWidget {
        background-color: #2d1b2e;
        color: #f0c0d8;
        font-family: Segoe UI;
        font-size: 13px;
    }
    QPushButton {
        background-color: #8b3a62;
        color: #f0c0d8;
        border: none;
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #a84d78;
    }
    QPushButton:pressed {
        background-color: #6b2a48;
    }
    QPushButton:disabled {
        background-color: #4a2a3a;
        color: #7a5a6a;
    }
    QLineEdit {
        background-color: #3d2040;
        color: #f0c0d8;
        border: 2px solid #8b3a62;
        border-radius: 10px;
        padding: 4px 10px;
    }
    QLineEdit:focus {
        border: 2px solid #c06090;
    }
    QTableWidget {
        background-color: #251525;
        color: #f0c0d8;
        gridline-color: #5a2a4a;
        border: 1px solid #8b3a62;
        border-radius: 8px;
    }
    QTableWidget::item:selected {
        background-color: #8b3a62;
        color: #f0c0d8;
    }
    QHeaderView::section {
        background-color: #3d2040;
        color: #f0c0d8;
        font-weight: bold;
        border: none;
        padding: 6px;
    }
    QGroupBox {
        border: 2px solid #8b3a62;
        border-radius: 10px;
        margin-top: 8px;
        color: #c06090;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
    }
    QListWidget {
        background-color: #251525;
        color: #f0c0d8;
        border: 1px solid #8b3a62;
        border-radius: 8px;
    }
    QListWidget::item:selected {
        background-color: #8b3a62;
        color: #f0c0d8;
    }
    QScrollBar:vertical {
        background: #3d2040;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #8b3a62;
        border-radius: 4px;
    }
)");

    FileRepository repo;  
    Service service(repo);

    MainWindow window(service);
    window.show();

    return app.exec();
}
