#pragma once
#include "TrenchCoat.h"
#include "Exceptions.h"

class CoatValidator
{
public:
	//validator for the objects of type TrenchCoat
	//check if the size is XS/S/M/L/XL/XXL
	//check if colour and link are not empty
	//check if price and quantity are not negative
	static void validate(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity);
};

