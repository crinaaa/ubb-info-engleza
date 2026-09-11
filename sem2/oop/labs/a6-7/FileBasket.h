#pragma once
#include "TrenchCoat.h"
#include <vector>
#include <string>

class FileBasket
{
protected:
	std::string filename;
	std::vector<TrenchCoat> basket;
public:
	//constructor
	FileBasket(const std::string& filename) : filename(filename) {}
	//destructor
	virtual ~FileBasket() = default;

	//setter for the shopping basket
	void setBasket(const std::vector<TrenchCoat>& basket) { this->basket = basket; }

	//virtual function for writing the shopping basket to the file
	virtual void writeToFile() const = 0;
	//virtual function for displaying the shopping basket
	virtual void display() const = 0;
};