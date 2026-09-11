#include "UserWidget.h"
#include "BasketDialog.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QMessageBox>
#include <QFont>

UserWidget::UserWidget(Service& service, QWidget* parent) : QWidget(parent), service(service)
{
	buildUI();
}

void UserWidget::buildUI()
{
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(15);
    mainLayout->setContentsMargins(20, 20, 20, 20);

    //title
    auto* title = new QLabel("Browse Trench Coats");
    QFont f = title->font();
    f.setPointSize(16);
    f.setBold(true);
    title->setFont(f);
    title->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(title);

    //filtering row
    auto* filterGroup = new QGroupBox("Filter by Size");
    auto* filterLayout = new QHBoxLayout(filterGroup);

    sizeFilterEdit = new QLineEdit();
    sizeFilterEdit->setPlaceholderText("Enter size (leave empty for all)");
    filterButton = new QPushButton("Show Coats");

    filterLayout->addWidget(sizeFilterEdit);
    filterLayout->addWidget(filterButton);
    mainLayout->addWidget(filterGroup);

    connect(filterButton, &QPushButton::clicked, this, &UserWidget::onFilter);

    //coat display
    auto* coatGroup = new QGroupBox("Current Coat");
    auto* coatLayout = new QVBoxLayout(coatGroup);

    coatDisplayLabel = new QLabel("Press 'Show Coats' to start browsing.");
    coatDisplayLabel->setAlignment(Qt::AlignCenter);
    coatDisplayLabel->setWordWrap(true);
    QFont cf = coatDisplayLabel->font();
    cf.setPointSize(11);
    coatDisplayLabel->setFont(cf);
    coatDisplayLabel->setMinimumHeight(120);

    auto* navLayout = new QHBoxLayout();
    nextButton = new QPushButton("Next Coat");
    addToBasketButton = new QPushButton("Add to Basket");
    nextButton->setEnabled(false);
    addToBasketButton->setEnabled(false);

    navLayout->addWidget(nextButton);
    navLayout->addWidget(addToBasketButton);

    coatLayout->addWidget(coatDisplayLabel);
    coatLayout->addLayout(navLayout);
    mainLayout->addWidget(coatGroup);

    connect(nextButton, &QPushButton::clicked, this, &UserWidget::onNext);
    connect(addToBasketButton, &QPushButton::clicked, this, &UserWidget::onAddToBasket);


    //bottom buttons
    auto* bottomLayout = new QHBoxLayout();

    viewBasketButton = new QPushButton("View Basket");
    backButton = new QPushButton("Back to Menu");
    backButton->setObjectName("backButton"); // so MainWindow can find it

    bottomLayout->addWidget(viewBasketButton);
    bottomLayout->addStretch();
    bottomLayout->addWidget(backButton);
    mainLayout->addLayout(bottomLayout);

    connect(viewBasketButton, &QPushButton::clicked, this, &UserWidget::onViewBasket);

}

void UserWidget::onFilter()
{
	std::string size = sizeFilterEdit->text().toStdString();
	filteredCoats = service.get_coats_by_size(size);
	currentIndex = -1;

	if (filteredCoats.empty())
	{
		coatDisplayLabel->setText("No coats found!");
		nextButton->setEnabled(false);
		addToBasketButton->setEnabled(false);
		return;
	}

	//start ar first coat
	currentIndex = 0;
	displayCurrentCoat();
    nextButton->setEnabled(true);
    addToBasketButton->setEnabled(true);
}

void UserWidget::onNext()
{
	if (filteredCoats.empty())
	{
		return;
	}

	currentIndex = (currentIndex + 1) % static_cast<int>(filteredCoats.size());
	displayCurrentCoat();
}

void UserWidget::onAddToBasket()
{
    if (currentIndex < 0 || currentIndex >= static_cast<int>(filteredCoats.size()))
        return;

    try
    {
        service.add_to_basket(filteredCoats[currentIndex]);

        //in case quantity changed, fetch the data about the coats again
        std::string size = sizeFilterEdit->text().toStdString();
        filteredCoats = service.get_coats_by_size(size);

        //keep the index in the correct limits
        if (!filteredCoats.empty())
            currentIndex = currentIndex % static_cast<int>(filteredCoats.size());
        else
            currentIndex = -1;

        displayCurrentCoat();
        QMessageBox::information(this, "Basket", "Coat added to basket!");
    }
    catch (const std::exception& e)
    {
        QMessageBox::warning(this, "Error", e.what());
    }
}

void UserWidget::displayCurrentCoat()
{
	if (currentIndex < 0 || currentIndex >= static_cast<int>(filteredCoats.size()))
	{
		coatDisplayLabel->setText("No coats to display!");
		return;
	}

	const TrenchCoat& coat = filteredCoats[currentIndex];
	QString info = QString(
		"Size:      %1\n"
		"Colour:    %2\n"
		"Price:     %3\n"
		"Quantity:  %4\n"
	)
		.arg(QString::fromStdString(coat.get_size()))
		.arg(QString::fromStdString(coat.get_colour()))
		.arg(coat.get_price())
		.arg(coat.get_quantity());


	coatDisplayLabel->setText(info);

    QString link = QString::fromStdString(coat.get_photoLink());
    if (!link.isEmpty())
        QDesktopServices::openUrl(QUrl(link));
}

void UserWidget::onViewBasket()
{
    BasketDialog dialog(service, this);
    dialog.exec();
}