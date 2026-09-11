#pragma once
#include <string>

class TrenchCoat
{
private:
	std::string size;
	std::string colour;
	std::string photoLink;
	double price;
	int quantity;

	//new data
	int length;

public:
	//constructors
	TrenchCoat();
	//copy constructor
	TrenchCoat(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity);
	//equality operator (two coats are "equal" if they have the same size and same colour)
	bool operator==(const TrenchCoat& other) const;

	
	//additional requirement
	//overload "<" operator
	bool operator<(const TrenchCoat& other) const { return this->length < other.length; }
	int getLengthCoat() const;
	void setLengthCoat(int newLength);


	//getters
	std::string get_size() const;
	std::string get_colour() const;
	std::string get_photoLink() const;
	double get_price() const;
	int get_quantity() const;

	//setters
	void set_size(const std::string& size);
	void set_colour(const std::string& colour);
	void set_photoLink(const std::string& photoLink);
	void set_price(double price);
	void set_quantity(int quantity);

	//convert to string (for display purposes)
	std::string to_string() const;

	//convert to string(for user display)
	std::string to_string_user() const;
};

