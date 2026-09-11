#include "HTML_Basket.h"
#include <fstream>
#include <windows.h>

void HTML_Basket::writeToFile() const
{
	std::ofstream fout(this->filename);
	fout << "<!DOCTYPE html>\n<html>\n<head>\n";
	fout << "    <title>Shopping Basket</title>\n";
	fout << "</head>\n<body>\n<table border=\"1\">\n";

	fout << "    <tr>\n";
	fout << "        <td>Size</td>\n";
	fout << "        <td>Colour</td>\n";
	fout << "        <td>Price</td>\n";
	fout << "        <td>Photo</td>\n";
	fout << "    </tr>\n";

	for (const TrenchCoat& coat : this->basket)
	{
		fout << "    <tr>\n";
		fout << "        <td>" << coat.get_size() << "</td>\n";
		fout << "        <td>" << coat.get_colour() << "</td>\n";
		fout << "        <td>" << coat.get_price() << "</td>\n";
		fout << "        <td><a href=\"" << coat.get_photoLink() << "\">Link</a></td>\n";
		fout << "    </tr>\n";
	}

	fout << "</table>\n</body>\n</html>\n";
}

void HTML_Basket::display() const
{
	writeToFile();
	ShellExecuteA(NULL, "open", this->filename.c_str(), NULL, NULL, SW_SHOWNORMAL);
}