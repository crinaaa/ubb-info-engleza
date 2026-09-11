#pragma once
#include <QWidget>
#include <QTableWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <qradiobutton.h>
#include "Service.h"

class AdminWidget : public QWidget
{
	Q_OBJECT

public:
	AdminWidget(Service& service, QWidget* parent = nullptr);

	//reload the table from the service
	void refreshTable();


private slots:
	void onAdd();
	void onRemove();
	void onUpdate();


	//added now
	void onSort();

private:
	Service& service;

	//table
	QTableWidget* table;

	//form inputs
	QLineEdit* sizeEdit;
	QLineEdit* colourEdit;
	QLineEdit* linkEdit;
	QLineEdit* priceEdit;
	QLineEdit* quantityEdit;

	//buttons
	QPushButton* addButton;
	QPushButton* removeButton;
	QPushButton* updateButton;
	QPushButton* backButton;

	//added now
	QPushButton* sortButton;

	void buildUI();
	void populateFormFromSelection();

	void clearForm();


	//radio buttons
	QRadioButton* ascendingRadio;
	QRadioButton* descendingRadio;
};