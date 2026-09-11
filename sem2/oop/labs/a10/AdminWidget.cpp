#include "AdminWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QGroupBox>
#include <QHeaderView>
#include <QMessageBox>
#include <QLabel>
#include "UserWidget.h"

#include <QShortcut>
#include <QKeySequence>

AdminWidget::AdminWidget(Service& service, QWidget* parent) : QWidget(parent), service(service)
{
    buildUI();
}

void AdminWidget::refreshTable()
{
    auto& coats = service.get_all_coats();
    table->setRowCount(static_cast<int>(coats.size()));

    for (int i = 0; i < static_cast<int>(coats.size()); ++i)
    {
        const auto& c = coats[i];
        table->setItem(i, 0, new QTableWidgetItem(QString::fromStdString(c.get_size())));
        table->setItem(i, 1, new QTableWidgetItem(QString::fromStdString(c.get_colour())));
        table->setItem(i, 2, new QTableWidgetItem(QString::fromStdString(c.get_photoLink())));
        table->setItem(i, 3, new QTableWidgetItem(QString::number(c.get_price())));
        table->setItem(i, 4, new QTableWidgetItem(QString::number(c.get_quantity())));
    }
}

void AdminWidget::buildUI()
{
    //combine everything 
    //show on the screen

    auto* mainLayout = new QHBoxLayout(this);

    //left side -> table
    auto* leftLayout = new QVBoxLayout();

    auto* tableLabel = new QLabel("All Trench Coats");
    QFont f = tableLabel->font();
    f.setBold(true);
    f.setPointSize(12);
    tableLabel->setFont(f);

    table = new QTableWidget();
    table->setColumnCount(5);
    table->setHorizontalHeaderLabels({ "Size", "Colour", "Photo Link", "Price", "Quantity" });
    table->setMinimumWidth(500);
    table->setColumnWidth(2, 150);

    //when i click, populate the table with the info from the text file
    connect(table, &QTableWidget::itemSelectionChanged,
        this, &AdminWidget::populateFormFromSelection);

    leftLayout->addWidget(tableLabel);
    leftLayout->addWidget(table);

    

    //rigth side -> buttons + form to add the data
    auto* rightLayout = new QVBoxLayout();

    auto* formBox = new QGroupBox("Coat Details");
    auto* formLayout = new QFormLayout(formBox);

    sizeEdit = new QLineEdit();
    colourEdit = new QLineEdit();
    linkEdit = new QLineEdit();
    priceEdit = new QLineEdit();
    quantityEdit = new QLineEdit();

    formLayout->addRow("Size (XS/S/M/L/XL/XXL):", sizeEdit);
    formLayout->addRow("Colour:", colourEdit);
    formLayout->addRow("Photo Link:", linkEdit);
    formLayout->addRow("Price:", priceEdit);
    formLayout->addRow("Quantity:", quantityEdit);

    addButton = new QPushButton("Add");
    removeButton = new QPushButton("Remove");
    updateButton = new QPushButton("Update");

    backButton = new QPushButton("Back to Menu");
    backButton->setObjectName("backButton"); 

    connect(addButton, &QPushButton::clicked, this, &AdminWidget::onAdd);
    connect(removeButton, &QPushButton::clicked, this, &AdminWidget::onRemove);
    connect(updateButton, &QPushButton::clicked, this, &AdminWidget::onUpdate);

    auto* btnLayout = new QVBoxLayout();
    btnLayout->addWidget(addButton);
    btnLayout->addWidget(removeButton);
    btnLayout->addWidget(updateButton);



    //added for the last assignment
    undoButton = new QPushButton("Undo");
    redoButton = new QPushButton("Redo");
    btnLayout->addWidget(undoButton);
    btnLayout->addWidget(redoButton);

    connect(undoButton, &QPushButton::clicked, this, &AdminWidget::onUndo);
    connect(redoButton, &QPushButton::clicked, this, &AdminWidget::onRedo);

    // key combinations (ctrl+z and ctrl+y)
    auto* undoShortcut = new QShortcut(QKeySequence(Qt::CTRL | Qt::Key_Z), this);
    auto* redoShortcut = new QShortcut(QKeySequence(Qt::CTRL | Qt::Key_Y), this);

    connect(undoShortcut, &QShortcut::activated, this, &AdminWidget::onUndo);
    connect(redoShortcut, &QShortcut::activated, this, &AdminWidget::onRedo);





    //added now
    auto* sortGroup = new QGroupBox("Sorting Options");
    auto* sortLayout = new QVBoxLayout(sortGroup);

    ascendingRadio = new QRadioButton("Ascending");
    descendingRadio = new QRadioButton("Descending");

    sortButton = new QPushButton("Apply Sort");

    sortLayout->addWidget(ascendingRadio);
    sortLayout->addWidget(descendingRadio);
    sortLayout->addWidget(sortButton);

    rightLayout->addWidget(sortGroup);

    connect(sortButton, &QPushButton::clicked, this, &AdminWidget::onSort);





    btnLayout->addStretch();
    btnLayout->addWidget(backButton);

    rightLayout->addWidget(formBox);
    rightLayout->addLayout(btnLayout);

    mainLayout->addLayout(leftLayout, 3);
    mainLayout->addLayout(rightLayout, 1);

}


