#include "CoatValidator.h"

void CoatValidator::validate(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity)
{
	if (size.empty())
		throw ValidationException("Size cannot be empty.");

	if (size != "XS" && size != "S" && size != "M" &&
		size != "L" && size != "XL" && size != "XXL")
		throw ValidationException("Size must be one of: XS, S, M, L, XL, XXL.");

	if (colour.empty())
		throw ValidationException("Colour cannot be empty.");

	if (photoLink.empty())
		throw ValidationException("Photo link cannot be empty.");

	if (price < 0)
		throw ValidationException("Price cannot be negative.");

	if (quantity < 0)
		throw ValidationException("Quantity cannot be negative.");
}
