//#include "Repository.h"
//
//Repository::Repository() {}
//
//void Repository::add_trench_coat(const TrenchCoat& coat)
//{
//    this->coats.push_back(coat);
//}
//
//void Repository::remove_trench_coat(const TrenchCoat& coat)
//{
//    std::vector<TrenchCoat>::iterator position = std::find(this->coats.begin(), this->coats.end(), coat);
//    this->coats.erase(position);
//}
//
//void Repository::update_trench_coat(const TrenchCoat& oldCoat, const TrenchCoat& newCoat)
//{
//    std::vector<TrenchCoat>::iterator position = std::find(this->coats.begin(), this->coats.end(), oldCoat);
//    if (position == this->coats.end())
//        return;
//    else
//        *position = newCoat;
//}
//
//std::vector<TrenchCoat>& Repository::get_all_trench_coats()
//{
//	return coats;
//}
//
//TrenchCoat* Repository::find_trench_coat(const std::string& size, const std::string& colour)
//{
//    for (TrenchCoat& coat : coats)
//    {
//        if (coat.get_size() == size && coat.get_colour() == colour)
//            return &coat;
//    }
//    return nullptr;
//}