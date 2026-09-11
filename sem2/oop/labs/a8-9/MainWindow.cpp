#include "MainWindow.h"
#include "AdminWidget.h"
#include "UserWidget.h"

#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>

void MainWindow::showModeSelection()
{
    //show the main menu - choose between admin or user
    static bool built = false;
    if (!built)
    {
        built = true;

        auto* page = new QWidget();
        //use vertical layout for the text and buttons
        auto* layout = new QVBoxLayout(page);
        //allign on center and set spacing
        layout->setAlignment(Qt::AlignCenter);
        layout->setSpacing(20);


        //add text labels (informative)
        auto* title = new QLabel("Trench Coat Shop");
        QFont titleFont = title->font();
        titleFont.setPointSize(24);
        titleFont.setBold(true);
        title->setFont(titleFont);
        title->setAlignment(Qt::AlignCenter);

        auto* subtitle = new QLabel("Please select your mode:");
        subtitle->setAlignment(Qt::AlignCenter);

        //add 2 buttons, one for admin and one for user
        auto* adminBtn = new QPushButton("Administrator");
        auto* userBtn = new QPushButton("User");
        adminBtn->setFixedSize(200, 50);
        userBtn->setFixedSize(200, 50);


        //when the admin button is clicked, refresh the table and make sure to display page 1 (for admin)
        connect(adminBtn, &QPushButton::clicked, this, [this]() {
            adminWidget->refreshTable();
            stack->setCurrentIndex(1);
            });

        //when the user button is clicked, display page 2 (for the user)
        connect(userBtn, &QPushButton::clicked, this, [this]() {
            stack->setCurrentIndex(2);
            });


        //use stretch to make them look nice
        //then add all the widgets to the layout
        layout->addStretch();
        layout->addWidget(title);
        layout->addWidget(subtitle);
        layout->addWidget(adminBtn, 0, Qt::AlignCenter);
        layout->addWidget(userBtn, 0, Qt::AlignCenter);
        layout->addStretch();

        //put the menu at index 0 (the menu page)
        auto* old = stack->widget(0);
        stack->removeWidget(old);
        old->deleteLater();
        stack->insertWidget(0, page);
    }

    stack->setCurrentIndex(0);
}


MainWindow::MainWindow(Service& service, QWidget* parent)
    : QMainWindow(parent), service(service)
{
    setWindowTitle("Trench Coat Shop");
    resize(900, 600);

    stack = new QStackedWidget(this);
    setCentralWidget(stack);

    // page 0: main menu
    // page 1: admin
    // page 2: user

    adminWidget = new AdminWidget(service);
    userWidget = new UserWidget(service);

    // connect "Back" buttons to return to mode selection
    connect(adminWidget->findChild<QPushButton*>("backButton"), &QPushButton::clicked,
        this, &MainWindow::showModeSelection);
    connect(userWidget->findChild<QPushButton*>("backButton"), &QPushButton::clicked,
        this, &MainWindow::showModeSelection);

    stack->addWidget(new QWidget()); // index 0 — main menu   (when called for the first time, it's empty)
    stack->addWidget(adminWidget);   // index 1 - admin
    stack->addWidget(userWidget);    // index 2 - user

    showModeSelection();
}