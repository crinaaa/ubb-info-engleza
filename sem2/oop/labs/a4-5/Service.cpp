#include "Service.h"
#include <stdexcept>

Service::Service(Repository& repo) : repo(repo) {}

void Service::add(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity)
{
	//validation
	if (size.empty())
		throw std::invalid_argument("Size cannot be empty.");
	if (colour.empty())
		throw std::invalid_argument("Colour cannot be empty.");
	if (photoLink.empty())
		throw std::invalid_argument("Photo link cannot be empty.");
	if (price < 0)
		throw std::invalid_argument("Price cannot be negative.");
	if (quantity < 0)
		throw std::invalid_argument("Quantity cannot be negative.");

	//check if the coat already exists (same size and colour)
	if (repo.find_trench_coat(size, colour) != nullptr)
		throw std::invalid_argument("A trench coat with the same size and colour already exists.");

	TrenchCoat coat(size, colour, photoLink, price, quantity);
	repo.add_trench_coat(coat);
}

void Service::remove(const std::string& size, const std::string& colour)
{
	//validation
	if (size.empty())
		throw std::invalid_argument("Size cannot be empty.");
	if (colour.empty())
		throw std::invalid_argument("Colour cannot be empty.");

	//check if the coat exists
	TrenchCoat* wanted = repo.find_trench_coat(size, colour);
	if (wanted == nullptr)
		throw std::invalid_argument("No trench coat with the given size and colour exists.");

	//check if quantity is 0
	if (wanted->get_quantity() != 0)
		throw std::invalid_argument("There still are trench coats of this model!");

	TrenchCoat coat(size, colour, "", 0, 0); //the photo link, price and quantity don't matter for removal
	repo.remove_trench_coat(coat);
}

void Service::update(const std::string& size, const std::string& colour, const std::string& newPhotoLink, double newPrice, int newQuantity)
{
	//validation
	if (size.empty())
		throw std::invalid_argument("Size cannot be empty.");
	if (colour.empty())
		throw std::invalid_argument("Colour cannot be empty.");
	if (newPhotoLink.empty())
		throw std::invalid_argument("Photo link cannot be empty.");
	if (newPrice < 0)
		throw std::invalid_argument("Price cannot be negative.");
	if (newQuantity < 0)
		throw std::invalid_argument("Quantity cannot be negative.");

	TrenchCoat* oldCoat = repo.find_trench_coat(size, colour);
	//check if the coat exists
	if (oldCoat == nullptr)
		throw std::invalid_argument("No trench coat with the given size and colour exists.");

	//update the coat in the repo
	TrenchCoat newCoat(size, colour, newPhotoLink, newPrice, newQuantity);
	repo.update_trench_coat(*oldCoat, newCoat);
}

DynamicVector<TrenchCoat>& Service::get_all_coats()
{
	return repo.get_all_trench_coats();
}

DynamicVector<TrenchCoat> Service::get_coats_by_size(const std::string& size)
{
	DynamicVector<TrenchCoat>& all = this->repo.get_all_trench_coats();
	if (size.empty())
		return all;
	DynamicVector<TrenchCoat> selected;
	for (int i = 0; i < all.getLength(); i++)
		if (all.get(i).get_size() == size)
			selected.add(all.get(i));
	return selected;
}

DynamicVector<TrenchCoat> Service::get_basket()
{
	return this->basket;
}

//void Service::add_to_basket(const TrenchCoat& coat)
//{
//	if (coat.get_quantity() <= 0)
//		throw std::invalid_argument("Empty stock!");
//	this->basket.add(coat);
//	this->total_price += coat.get_price();
//	this->repo.update_trench_coat(coat, TrenchCoat(coat.get_size(), coat.get_colour(), coat.get_photoLink(), coat.get_price(), coat.get_quantity() - 1));
//	TrenchCoat* coaty = this->repo.find_trench_coat(coat.get_size(), coat.get_colour());
//	coaty->set_quantity(coat.get_quantity() - 1);
//	//coat = coaty;
//}

void Service::add_to_basket(const TrenchCoat& coat)
{
	TrenchCoat* repoCoat = this->repo.find_trench_coat(coat.get_size(), coat.get_colour());
	if (repoCoat == nullptr)
		throw std::invalid_argument("Coat not found!");
	if (repoCoat->get_quantity() <= 0)
		throw std::invalid_argument("Empty stock!");

	this->basket.add(*repoCoat);
	this->total_price += repoCoat->get_price();
	repoCoat->set_quantity(repoCoat->get_quantity() - 1);
}

int Service::get_total_price()
{
	return total_price;
}


DynamicVector<TrenchCoat> Service::filter_by_length(int maxLength) {
	DynamicVector<TrenchCoat>& all = this->repo.get_all_trench_coats();
	DynamicVector<TrenchCoat> filtered;

	TrenchCoat threshold;
	threshold.setLengthCoat(maxLength); 

	for (int i = 0; i < all.getLength(); i++) {
		if (all.get(i) < threshold) {
			filtered.add(all.get(i));
		}
	}
	return filtered;
}