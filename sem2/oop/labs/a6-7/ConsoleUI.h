#pragma once
#include "Service.h"
#include "FileBasket.h"

class ConsoleUI
{
private:
	Service& service;
	std::unique_ptr<FileBasket> fileBasket;

	void run_administrator();
	void run_user();

	//admin
	void add_trench_coat();
	void remove_trench_coat();
	void update_trench_coat();
	void display_all_trench_coats();


	//user
	void see_coats_of_given_size();
	void see_basket();
	void open_basket_file();


public:
	//constructor
	ConsoleUI(Service& service);
	void run();
};

