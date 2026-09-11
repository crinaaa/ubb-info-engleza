#pragma once
#include "FileBasket.h"

class HTML_Basket : public FileBasket
{
public:
	//constructor
	HTML_Basket(const std::string& filename = "basket.html") : FileBasket(filename) {}
	//function to write the content of the basket to the file
	void writeToFile() const override;
	//function to display the content of the basket, that is, it opens the corresponding app for the HTML file
	void display() const override;
};

