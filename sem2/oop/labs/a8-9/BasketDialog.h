#pragma once
#include <QDialog>
#include <QListWidget>
#include <QLabel>
#include "Service.h"

class BasketDialog : public QDialog
{
	Q_OBJECT

private:
	Service& service;
	QListWidget* basketList;
	QLabel* totalLabel;

	void buildUI();
	void refreshList();

public:
	explicit BasketDialog(Service& service, QWidget* parent = nullptr);

private slots:
	void saveOnCSV();
	void saveOnHTML();
};