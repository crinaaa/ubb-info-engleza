#include "service.h"
#include<stdlib.h>
#include<stdio.h>
#include<string.h>

Service* createService(EstateRepo* repo)
{
    Service* service = (Service*)malloc(sizeof(Service));
    if (!service)
        return NULL;

	//make a copy to work on it without modifying the original repo
    service->repo = copyRepo(repo);
    if (!service->repo)
    {
        free(service);
        return NULL;
    }

    service->undoStack = createDynamicVector(10, (DestroyElementFunctionPointer)destroyRepo);
    service->redoStack = createDynamicVector(10, (DestroyElementFunctionPointer)destroyRepo);

    if (!service->undoStack || !service->redoStack)
    {
        if (service->undoStack)
            destroyDynamicVector(service->undoStack);
        if (service->redoStack)
            destroyDynamicVector(service->redoStack);
        destroyRepo(service->repo);
        free(service);
        return NULL;
    }

    return service;
}

void destroyService(Service* service)
{
    if (service)
    {
        if (service->undoStack)
            destroyDynamicVector(service->undoStack);
        if (service->redoStack)
            destroyDynamicVector(service->redoStack);
        if (service->repo)
            destroyRepo(service->repo);
        free(service);
    }
}

void saveStateForUndo(Service* service)
{
    if (!service)
        return;

    //clear redo stack when a new operation is performed
    for (int i = 0; i < getLength(service->redoStack); i++)
        destroyRepo((EstateRepo*)getElement(service->redoStack, i));
    service->redoStack->length = 0;

    //save current state to undo stack
    EstateRepo* currentState = copyRepo(service->repo);
    addElement(service->undoStack, currentState);
}

int serviceAddEstate(Service* service, char* type, char* address, double surface, double price)
{
    if (!service || !type || !address)
        return 0;

    //validate type
    if (strcmp(type, "house") != 0 && strcmp(type, "apartment") != 0 && strcmp(type, "penthouse") != 0)
        return 0;

    //validate surface and price
    if (surface <= 0 || price <= 0)
        return 0;

    //save the state for undo
    saveStateForUndo(service);

    //create estate
    Estate* estate = createEstate(type, address, surface, price);
    if (!estate)
        return 0;

    //add to repo
    if (!addEstate(service->repo, estate))
    {
        destroyEstate(estate);
        return 0;
    }

    return 1;
}

int serviceDeleteEstate(Service* service, char* address)
{
    if (!service || !address)
        return 0;

    //save state for undo
    saveStateForUndo(service);

    return deleteEstate(service->repo, address);
}

int serviceUpdateEstate(Service* service, char* address, char* newType, double newSurface, double newPrice)
{
    if (!service || !address || !newType)
        return 0;

    //validate type
    if (strcmp(newType, "house") != 0 && strcmp(newType, "apartment") != 0 && strcmp(newType, "penthouse") != 0)
        return 0;

    //validate surface and price
    if (newSurface <= 0 || newPrice <= 0)
        return 0;

    //save state for undo
    saveStateForUndo(service);

    //create new estate
    Estate* newEstate = createEstate(newType, address, newSurface, newPrice);
    if (!newEstate)
        return 0;

    if (!updateEstate(service->repo, address, newEstate))
    {
        destroyEstate(newEstate);
        return 0;
    }

    return 1;
}

DynamicVector* getAllEstatesService(Service* service)
{
    if (!service)
        return NULL;

    DynamicVector* result = createDynamicVector(10, NULL);
    DynamicVector* allEstates = getAllEstatesRepo(service->repo);

    for (int i = 0; i < getLength(allEstates); i++)
        addElement(result, getElement(allEstates, i));

    return result;
}

DynamicVector* getEstatesByTypeAndSurfaceService(Service* service, char* type, double surface)
{
    if (!service || !type)
        return NULL;

    DynamicVector* result = createDynamicVector(10, NULL);
    DynamicVector* allEstates = getAllEstatesRepo(service->repo);

    for (int i = 0; i < getLength(allEstates); i++)
    {
        Estate* estate = (Estate*)getElement(allEstates, i);
        if (strcmp(getTypeOfEstate(estate), type) == 0 && getSurfaceOfEstate(estate) >= surface)
            addElement(result, estate);
    }
    return result;
}

