#include "CSV_Basket.h"
#include<fstream>
#include<windows.h>

void CSV_Basket::writeToFile() const
{
	std::ofstream fout(this->filename);
	for (const TrenchCoat& c : this->basket)
	{
		fout << c.get_size() << "," << c.get_colour() << "," << c.get_photoLink() << "," << c.get_price() 
		<< "," << c.get_quantity()<<'\n';
	}
}

void CSV_Basket::display() const
{
	writeToFile();
	ShellExecuteA(NULL, "open", this->filename.c_str(), NULL, NULL, SW_SHOWNORMAL);
}