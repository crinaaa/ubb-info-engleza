#pragma once
#include "TrenchCoat.h"
#include<vector>

class IRepository
{
public:
	//virtual destructor
	virtual ~IRepository() = default;

	//takes an object ot type TrenchCoat and adds it to the repository
	//pre condition: the coat is not already in the repo 
	//throw exception if the coat is already in the repo
	virtual void add_trench_coat(const TrenchCoat& coat) = 0;
	//remove a trench coat from the repository
	//pre condition: the coat exists in the repo
	//throw exception if the coat does nto exist
	virtual void remove_trench_coat(const TrenchCoat& coat) = 0;
	//update a trench coat from the repository with a new one
	//pre condition: the oldCoat exists in the repo
	//throw exception if the oldCoat does 
	virtual void update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat) = 0;
	//get all trench coats in the repository
	virtual std::vector<TrenchCoat>& get_all_trench_coats() = 0;

	//find a trench coat by size and colour, return the coat if found, otherwise return a default coat with empty size and colour
	virtual TrenchCoat* find_trench_coat(const std::string& size, const std::string& colour) = 0;
};