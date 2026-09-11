#include "Service.h"
#include "Exceptions.h"
#include "CoatValidator.h"
#include <stdexcept>
#include <algorithm>
#include <vector>

Service::Service(IRepository& repo) : repo(repo) {}

//void Service::add(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity)
//{
//	//validation
//	CoatValidator::validate(size, colour, photoLink, price, quantity);
//
//	TrenchCoat coat(size, colour, photoLink, price, quantity);
//	repo.add_trench_coat(coat); //it throws an exception if the coat already exists
//}

void Service::add(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity)
{
	CoatValidator::validate(size, colour, photoLink, price, quantity);
	TrenchCoat coat(size, colour, photoLink, price, quantity);

	repo.add_trench_coat(coat);

	// Save action and clear redo history
	undoStack.push_back(std::make_unique<ActionAdd>(repo, coat));
	redoStack.clear();
}


//void Service::remove(const std::string& size, const std::string& colour)
//{
//	//check if the coat exists
//	TrenchCoat* wanted = repo.find_trench_coat(size, colour);
//	if (wanted == nullptr)
//		throw NotFoundException();
//
//	//check if quantity is 0
//	if (wanted->get_quantity() != 0)
//		throw ValidationException("There still are trench coats of this model!");
//
//	TrenchCoat coat(size, colour, "", 0, 0); //the photo link, price and quantity don't matter for removal
//	repo.remove_trench_coat(coat);
//}

void Service::remove(const std::string& size, const std::string& colour)
{
	TrenchCoat* wanted = repo.find_trench_coat(size, colour);
	if (wanted == nullptr) throw NotFoundException();
	if (wanted->get_quantity() != 0) throw ValidationException("There still are trench coats of this model!");

	TrenchCoat snapshot = *wanted; // capture all fields for restoration later
	repo.remove_trench_coat(snapshot);

	undoStack.push_back(std::make_unique<ActionRemove>(repo, snapshot));
	redoStack.clear();
}

//void Service::update(const std::string& size, const std::string& colour, const std::string& newPhotoLink, double newPrice, int newQuantity)
//{
//	//validation
//	CoatValidator::validate(size, colour, newPhotoLink, newPrice, newQuantity);
//
//	TrenchCoat* oldCoat = repo.find_trench_coat(size, colour);
//	//check if the coat exists
//	if (oldCoat == nullptr)
//		throw NotFoundException();
//
//	//update the coat in the repo
//	TrenchCoat newCoat(size, colour, newPhotoLink, newPrice, newQuantity);
//	repo.update_trench_coat(*oldCoat, newCoat);
//}

void Service::update(const std::string& size, const std::string& colour, const std::string& newPhotoLink, double newPrice, int newQuantity)
{
	CoatValidator::validate(size, colour, newPhotoLink, newPrice, newQuantity);
	TrenchCoat* oldCoat = repo.find_trench_coat(size, colour);
	if (oldCoat == nullptr) throw NotFoundException();

	TrenchCoat oldSnapshot = *oldCoat;
	TrenchCoat newCoat(size, colour, newPhotoLink, newPrice, newQuantity);

	repo.update_trench_coat(*oldCoat, newCoat);

	undoStack.push_back(std::make_unique<ActionUpdate>(repo, oldSnapshot, newCoat));
	redoStack.clear();
}


//added for the last assignment
void Service::undo()
{
	if (undoStack.empty()) throw std::runtime_error("No more actions to undo!");

	undoStack.back()->undo();
	redoStack.push_back(std::move(undoStack.back()));
	undoStack.pop_back();
}

void Service::redo()
{
	if (redoStack.empty()) throw std::runtime_error("No more actions to redo!");

	redoStack.back()->redo();
	undoStack.push_back(std::move(redoStack.back()));
	redoStack.pop_back();
}

std::vector<TrenchCoat>& Service::get_all_coats()
{
	return repo.get_all_trench_coats();
}

std::vector<TrenchCoat> Service::get_coats_by_size(const std::string& size)
{
	std::vector<TrenchCoat>& all = this->repo.get_all_trench_coats();
	if (size.empty())
		return all;

	std::vector<TrenchCoat> selected;
	std::copy_if(all.begin(), all.end(), std::back_inserter(selected), [&size](const TrenchCoat& c) {return c.get_size() == size; });

	return selected;
}

std::vector<TrenchCoat> Service::get_basket()
{
	return this->basket;
}

void Service::add_to_basket(const TrenchCoat& coat)
{
	TrenchCoat* repoCoat = this->repo.find_trench_coat(coat.get_size(), coat.get_colour());
	if (repoCoat == nullptr)
		throw NotFoundException();
	if (repoCoat->get_quantity() <= 0)
		throw ValidationException("Empty stock!");

	// copy FIRST before anything modifies the vector
	TrenchCoat snapshot = *repoCoat;

	this->basket.push_back(snapshot);
	this->total_price += snapshot.get_price();

	TrenchCoat updated = snapshot;
	updated.set_quantity(snapshot.get_quantity() - 1);
	repo.update_trench_coat(snapshot, updated);
}

int Service::get_total_price()
{
	return total_price;
}

void Service::file_basket(FileBasket& fileBasket)
{
	fileBasket.setBasket(this->basket);
	fileBasket.display();
}

void Service::sortByColour(bool ascending)
{
	std::vector<TrenchCoat>& allCoats = repo.get_all_trench_coats();

	std::sort(allCoats.begin(), allCoats.end(),
		[ascending](const TrenchCoat& a, const TrenchCoat& b) {
			if (ascending)
				return a.get_colour() < b.get_colour();
			else
				return a.get_colour() > b.get_colour(); 
		}
	);
}