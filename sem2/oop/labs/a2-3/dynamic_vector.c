#include<stdlib.h>
#include<stdio.h>
#include "dynamic_vector.h"

DynamicVector* createDynamicVector(int capacity, DestroyElementFunctionPointer destroyPointer)
{
	DynamicVector* v = (DynamicVector*)malloc(sizeof(DynamicVector));

	if (!v)
		return NULL;

	v->capacity = capacity;
	v->length = 0;
	v->destroyPointer = destroyPointer;

	v->elements = (TElem*)malloc(sizeof(TElem) * v->capacity);

	if (!v->elements)
	{
		free(v);
		return NULL;
	}

	return v;
}

void destroyDynamicVector(DynamicVector* v)
{
	if (!v)
		return;

	for (int i = 0; i < v->length; i++)
		if (v->destroyPointer)
			v->destroyPointer(v->elements[i]);

	free(v->elements);
	free(v);
}

//getters
int getLength(DynamicVector* v)
{
	return v->length;
}

int getCapacity(DynamicVector* v)
{
	return v->capacity;
}


//resize the vector by doubling its capacity
void resize(DynamicVector* v)
{
	v->capacity *= 2;
	TElem* newElements = (TElem*)realloc(v->elements, sizeof(TElem) * v->capacity);

	if (!newElements)
		return;

	v->elements = newElements;
}


void addElement(DynamicVector* v, TElem elem)
{
	if (v->length == v->capacity)
		resize(v);
	v->elements[v->length++] = elem;
}

void deleteElement(DynamicVector* v, int position)
{
	if (position < 0 || position >= v->length)
		return;

	//destroy old element
	if (v->destroyPointer)
		v->destroyPointer(v->elements[position]);

	//shift the elements to the left
	for (int i = position; i < v->length - 1; i++)
		v->elements[i] = v->elements[i + 1];

	v->length--;
}

void updateElement(DynamicVector* v, int position, TElem newElem)
{
	if (position < 0 || position >= v->length)
		return;

	//destroy old element
	if (v->destroyPointer)
		v->destroyPointer(v->elements[position]);

	//place the new element on the given position
	v->elements[position] = newElem;
}

//getter for the element on a given position
TElem getElement(DynamicVector* v, int position)
{
	if (position < 0 || position >= v->length)
		return;

	return v->elements[position];
}

DynamicVector* copyDynamicVector(DynamicVector* v, TElem(*copyDestroyPointer)(TElem))
{
	if (!v)
		return NULL;

	DynamicVector* newV = createDynamicVector(v->capacity, v->destroyPointer);
	if (!newV)
		return NULL;

	for (int i = 0; i < v->length; i++)
	{
		TElem copied = copyDestroyPointer(v->elements[i]);
		addElement(newV, copied);
	}

	return newV;
}
