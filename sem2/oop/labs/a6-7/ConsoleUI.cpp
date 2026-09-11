#include "ConsoleUI.h"
#include "Exceptions.h"
#include "CSV_Basket.h"
#include "HTML_Basket.h"
#include <iostream>
#include <stdexcept>
#include <limits>
#include <cctype>
#include <algorithm>
#include <windows.h>
#undef max

// helper functions

int read_integer(const std::string& prompt)
{
	int value;
	std::cout << prompt;
	std::cin >> value;
	if (!std::cin.good())
	{
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
		throw ValidationException("Invalid input. Please enter a valid integer.");
	}
	return value;
}

double read_double(const std::string& prompt)
{
	double value;
	std::cout << prompt;
	std::cin >> value;
	if (!std::cin.good())
	{
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
		throw ValidationException("Invalid input. Please enter a valid number.");
	}
	return value;
}

std::string read_string(const std::string& prompt)
{
	std::string value;
	std::cout << prompt;
	std::cin >> value;
	if (value.empty())
		throw ValidationException("Input cannot be empty.");
	return value;
}

std::string read_size_or_empty(const std::string& prompt)
{
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	std::string value;
	std::cout << prompt;
	std::getline(std::cin, value);

	if (value.empty())
		return value;

	std::string upper = value;
	std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);

	if (upper != "XS" && upper != "S" && upper != "M" &&
		upper != "L" && upper != "XL" && upper != "XXL")
		throw ValidationException("Invalid size. Allowed values: XS, S, M, L, XL, XXL, or press Enter for all.");

	return upper;
}

std::string read_size(const std::string& prompt)
{
	std::string value = read_size_or_empty(prompt);
	if (value.empty())
		throw ValidationException("Size cannot be empty. Allowed values: XS, S, M, L, XL, XXL.");
	return value;
}

std::string read_colour(const std::string& prompt)
{
	std::string value;
	std::cout << prompt;
	std::cin >> value;

	if (value.empty())
		throw ValidationException("Colour cannot be empty.");

	for (char c : value)
		if (!std::isalpha(c))
			throw ValidationException("Invalid colour. Please enter letters only.");

	return value;
}


ConsoleUI::ConsoleUI(Service& service) : service(service) {}

