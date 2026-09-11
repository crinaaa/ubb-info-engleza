#include "ConsoleUI.h"
#include <iostream>
#include <stdexcept>
#include <limits>
#include <cctype>
#include <algorithm>
#include <windows.h>
#undef max

ConsoleUI::ConsoleUI(Service& service) : service(service) {}

//helper functions for reading input and displaying output
int read_integer(const std::string& prompt)
{
	int value;
	while (true)
	{
		std::cout << prompt;
		std::cin >> value;
		if (std::cin.good())
			return value;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
		std::cout << "Invalid number. Please enter a valid integer." << std::endl;
	}
}

double read_double(const std::string& prompt)
{
	double value;
	while (true)
	{
		std::cout << prompt;
		std::cin >> value;
		if (std::cin.good())
			return value;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
		std::cout << "Invalid number. Please enter a valid double." << std::endl;
	}
}

std::string read_string(const std::string& prompt)
{
	std::string value;
	std::cout << prompt;
	std::cin >> value;
	return value;
}

std::string read_size_or_empty(const std::string& prompt)
{
	while (true)
	{
		std::string value;
		std::cout << prompt;
		std::getline(std::cin, value);
		if (value.empty())
			return value;
		std::string upper = value;
		std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
		if (upper == "XS" || upper == "S" || upper == "M" ||
			upper == "L" || upper == "XL" || upper == "XXL")
			return upper;
		std::cout << "Invalid size. Allowed values: XS, S, M, L, XL, XXL, or press Enter for all.\n";
	}
}

std::string read_size(const std::string& prompt)
{
	while (true)
	{
		std::string value = read_size_or_empty(prompt);
		if (!value.empty())
			return value;
		std::cout << "Size cannot be empty. Allowed values: XS, S, M, L, XL, XXL.\n";
	}
}

static std::string read_colour(const std::string& prompt) {
	while (true) {
		std::cout << prompt;
		std::string value;
		std::cin >> value;
		// must contain only letters
		bool valid = !value.empty();
		for (char c : value)
			if (!std::isalpha(c)) { valid = false; break; }
		if (valid)
			return value;
		std::cout << "Invalid colour. Please enter letters only (no numbers or symbols).\n";
	}
}

void ConsoleUI::run()
{
	int choice = -1;
	while (choice)
	{
		std::cout << "Welcome to the Trench Coat Management System!" << std::endl;
		std::cout << "Please select your role:" << std::endl;
		std::cout << "1. Administrator" << std::endl;
		std::cout << "2. User" << std::endl;
		std::cout << "0. Exit" << std::endl;

		choice = read_integer("Enter your choice: ");
		if (choice == 1)
			run_administrator();
		else if (choice == 2)
			run_user();
		else if (choice == 0)
			std::cout << "Goodbye!" << std::endl;
		else
			std::cout << "Invalid choice. Please try again." << std::endl;
	}
}

void ConsoleUI::run_administrator()
{
	int choice = -1;

	while (true)
	{
		std::cout << "Administrator mode selected." << std::endl;
		std::cout << "Please select an operation:" << std::endl;
		std::cout << "1. Add a new trench coat" << std::endl;
		std::cout << "2. Remove a trench coat" << std::endl;
		std::cout << "3. Update a trench coat" << std::endl;
		std::cout << "4. Display all trench coats" << std::endl;
		std::cout << "0. Back to main menu" << std::endl;

		choice = read_integer("Enter your choice: ");

		if (choice == 1)
			add_trench_coat();
		else if (choice == 2)
			remove_trench_coat();
		else if (choice == 3)
			update_trench_coat();
		else if (choice == 4)
			display_all_trench_coats();
		else if (choice == 0)
			return;
		else
			std::cout << "Invalid choice." << std::endl;
	}
}

void ConsoleUI::run_user()
{
	int choice = -1;
	while (true)
	{
		std::cout << "User mode selected.\n";
		std::cout << "Please select an operation: \n";
		std::cout << "1. See all coats of a given size.\n";
		std::cout << "2. See the shopping basket and the total price of the items.\n";
		std::cout << "3. Filtering by length.\n";
		std::cout << "0. Exit.\n";

		choice = read_integer("Enter your choice: ");

		if (choice == 1)
			see_coats_of_given_size();
		else if (choice == 2)
			see_basket();
		else if (choice == 3)
			filter_user_coats_by_length();
		else if (choice == 0)
			return;
		else
			std::cout << "Invalid command!";
	}
}

