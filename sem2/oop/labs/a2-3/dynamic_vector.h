#pragma once
#include"estate.h"

typedef void* TElem;
typedef void (*DestroyElementFunctionPointer)(TElem);

typedef struct
{
	TElem* elements;
	int length, capacity;
	DestroyElementFunctionPointer destroyPointer;
}DynamicVector;

//create a dynamic vector with given initial capacity and a pointer to a function that can destroy the elements (or NULL if not needed)
DynamicVector* createDynamicVector(int capacity, DestroyElementFunctionPointer destroyPointer);

//destructor
void destroyDynamicVector(DynamicVector* v);

//getters
int getLength(DynamicVector* v);
int getCapacity(DynamicVector* v);

//void resize(DynamicVector* v);

//add an element to the end of the vector
void addElement(DynamicVector* v, TElem elem);

//delete the element on the given position
void deleteElement(DynamicVector* v, int position);

//update the element on the given position with a new element
void updateElement(DynamicVector* v, int position, TElem newElem);

//return the element on the given position
TElem getElement(DynamicVector* v, int position); 

//copy the vector
DynamicVector* copyDynamicVector(DynamicVector* v, TElem (*copyDestroyPointer)(TElem));