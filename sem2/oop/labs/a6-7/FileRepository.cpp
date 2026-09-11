#include "FileRepository.h"
#include "Exceptions.h"
#include<fstream>
#include<algorithm>

FileRepository::FileRepository(const std::string& filename) : filename(filename)
{
	load_file();
}


//helper function to read from file and write to file 
void FileRepository::load_file()
{
	std::ifstream fin(this->filename);
	if (!fin.is_open())
		return;

	TrenchCoat coat;
	while (fin >> coat)
	{
		if (!coat.get_size().empty())
			this->coats.push_back(coat);
	}
}

void FileRepository::save_file()
{
	std::ofstream fout(this->filename);
	for (const TrenchCoat& c : this->coats)
		fout << c << '\n';
}

void FileRepository::add_trench_coat(const TrenchCoat& coat)
{
	if (find_trench_coat(coat.get_size(), coat.get_colour()) != nullptr)
		throw DuplicateException();

	this->coats.push_back(coat);
	save_file();
}

void FileRepository::remove_trench_coat(const TrenchCoat& coat)
{
	auto position = std::find(this->coats.begin(), this->coats.end(), coat);
	if (position == this->coats.end())
		throw NotFoundException();

	this->coats.erase(position);
	save_file();
}

void FileRepository::update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat)
{
	auto position = std::find(this->coats.begin(), this->coats.end(), oldCoat);
	if (position == this->coats.end())
		throw NotFoundException();

	*position = newCoat;
	save_file();
}

std::vector<TrenchCoat>& FileRepository::get_all_trench_coats()
{
	return this->coats;
}

TrenchCoat* FileRepository::find_trench_coat(const std::string& size, const std::string& colour)
{
	for (TrenchCoat& c : this->coats)
	{
		if (c.get_size() == size && c.get_colour() == colour)
		{
			return &c;
		}
	}
	return nullptr;
}