//helper function to sort a vector of estates ascending by price
void sortAscendingByPrice(DynamicVector* v)
{
    for (int i = 0; i < getLength(v) - 1; i++)
    {
        for (int j = 0; j < getLength(v) - i - 1; j++)
        {
            Estate* estate1 = (Estate*)getElement(v, j);
            Estate* estate2 = (Estate*)getElement(v, j + 1);
            if (getPriceOfEstate(estate1) > getPriceOfEstate(estate2))
            {
                //swap
                TElem temp = getElement(v, j);
                updateElement(v, j, getElement(v, j + 1));
                updateElement(v, j + 1, temp);
            }
        }
    }
}

DynamicVector* getEstatesByAddressSubstringService(Service* service, char* substring)
{
    if (!service || !substring)
        return NULL;

    DynamicVector* result = createDynamicVector(10, NULL);
    DynamicVector* allEstates = getAllEstatesRepo(service->repo);

    for (int i = 0; i < getLength(allEstates); i++)
    {
        Estate* estate = (Estate*)getElement(allEstates, i);
        if (strstr(getAddressOfEstate(estate), substring) != NULL)
            addElement(result, estate);
    }
    sortAscendingByPrice(result);
    return result;
}


//helper function to sort a vector of estates ascending by address
void sortAscendingByAddress(DynamicVector* v)
{
    for (int i = 0; i < getLength(v) - 1; i++)
    {
        for (int j = 0; j < getLength(v) - i - 1; j++)
        {
            Estate* e1 = (Estate*)getElement(v, j);
            Estate* e2 = (Estate*)getElement(v, j + 1);
            if (strcmp(getAddressOfEstate(e1), getAddressOfEstate(e2)) > 0)
            {
				TElem tmp = getElement(v, j);  //auxiliary variable for swapping
                updateElement(v, j, getElement(v, j + 1));
                updateElement(v, j + 1, tmp);
            }
        }
    }
}

//return all estates of a given type, sorted ascending by address
DynamicVector* getEstatesByTypeSortedByAddressService(Service* service, char* type)
{
    if (!service || !type)
        return NULL;

    DynamicVector* result = createDynamicVector(10, NULL);
    if (!result)
        return NULL;

    DynamicVector* all = getAllEstatesRepo(service->repo);
    for (int i = 0; i < getLength(all); i++)
    {
        Estate* estate = (Estate*)getElement(all, i);
        if (strcmp(getTypeOfEstate(estate), type) == 0)
            addElement(result, estate);
    }

    sortAscendingByAddress(result);
    return result;
}


int serviceUndo(Service* service)
{
    if (!service)
        return 0;
    if (getLength(service->undoStack) == 0)
        return 0;   //nothing to undo

    //save current state for redo
    EstateRepo* currentCopy = copyRepo(service->repo);
    if (currentCopy)
        addElement(service->redoStack, currentCopy);

    //restore state from undo stack
    EstateRepo* previousState = (EstateRepo*)getElement(service->undoStack, getLength(service->undoStack) - 1);

    destroyRepo(service->repo);
    service->repo = copyRepo(previousState);

    //remove last element from undo stack
    service->undoStack->length--;
    destroyRepo(previousState);
    return 1;

}

int serviceRedo(Service* service)
{
    if (!service)
        return 0;
    if (getLength(service->redoStack) == 0)
        return 0;   //nothing to redo

    //save current state for undo
    EstateRepo* currentCopy = copyRepo(service->repo);
    if (currentCopy)
        addElement(service->undoStack, currentCopy);

    //restore state from redo stack
    EstateRepo* nextState = (EstateRepo*)getElement(service->redoStack, getLength(service->redoStack) - 1);

    destroyRepo(service->repo);
    service->repo = copyRepo(nextState);

    //remove last element from redo stack
    service->redoStack->length--;
    destroyRepo(nextState);

    return 1;
}

DynamicVector* getEstatesBySurfaceSortedByPriceService(Service* service, double surface)
{
    if (!service)
        return NULL;

    DynamicVector* result = createDynamicVector(10, NULL);
    DynamicVector* allEstates = getAllEstatesRepo(service->repo);

    for (int i = 0; i < getLength(allEstates); i++)
    {
        Estate* estate = (Estate*)getElement(allEstates, i);
        if (getSurfaceOfEstate(estate) == surface)
            addElement(result, estate);
    }

    sortAscendingByPrice(result);
	return result;
}
