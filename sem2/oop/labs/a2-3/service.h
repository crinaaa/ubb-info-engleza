#pragma once
#include"repository.h"
#include"dynamic_vector.h"

typedef struct
{
	EstateRepo* repo;  //use a copy of the repo
	DynamicVector* undoStack;	//stack of previous states for undo
	DynamicVector* redoStack;	//stack of states for redo
}Service;

//create service
Service* createService(EstateRepo* repo);

//free the memory allocated for the service
void destroyService(Service* service);

//add an estate to the service. returns 1 if successful, 0 otherwise(invalid input)
int serviceAddEstate(Service* service, char* type, char* address, double surface, double price);

//delete an estate from the service. returns 1 if successful, 0 otherwise(estate not found)
int serviceDeleteEstate(Service* service, char* address);

//update an estate in the service. returns 1 if successful, 0 otherwise(estate not found or invalid input)
int serviceUpdateEstate(Service* service, char* address, char* newType, double newSurface, double newPrice);

//return a vector with all the estates in the service
DynamicVector* getAllEstatesService(Service* service);

//return a vector with all the estates of a given type and with surface greater or equal to a given value
DynamicVector* getEstatesByTypeAndSurfaceService(Service* service, char* type, double surface);

//return a vector with all the estates whose address contains a given substring
DynamicVector* getEstatesByAddressSubstringService(Service* service, char* substring);

//return a vector with all the estates of a given type, sorted ascending by address
DynamicVector* getEstatesByTypeSortedByAddressService(Service* service, char* type);

//undo the last performed operation. returns 1 if successful, 0 otherwise(nothing to undo)
int serviceUndo(Service* service);

//redo the last performed undo operation. returns 1 if successful, 0 otherwise(nothing to redo)
int serviceRedo(Service* service);

//for a given surface, display all offers, sorted ascending by price
DynamicVector* getEstatesBySurfaceSortedByPriceService(Service* service, double surface);