#pragma once

//struct holding estate data: type, address, surface and price
typedef struct
{
	char* type;
	char* address;
	double surface;
	double price;
}Estate;

//create new estate (constructor)
Estate* createEstate(char* type, char* address, double surface, double price);

//free the memory allocated for an estate (destructor)
void destroyEstate(Estate* estate);

//getters and copy function
char* getTypeOfEstate(Estate* estate);
char* getAddressOfEstate(Estate* estate);
double getSurfaceOfEstate(Estate* estate);
double getPriceOfEstate(Estate* estate);
Estate* copyEstate(Estate* estate);