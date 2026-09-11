#include "estate.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

Estate* createEstate(char* type, char* address, double surface, double price)
{
	Estate* estate = (Estate*)malloc(sizeof(Estate));
	if (!estate)
		return NULL;

	//allocate memory for the type
	estate->type = (char*)malloc(sizeof(char) * (strlen(type) + 1));
	if (!estate->type)
	{
		free(estate);
		return NULL;
	}
	strcpy(estate->type, type);

	//allocate memory for the address
	estate->address = (char*)malloc(sizeof(char) * (strlen(address) + 1));
	if (!estate->address)
	{
		free(estate->type);
		free(estate);
		return NULL;
	}
	strcpy(estate->address, address);

	estate->surface = surface;
	estate->price = price;
	return estate;
}

//getters
char* getTypeOfEstate(Estate* estate)
{
	return estate->type;
}

char* getAddressOfEstate(Estate* estate)
{
	return estate->address;
}

double getSurfaceOfEstate(Estate* estate)
{
	return estate->surface;
}

double getPriceOfEstate(Estate* estate)
{
	return estate->price;
}

Estate* copyEstate(Estate* estate)
{
	return createEstate(getTypeOfEstate(estate), getAddressOfEstate(estate), getSurfaceOfEstate(estate), getPriceOfEstate(estate));
}

void destroyEstate(Estate* estate)
{
	if (estate)
	{
		if (estate->type)
			free(estate->type);
		if (estate->address)
			free(estate->address);
		free(estate);
	}
}