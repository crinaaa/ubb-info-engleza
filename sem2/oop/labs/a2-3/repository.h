#pragma once
#include"estate.h"
#include"dynamic_vector.h"

typedef struct
{
	DynamicVector* estates;
}EstateRepo;


//cerate and destroy the repo
EstateRepo* createRepo();
void destroyRepo(EstateRepo* repo);

//add an estate to the repo, return 1 if successful, 0 otherwise(if repo or estate is NULL)
int addEstate(EstateRepo* repo, Estate* estate);

//delete an estate from the repo by its address, return 1 if successful, 0 otherwise(if repo or address is NULL, or if no estate with the given address exists)
int deleteEstate(EstateRepo* repo, char* address);

//update an estate in the repo by its address, return 1 if successful, 0 otherwise(if repo or address is NULL, if no estate with the given address exists, or if newEstate is NULL)
int updateEstate(EstateRepo* repo, char* address, Estate* newEstate);

//find the position of an estate in the repo by its address, return the position if found, -1 otherwise
//int findEstatePositionByAddress(EstateRepo* repo, char* address);

//return a dynamic vector with all the estates in the repo, or NULL if the repo is NULL
DynamicVector* getAllEstatesRepo(EstateRepo* repo);

//copy the repo, return the copy if successful, NULL otherwise
EstateRepo* copyRepo(EstateRepo* repo);