//when a coat from the table is clicked, put the informatio in the form
void AdminWidget::populateFormFromSelection()
{
    auto selected = table->selectedItems();
    if (selected.empty())
        return;

    int row = table->currentRow();
    sizeEdit->setText(table->item(row, 0)->text());
    colourEdit->setText(table->item(row, 1)->text());
    linkEdit->setText(table->item(row, 2)->text());
    priceEdit->setText(table->item(row, 3)->text());
    quantityEdit->setText(table->item(row, 4)->text());
}


//clear all form inputs
void AdminWidget::clearForm()
{
    sizeEdit->clear();
    colourEdit->clear();
    linkEdit->clear();
    priceEdit->clear();
    quantityEdit->clear();
}

void AdminWidget::onAdd()
{
    bool priceOk, quantityOk;
    double price = priceEdit->text().toDouble(&priceOk);
    int quantity = quantityEdit->text().toInt(&quantityOk);

    if (!priceOk || !quantityOk)
    {
        QMessageBox::warning(this, "Input Error", "Price must be a double and quantity an integer!");
        return;
    }

    try
    {
        service.add(sizeEdit->text().toStdString(),
            colourEdit->text().toStdString(),
            linkEdit->text().toStdString(),
            price, quantity);

        refreshTable();
        clearForm();
        QMessageBox::information(this, "Success", "Coat added successfully!");
    }
    catch (const std::exception& e)
    {
        QMessageBox::warning(this, "Error", e.what());
    }
}

void AdminWidget::onRemove()
{
    if (sizeEdit->text().isEmpty() || colourEdit->text().isEmpty())
    {
        QMessageBox::warning(this, "Input error", "Size and colour cannot be empty!");
        return;
    }
    try
    {
        service.remove(sizeEdit->text().toStdString(), colourEdit->text().toStdString());
        refreshTable();
        clearForm();
        QMessageBox::information(this, "Success!", "Coat removed successfully!");
    }
    catch (const std::exception& e)
    {
        QMessageBox::warning(this, "Error", e.what());
    }
}

void AdminWidget::onUpdate()
{
    bool priceOk, quantityOk;
    double price = priceEdit->text().toDouble(&priceOk);
    int quantity = quantityEdit->text().toInt(&quantityOk);

    if (!priceOk || !quantityOk)
    {
        QMessageBox::warning(this, "Input error", "Price must be a double and quantity an integer!");
        return;
    }

    if (sizeEdit->text().isEmpty() || colourEdit->text().isEmpty())
    {
        QMessageBox::warning(this, "Input error", "Size and colour cannot be empty!");
        return;
    }

    try
    {
        service.update(sizeEdit->text().toStdString(),
            colourEdit->text().toStdString(),
            linkEdit->text().toStdString(),
            price, quantity);

        refreshTable();
        clearForm();
        QMessageBox::information(this, "Success", "Coat updated successfully!");
    }
    catch (const std::exception& e)
    {
        QMessageBox::warning(this, "Error", e.what());
    }
}

void AdminWidget::onSort()
{
    bool isAscending = ascendingRadio->isChecked();
    service.sortByColour(isAscending);
    refreshTable();
}



//added for the last assignment
void AdminWidget::onUndo()
{
    try {
        service.undo();
        refreshTable();
        clearForm();
    }
    catch (const std::exception& e) {
        QMessageBox::information(this, "Undo", e.what());
    }
}

void AdminWidget::onRedo()
{
    try {
        service.redo();
        refreshTable();
        clearForm();
    }
    catch (const std::exception& e) {
        QMessageBox::information(this, "Redo", e.what());
    }
}