void ConsoleUI::add_trench_coat()
{
	std::string size = read_size("Enter the size: ");
	std::string colour = read_colour("Enter the colour: ");
	std::string photoLink = read_string("Enter the photo link: ");
	double price = read_double("Enter the price: ");
	int quantity = read_integer("Enter the quantity: ");
	
	try
	{
		service.add(size, colour, photoLink, price, quantity);
		std::cout << "Coat added successfully!";
	}
	catch (const std::invalid_argument& e)
	{
		std::cout << e.what() << '\n';
	}
}

void ConsoleUI::remove_trench_coat()
{
	std::string size = read_size("Size (XS/S/M/L/XL/XXL): ");
	std::string colour = read_colour("Colour: ");

	try {
		service.remove(size, colour);
		std::cout << "Coat removed successfully.\n";
	}
	catch (const std::invalid_argument& e) {
		std::cout << "Error: " << e.what() << "\n";
	}
}

void ConsoleUI::update_trench_coat()
{
	std::string size = read_size("Size (XS/S/M/L/XL/XXL): ");
	std::string colour = read_colour("Colour: ");
	std::string photoLink = read_string("New photo URL: ");
	double      price = read_double("New price: ");
	int         quantity = read_integer("New quantity: ");

	try {
		service.update(size, colour, photoLink, price, quantity);
		std::cout << "Coat updated successfully.\n";
	}
	catch (const std::invalid_argument& e) {
		std::cout << "Error: " << e.what() << "\n";
	}
}

void ConsoleUI::display_all_trench_coats()
{
	DynamicVector<TrenchCoat>& coats = this->service.get_all_coats();
	if (coats.getLength() == 0)
	{
		std::cout << "No trench coats in inventory." << std::endl;
		return;
	}
	std::cout << "Trench Coats in Inventory:" << std::endl;
	for (int i= 0; i < coats.getLength(); i++)
	{
		std::cout << coats.get(i).to_string() << std::endl;
	}
}

void ConsoleUI::see_coats_of_given_size()
{
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	std::string size = read_size_or_empty("Size (XS/S/M/L/XL/XXL): ");
	DynamicVector<TrenchCoat> coats = service.get_coats_by_size(size);
	if (coats.getLength() == 0)
	{
		std::cout << "No trench coats in the inventory! Sorry!" << std::endl;
		return;
	}
	bool finish = false;
	for (int i = 0; i < coats.getLength() && !finish; i++)
	{
		//show trench coat information
		std::cout << i+1 << " " << coats.get(i).to_string_user() << std::endl;
		std::string url = coats.get(i).get_photoLink();
		ShellExecuteA(NULL, "open", url.c_str(), NULL, NULL, SW_SHOWNORMAL);

		//possibility to add to the shopping basket
		int choice = -1;
		while (choice)
		{
			std::cout << "1. Add the trench coat to the basket.\n";
			std::cout << "2. Do not add the trench coat to the basket.\n";
			std::cout << "0. Finish shoppping session.\n";
			choice = read_integer("Enter your option: ");
			if (choice == 1)
			{
				try
				{
					this->service.add_to_basket(coats.get(i));
					coats = service.get_coats_by_size(size);
					std::cout << "Trench coat was added to your basket!\n";
				}
				catch (std::invalid_argument& e)
				{
					std::cout << e.what() << '\n';
				}
				std::cout << "So far, the total price of your items is: " << this->service.get_total_price() << '\n';
				break;
			}
			else if (choice == 2)
				break;
			else if (choice == 0)
				finish = true;
			else
				std::cout << "Invalid option!\n";
		}

		//if we get to the last trench coat, the user may repeat the process
		if (i == coats.getLength() - 1)
		{
			int option = -1;
			std::cout << "1. Exit the trench coat display.\n";
			std::cout << "2. Display the trench coats again.\n";
			
			while (option!=1)
			{
				option = read_integer("Enter your option: ");
				if (option == 1)
					break;
				else if (option == 2)
				{
					i = -1;
					break;
				}
				else
					std::cout << "Invalid option!";
			}
		}
	}
}

void ConsoleUI::see_basket()
{
	DynamicVector<TrenchCoat> basket_coats = this->service.get_basket();
	for (int i = 0; i < basket_coats.getLength(); i++)
		std::cout << basket_coats.get(i).to_string_user() << '\n';
	std::cout << "Total price of your items is: " << this->service.get_total_price()<<'\n';
}



void ConsoleUI::filter_user_coats_by_length() {
	int limit = read_integer("Enter maximum length to filter by: ");

	DynamicVector<TrenchCoat> result = service.filter_by_length(limit);

	if (result.getLength() == 0) {
		std::cout << "No coats found shorter than " << limit << ".\n";
	}
	else {
		for (int i = 0; i < result.getLength(); i++) {
			std::cout << result.get(i).to_string_user() << "\n";
		}
	}
}