#pragma once
#include "FileBasket.h"
#include "IRepository.h"
#include "UndoRedoAction.h"
#include <stack>

class Service
{
private:
	IRepository& repo;
	std::vector<TrenchCoat> basket;
	int total_price = 0;


	//added fot the undo/reco functionality
	// Undo/redo stacks hold owning pointers to actions
	std::vector<std::unique_ptr<UndoRedoAction>> undoStack;
	std::vector<std::unique_ptr<UndoRedoAction>> redoStack;

public:
	//constructor
	Service(IRepository& repo);

	//admin operations
	
	//add a new trench coat
	//takes as input the size, the colour, the photo link, the price and the quantity
	//throw exception if the coat already exists
	void add(const std::string& size, const std::string& colour, const std::string& photoLink, double price, int quantity);
	//remove a trench coat
	//take as input the size and the colour, find the corresponding coat, and remove it
	//throw exception if the coat does not exist
	void remove(const std::string& size, const std::string& colour);
	//update a trench coat
	//take as parameters the size and the colour of the coat, find the coat and update it with the new values
	//throw exception if the coat does not exist
	void update(const std::string& size, const std::string& colour, const std::string& newPhotoLink, double newPrice, int newQuantity);
	//get all coats
	std::vector<TrenchCoat>& get_all_coats();

	//get all coats with a given size; if size is empty, get all coats
	std::vector<TrenchCoat> get_coats_by_size(const std::string& size);


	//get the basket
	std::vector<TrenchCoat> get_basket();

	//add a new coat to the basket
	//throw exception if the quantity is 0 (stock is empty)
	void add_to_basket(const TrenchCoat& coat);

	//return the total price of the coats that have been added
	int get_total_price();

	//
	void file_basket(FileBasket& fileBasket);


	//added now for sorting
	void sortByColour(bool ascending);



	//aded for undo/redo
	//undo/redo stacks hold owning pointers to actions
	//std::stack<std::unique_ptr<UndoRedoAction>> undoStack;
	//std::stack<std::unique_ptr<UndoRedoAction>> redoStack;
	void undo();
	void redo();
};

