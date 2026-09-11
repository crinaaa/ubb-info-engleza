#include "Bag.h"
#include "BagIterator.h"
#include <exception>
#include <iostream>
using namespace std;


//BC = WC = TC = Theta(elemsSize) - we need to copy all the elements to the new array
void Bag::resizeElems()
{
	TElem* newElems = new TElem[this->elemsCapacity * 2];
	for (int i = 0; i < this->elemsSize; i++)
		newElems[i] = this->elems[i];
	this->elemsCapacity *= 2;
	delete[] this->elems;
	this->elems = newElems;
}

//BC = WC = TC = Theta(bagSize) - we need to copy all the positions to the new array
void Bag::resizePositions()
{
	int* newPositions = new int[this->posCapacity * 2];
	for (int i = 0; i < this->bagSize; i++)
		newPositions[i] = this->positions[i];
	this->posCapacity *= 2;
	delete[] this->positions;
	this->positions = newPositions;
}

//BC = WC = TC = Theta(1)
Bag::Bag() {
	//TODO - Implementation
	this->elemsSize = 0;
	this->elemsCapacity = 10;
	this->elems = new TElem[this->elemsCapacity];

	this->bagSize = 0;
	this->posCapacity = 10;
	this->positions = new int[this->posCapacity];
}


// BC = Theta(1) - element exists in the elems[] and is on the first position
// WC = Theta(bagSize) - element not in the bag and we need to resize both arrays
// Total complexity : O(bagSize)
void Bag::add(TElem elem) {
	//TODO - Implementation

	//look for the element first
	int index = -1;
	for (int i = 0; i < this->elemsSize; i++)
	{
		if (this->elems[i] == elem)
		{
			index = i;
			break;
		}
	}

	//if the element is not in the bag, add it to the end of the elems array
	if (index == -1)
	{
		if (this->elemsSize == this->elemsCapacity)
			this->resizeElems();
		this->elems[this->elemsSize] = elem;
		index = this->elemsSize;
		this->elemsSize++;
	}

	//add the position of the element to the positions array
	if (this->bagSize == this->posCapacity)
		this->resizePositions();
	this->positions[this->bagSize] = index;
	this->bagSize++;
}


//BC - Theta(elemsSize) - the element does not exist in the bag
//WC - Theta(bagSize) - element is the last one in the bag and we need to check all the positions to update the index of the moved element
//TC - O(bagSize)
bool Bag::remove(TElem elem) {
	//TODO - Implementation
	
	//find elem in elems[]
	int index = -1;
	for (int i = 0; i < this->elemsSize; i++)
	{
		if (this->elems[i] == elem)
		{
			index = i;
			break;
		}
	}
	if (index == -1)
		return false;

	//find an appearence of the element in the positions array
	int posSlot = -1;
	for (int i = 0; i < this->bagSize; i++)
	{
		if (this->positions[i] == index)
		{
			posSlot = i;
			break;
		}
	}

	//put the last element from the positions array in the posSlot and decrease the bag size
	this->positions[posSlot] = this->positions[this->bagSize - 1];
	this->bagSize--;


	//check if we removed the last appereance of the element
	bool stillInBag = false;
	for (int i = 0; i < this->bagSize; i++)
	{
		if (this->positions[i] == index)
		{
			stillInBag = true;
			break;
		}
	}

	//if it was indeed the last occurence, remove from elems[] too
	if (!stillInBag)
	{
		int lastElemIndex = this->elemsSize - 1;
		if (index != lastElemIndex)
		{
			this->elems[index] = this->elems[lastElemIndex];
			//update the positions array to point to the new index of the moved element
			for (int i = 0; i < this->bagSize; i++)
			{
				if (this->positions[i] == lastElemIndex)
					this->positions[i] = index;
			}
		}
		this->elemsSize--;
	}

	return true;
}


//BC = Theta(1) - element is on the first position
//WC = Theta(elemsSize) - element is on the last position or not in the bag
//TC = O(elemsSize)
bool Bag::search(TElem elem) const {
	//TODO - Implementation
	for (int i = 0; i < this->elemsSize; i++)
	{
		if(this->elems[i] == elem)
			return true;
	}
	return false;
}


//BC = WC = TC = Theta(bagSize) - we need to check all the positions
int Bag::nrOccurrences(TElem elem) const {
	//TODO - Implementation
	int counter = 0;
	for (int i = 0; i < this->bagSize; i++)
	{
		if (this->elems[this->positions[i]] == elem)
			counter++;
	}
	return counter;
}


//BC = WC = TC = Theta(1)
int Bag::size() const {
	//TODO - Implementation
	return this->bagSize;
}


//BC = WC = TC = Theta(1)
bool Bag::isEmpty() const {
	//TODO - Implementation
	return this->bagSize == 0;
}


//BC = WC = TC = Theta(1)
BagIterator Bag::iterator() const {
	return BagIterator(*this);
}


//BC = WC = TC = Theta(1)
Bag::~Bag() {
	//TODO - Implementation
	delete[] this->elems;
	delete[] this->positions;
}


//BC = WC = TC = Theta(bagSize)
Bag::Bag(const Bag& other)
{
	this->elemsSize = other.elemsSize;
	this->elemsCapacity = other.elemsCapacity;
	this->elems = new TElem[this->elemsCapacity];
	for (int i = 0; i < this->elemsSize; i++)
		this->elems[i] = other.elems[i];

	this->bagSize = other.bagSize;
	this->posCapacity = other.posCapacity;
	this->positions = new int[this->posCapacity];
	for (int i = 0; i < this->bagSize; i++)
		this->positions[i] = other.positions[i];
}


//BC = WC = TC = Theta(bagSize)
Bag& Bag::operator=(const Bag& other)
{
	// TODO: insert return statement here
	if (this == &other)
		return *this;

	delete[] this->elems;
	delete[] this->positions;

	this->elemsSize = other.elemsSize;
	this->elemsCapacity = other.elemsCapacity;
	this->elems = new TElem[this->elemsCapacity];
	for (int i = 0; i < this->elemsSize; i++)
		this->elems[i] = other.elems[i];

	this->bagSize = other.bagSize;
	this->posCapacity = other.posCapacity;
	this->positions = new int[this->posCapacity];
	for (int i = 0; i < this->bagSize; i++)
		this->positions[i] = other.positions[i];

	return *this;
}
