#include "repository.h"
#include<stdlib.h>
#include<stdio.h>
#include<string.h>

EstateRepo* createRepo()
{
    EstateRepo* repo = (EstateRepo*)malloc(sizeof(EstateRepo));
    if (!repo)
        return NULL;
    
    repo->estates = createDynamicVector(10, (DestroyElementFunctionPointer)destroyEstate);
    if (!repo->estates)
    {
        free(repo);
        return NULL;
    }

    return repo;
}

void destroyRepo(EstateRepo* repo)
{
    if (!repo)
        return;

    destroyDynamicVector(repo->estates);
    free(repo);
}

int addEstate(EstateRepo* repo, Estate* estate)
{
    if (!repo || !estate)
        return 0;
    addElement(repo->estates, estate);
    return 1;
}

int deleteEstate(EstateRepo* repo, char* address)
{
    if (!repo || !address)
        return 0;

    int pos = findEstatePositionByAddress(repo, address);
    if (pos == -1)
        return 0;

    deleteElement(repo->estates, pos);
    return 1;
}

int updateEstate(EstateRepo* repo, char* address, Estate* newEstate)
{
    if (!repo || !address)
        return 0;

    int pos = findEstatePositionByAddress(repo, address);
    if (pos == -1)
        return 0;

    updateElement(repo->estates, pos, newEstate);
    return 1;
}

int findEstatePositionByAddress(EstateRepo* repo, char* address)
{
    for (int i = 0; i < getLength(repo->estates); i++)
    {
        Estate* estate = (Estate*)getElement(repo->estates, i);
        if (strcmp(getAddressOfEstate(estate), address) == 0)
            return i;
    }
    return -1;
}

DynamicVector* getAllEstatesRepo(EstateRepo* repo)
{
    return repo->estates;
}

EstateRepo* copyRepo(EstateRepo* repo)
{
	EstateRepo* newRepo = createRepo();
    if (!newRepo)
		return NULL;
	DynamicVector* allEstates = getAllEstatesRepo(repo);
    for (int i = 0; i < getLength(allEstates); i++)
    {
        Estate* estate = (Estate*)getElement(allEstates, i);
        Estate* copied = copyEstate(estate);
        addElement(newRepo->estates, copied);
	}

    return newRepo;
}