void ConsoleUI::run()
{
	int option = 0;
	while (option != 1 && option != 2)
	{
		std::cout << "Select basket file type:\n";
		std::cout << "1. CSV\n";
		std::cout << "2. HTML\n";
		std::cout << "0. Exit\n";

		try
		{
			option = read_integer("Enter your choice: ");
			if (option != 1 && option != 2 && option != 0)
				std::cout << "Invalid choice. Please enter 1, 2 or 0.\n";
			else if (option == 0)
				break;  // exit the loop
		}
		catch (const std::exception& e)
		{
			std::cout << "Error: " << e.what() << "\n";
		}
	}

	if (option == 1)
		fileBasket = std::make_unique<CSV_Basket>("basket.csv");
	else if (option == 2)
		fileBasket = std::make_unique<HTML_Basket>("basket.html");
	else
		return;

	int choice = -1;
	while (choice)
	{
		std::cout << "Welcome to the Trench Coat Management System!" << std::endl;
		std::cout << "Please select your role:" << std::endl;
		std::cout << "1. Administrator" << std::endl;
		std::cout << "2. User" << std::endl;
		std::cout << "0. Exit" << std::endl;

		try
		{
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
		catch (const std::exception& e)
		{
			std::cout << "Error: " << e.what() << "\n";
		}
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

		try
		{
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
		catch (const std::exception& e)
		{
			std::cout << "Error: " << e.what() << "\n";
		}
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
		std::cout << "3. See shopping basket in a file of your choice.\n";
		std::cout << "0. Exit.\n";

		try
		{
			choice = read_integer("Enter your choice: ");
			if (choice == 1)
				see_coats_of_given_size();
			else if (choice == 2)
				see_basket();
			else if (choice == 3)
				open_basket_file();
			else if (choice == 0)
				return;
			else
				std::cout << "Invalid command!\n";
		}
		catch (const std::exception& e)
		{
			std::cout << "Error: " << e.what() << "\n";
		}
	}
}

void ConsoleUI::add_trench_coat()
{
	try
	{
		std::string size = read_size("Enter the size: ");
		std::string colour = read_colour("Enter the colour: ");
		std::string photoLink = read_string("Enter the photo link: ");
		double price = read_double("Enter the price: ");
		int quantity = read_integer("Enter the quantity: ");
		service.add(size, colour, photoLink, price, quantity);
		std::cout << "Coat added successfully!\n";
	}
	catch (const std::exception& e)
	{
		std::cout << "Error: " << e.what() << "\n";
	}
}

void ConsoleUI::remove_trench_coat()
{
	try
	{
		std::string size = read_size("Size (XS/S/M/L/XL/XXL): ");
		std::string colour = read_colour("Colour: ");
		service.remove(size, colour);
		std::cout << "Coat removed successfully.\n";
	}
	catch (const std::exception& e)
	{
		std::cout << "Error: " << e.what() << "\n";
	}
}

void ConsoleUI::update_trench_coat()
{
	try
	{
		std::string size = read_size("Size (XS/S/M/L/XL/XXL): ");
		std::string colour = read_colour("Colour: ");
		std::string photoLink = read_string("New photo URL: ");
		double price = read_double("New price: ");
		int quantity = read_integer("New quantity: ");
		service.update(size, colour, photoLink, price, quantity);
		std::cout << "Coat updated successfully.\n";
	}
	catch (const std::exception& e)
	{
		std::cout << "Error: " << e.what() << "\n";
	}
}

void ConsoleUI::display_all_trench_coats()
{
	std::vector<TrenchCoat>& coats = this->service.get_all_coats();
	if (coats.size() == 0)
	{
		std::cout << "No trench coats in inventory." << std::endl;
		return;
	}
	std::cout << "Trench Coats in Inventory:" << std::endl;
	for (const TrenchCoat& coat : coats)
	{
		std::cout << coat.to_string() << std::endl;
	}
}

void ConsoleUI::see_coats_of_given_size()
{
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	std::string size = read_size_or_empty("Size (XS/S/M/L/XL/XXL): ");

	if (service.get_coats_by_size(size).size() == 0)
	{
		std::cout << "No trench coats in the inventory! Sorry!\n";
		return;
	}

	bool finish = false;
	bool restart = true;

	while (restart && !finish)
	{
		std::vector<TrenchCoat> coats = service.get_coats_by_size(size);
		restart = false;

		std::for_each(coats.begin(), coats.end(), [&](const TrenchCoat& coat)
			{
				if (finish) return;

				std::cout << coat.to_string() << "\n";
				ShellExecuteA(NULL, "open", coat.get_photoLink().c_str(), NULL, NULL, SW_SHOWNORMAL);

				int choice = -1;
				while (choice)
				{
					std::cout << "1. Add the trench coat to the basket.\n";
					std::cout << "2. Do not add the trench coat to the basket.\n";
					std::cout << "0. Finish shopping session.\n";
					choice = read_integer("Enter your option: ");

					if (choice == 1)
					{
						try
						{
							service.add_to_basket(coat);
							std::cout << "Trench coat was added to your basket!\n";
							std::cout << "Total so far: " << service.get_total_price() << "\n";


							//save to the file containing the shooping basket
							fileBasket->setBasket(service.get_basket());
							fileBasket->writeToFile();
						}
						catch (const std::exception& e) { std::cout << e.what() << "\n"; }
						break;
					}
					else if (choice == 2) break;
					else if (choice == 0) { finish = true; break; }
					else std::cout << "Invalid option!\n";
				}
			});

		if (!finish)
		{
			std::cout << "1. Exit the trench coat display.\n";
			std::cout << "2. Display the trench coats again.\n";

			int option = -1;
			while (option != 1)
			{
				option = read_integer("Enter your option: ");
				if (option == 1) restart = false;
				else if (option == 2) restart = true;
				else std::cout << "Invalid option!\n";
				break;
			}
		}
	}
}

void ConsoleUI::see_basket()
{
	std::vector<TrenchCoat> basket_coats = this->service.get_basket();
	for (const TrenchCoat& coat : basket_coats)
		std::cout << coat.to_string_user() << '\n';
	std::cout << "Total price of your items is: " << this->service.get_total_price() << '\n';
}


void ConsoleUI::open_basket_file()
{
	std::vector<TrenchCoat> basket_coats = this->service.get_basket();
	if (basket_coats.empty())
	{
		std::cout << "Your basket is empty.\n";
		return;
	}

	fileBasket->setBasket(basket_coats);
	fileBasket->display();
}