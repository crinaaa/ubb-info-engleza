#pragma once
#include "Service.h"

class ConsoleUI
{
private:
	Service& service;
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

	void filter_user_coats_by_length();

public:
	//constructor
	ConsoleUI(Service& service);
	void run();
};

