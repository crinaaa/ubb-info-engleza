#pragma once
#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QComboBox>
#include <QListWidget>
#include <QGroupBox>
#include "Service.h"
#include "FileBasket.h"
#include <QDesktopServices>
#include <QUrl>


class UserWidget : public QWidget
{
	Q_OBJECT
private:
	Service& service;
	//filtered coat list
	std::vector<TrenchCoat> filteredCoats;
	int currentIndex = -1;


	//filtering
	QLineEdit* sizeFilterEdit;
	QPushButton* filterButton;

	//coat display one by one
	QLabel* coatDisplayLabel;
	QPushButton* nextButton;
	QPushButton* addToBasketButton;

	//basket actions
	QPushButton* viewBasketButton;
	QPushButton* backButton;


	void buildUI();
	void displayCurrentCoat();

public:
	explicit UserWidget(Service& service, QWidget* parent = nullptr);

private slots:
	void onFilter();
	void onNext();
	void onAddToBasket();
	void onViewBasket();
};