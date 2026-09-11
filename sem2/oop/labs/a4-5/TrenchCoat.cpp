#include "TrenchCoat.h"

TrenchCoat::TrenchCoat() : size(""), colour(""), photoLink(""), price(0), quantity(0) {}

TrenchCoat::TrenchCoat(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity)
{
	this->size = size;
	this->colour = colour;
	this->photoLink = photoLink;
	this->price = price;
	this->quantity = quantity;
}

bool TrenchCoat::operator==(const TrenchCoat& other) const
{
	return this->size == other.size && this->colour == other.colour;
}

int TrenchCoat::getLengthCoat() const
{
	return this->length;
}

void TrenchCoat::setLengthCoat(int newLength)
{
	this->length = newLength;
}

std::string TrenchCoat::get_size() const
{
	return this->size;
}


std::string TrenchCoat::get_colour() const
{
	return this->colour;
}

std::string TrenchCoat::get_photoLink() const
{
	return this->photoLink;
}

double TrenchCoat::get_price() const
{
	return this->price;
}

int TrenchCoat::get_quantity() const
{
	return this->quantity;
}

void TrenchCoat::set_size(const std::string& size)
{
	this->size = size;
}

void TrenchCoat::set_colour(const std::string& colour)
{
	this->colour = colour;
}

void TrenchCoat::set_photoLink(const std::string& photoLink)
{
	this->photoLink = photoLink;
}

void TrenchCoat::set_price(double price)
{
	this->price = price;
}

void TrenchCoat::set_quantity(int quantity)
{
	this->quantity = quantity;
}

std::string TrenchCoat::to_string() const
{
	return "[ " + this->size + " | " + this->colour + " | " + this->photoLink + " | " + 
		std::to_string(this->price) + " | " + std::to_string(this->quantity) + " ]";
}

std::string TrenchCoat::to_string_user() const
{
	return "[ " + this->size + " | " + this->colour + " | " + 
		std::to_string(this->price) + " | " + std::to_string(this->quantity) + " | "  + std::to_string(this->length) + " ]";
}

