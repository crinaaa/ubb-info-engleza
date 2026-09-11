#pragma once
#include <QDialog>
#include <QListWidget>
#include <QLabel>
#include "Service.h"

#include "BasketModel.h"
#include <QTableView>

class BasketDialog : public QDialog
{
	Q_OBJECT

private:
	Service& service;
	//QListWidget* basketList;
	QLabel* totalLabel;

	//added for this assignment
	QTableView* basketTableView; 
	BasketModel* basketModel;

	void buildUI();
	void refreshList();

public:
	explicit BasketDialog(Service& service, QWidget* parent = nullptr);

private slots:
	void saveOnCSV();
	void saveOnHTML();
};