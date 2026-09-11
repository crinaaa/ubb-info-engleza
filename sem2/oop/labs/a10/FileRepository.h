#pragma once
#include "IRepository.h"
#include<string>

class FileRepository : public IRepository
{
private:
	std::vector<TrenchCoat> coats;
	std::string filename;

	//helper function to read from file
	void load_file();

	//helper function to write to file
	void save_file();

public:
	explicit FileRepository(const std::string& filename = "coats.txt");

	//takes an object ot type TrenchCoat and adds it to the repository
	//pre condition: the coat is not already in the repo 
	//throw exception if the coat is already in the repo
	//overrides the method from the IRepository class
	void add_trench_coat(const TrenchCoat& coat) override;
	//remove a trench coat from the repository
	//pre condition: the coat exists in the repo
	//throw exception if the coat does nto exist
	void remove_trench_coat(const TrenchCoat& coat) override;
	//update a trench coat from the repository with a new one
	//pre condition: the oldCoat exists in the repo
	//throw exception if the oldCoat does 
	void update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat) override;
	//get all trench coats in the repository
	std::vector<TrenchCoat>& get_all_trench_coats() override;

	//find a trench coat by size and colour, return the coat if found, otherwise return a default coat with empty size and colour
	TrenchCoat* find_trench_coat(const std::string& size, const std::string& colour) override;
};

