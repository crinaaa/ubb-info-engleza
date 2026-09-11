#pragma once
#include <QMainWindow>
#include <QStackedWidget>
#include "Service.h"

class AdminWidget;
class UserWidget;

class MainWindow : public QMainWindow
{
	Q_OBJECT;

private:
	Service& service;
	QStackedWidget* stack;
	AdminWidget* adminWidget;
	UserWidget* userWidget;

	/*QWidget* buildMenuPage();*/
	void showModeSelection();

public:
	explicit MainWindow(Service& service, QWidget* parent = nullptr);
};