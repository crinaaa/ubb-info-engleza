#pragma once
#include "TrenchCoat.h"
#include "DynamicVectorTemplate.h"

class Repository
{
private:
	DynamicVector<TrenchCoat> coats;
public:
	//constructor
	Repository();
	
	//takes an object ot type TrenchCoat and adds it to the repository
	//pre condition: the coat is not already in the repo 
	//throw exception if the coat is already in the repo
	void add_trench_coat(const TrenchCoat& coat);
	//remove a trench coat from the repository
	//pre condition: the coat exists in the repo
	//throw exception if the coat does nto exist
	void remove_trench_coat(const TrenchCoat& coat);
	//update a trench coat from the repository with a new one
	//pre condition: the oldCoat exists in the repo
	//throw exception if the oldCoat does 
	void update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat);
	//get all trench coats in the repository
	DynamicVector<TrenchCoat>& get_all_trench_coats();

	//find a trench coat by size and colour, return the coat if found, otherwise return a default coat with empty size and colour
	TrenchCoat* find_trench_coat(const std::string& size, const std::string& colour) const;
};

