#include "BasketDialog.h"
#include "CSV_Basket.h"
#include "HTML_Basket.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QGroupBox>
#include <QMessageBox>
#include <QFont>

#include <QHeaderView>

void BasketDialog::refreshList()
{

	basketModel->setBasket(service.get_basket());

	/*basketList->clear();

	auto basket = service.get_basket();
	for (const auto& coat : basket)
	{
		QString entry = QString("%1 | %2 | %3")
			.arg(QString::fromStdString(coat.get_size()))
			.arg(QString::fromStdString(coat.get_colour()))
			.arg(coat.get_price());

		basketList->addItem(entry);
	}*/

	totalLabel->setText(QString("Total: €%1").arg(service.get_total_price()));
}

void BasketDialog::buildUI()
{
	auto* mainLayout = new QVBoxLayout(this);

	//basket list
	auto* listGroup = new QGroupBox("Items in basket");
	auto* listLayout = new QVBoxLayout(listGroup);

	//basketList = new QListWidget();
	//listLayout->addWidget(basketList);
	//mainLayout->addWidget(listGroup);


	//added for this assignment
	basketTableView = new QTableView(this);
	basketTableView->setModel(basketModel);

	basketTableView->horizontalHeader()->setVisible(true);
	basketTableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

	//add the view to the existing layer
	listLayout->addWidget(basketTableView);
	mainLayout->addWidget(listGroup);

	

	//show the total price
	totalLabel = new QLabel("Total: 0");
	QFont f = totalLabel->font();
	f.setBold(true);
	f.setPointSize(12);
	totalLabel->setFont(f);
	mainLayout->addWidget(totalLabel);

	//buttons for saving to file
	auto* saveGroup = new QGroupBox("Save & Open Basket As");
	auto* saveLayout = new QHBoxLayout(saveGroup);

	auto* csvButton = new QPushButton("Save as CSV");
	auto* htmlButton = new QPushButton("Save as HTML");

	saveLayout->addWidget(csvButton);
	saveLayout->addWidget(htmlButton);
	mainLayout->addWidget(saveGroup);

	connect(csvButton, &QPushButton::clicked, this, &BasketDialog::saveOnCSV);
	connect(htmlButton, &QPushButton::clicked, this, &BasketDialog::saveOnHTML);


	//button to close
	auto* closeButton = new QPushButton("Close");
	connect(closeButton, &QPushButton::clicked, this, &QDialog::accept);
	mainLayout->addWidget(closeButton);
}

BasketDialog::BasketDialog(Service& service, QWidget* parent) : QDialog(parent), service(service)
{
	setWindowTitle("My Basket");
	setMinimumSize(400, 350);

	//added now
	basketModel = new BasketModel(this);

	buildUI();
	refreshList();
}


void BasketDialog::saveOnCSV()
{
	try
	{
		CSV_Basket basket;
		service.file_basket(basket);
		//basket.display();

		QMessageBox::information(this, "Saved", "Basket saved to CSV file and opened!");
	}
	catch (const std::exception& e)
	{
		QMessageBox::warning(this, "Error", e.what());
	}
}

void BasketDialog::saveOnHTML()
{
	try
	{
		HTML_Basket basket;
		service.file_basket(basket);
		//basket.display();

		QMessageBox::information(this, "Saved", "Basket saved to HTML file and opened!");
	}
	catch (const std::exception& e)
	{
		QMessageBox::warning(this, "Error", e.what());
	}
}