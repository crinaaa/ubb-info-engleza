#include "Repository.h"

Repository::Repository() {}

void Repository::add_trench_coat(const TrenchCoat& coat)
{
	this->coats.add(coat);
}

void Repository::remove_trench_coat(const TrenchCoat& coat)
{
    for (int i=0;i<this->coats.getLength();i++)
    {
        if (coats.get(i) == coat)
        {
            this->coats.remove(i);
            return;
        }
	}
}

void Repository::update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat)
{
    for (int i=0;i<this->coats.getLength();i++)
    {
        if (coats.get(i) == oldCoat)
        {
            this->coats.update(i, newCoat);
            return;
        }
	}
}

DynamicVector<TrenchCoat>& Repository::get_all_trench_coats()
{
	return coats;
}

TrenchCoat* Repository::find_trench_coat(const std::string& size, const std::string& colour) const
{
    for (int i = 0; i < this->coats.getLength(); i++)
    {
        if (coats.get(i).get_size() == size && coats.get(i).get_colour() == colour)
            return &this->coats.get(i);
    }
    return nullptr;
}





