#pragma once
#include "FileBasket.h"

class CSV_Basket : public FileBasket
{
public:
	//constructor
	CSV_Basket(const std::string& filename = "basket.csv") : FileBasket(filename) {}
	//function to write the content of the basket to the file
	void writeToFile() const override;
	//function to display the content of the basket, that is, it opens the corresponding app for the CSV file
	void display() const override;
};

