
#include <exception>
#include "ListIterator.h"
#include "IteratedList.h"

//helper functions

//BC = WC = TC = Theta(n), where n = the capacity of the SLLA
void IteratedList::resize()
{
	int newCapacity = this->capacity * 2;
	TElem* newElements = new TElem[newCapacity];
	int* newNext = new int[newCapacity];

	for (int i = 0; i < this->capacity; i++)
	{
		newElements[i] = this->elems[i];
		newNext[i] = this->next[i];
	}

	for (int i = this->capacity; i < newCapacity; i++)
		newNext[i] = i + 1;
	newNext[newCapacity - 1] = -1;

	if (this->firstEmpty == -1)
		this->firstEmpty = capacity;

	delete[] this->elems;
	delete[] this->next;

	this->elems = newElements;
	this->next = newNext;
	capacity = newCapacity;
}

// BC = Theta(1)
// WC = Theta(n)
// TC = Theta(1) amortized
int IteratedList::allocate()
{
	if (this->firstEmpty == -1)
		resize();

	int position = this->firstEmpty;
	this->firstEmpty = this->next[this->firstEmpty];
	return position;
}


// BC = WC = TC = Theta(n), where n = the capacity of the SLLA
IteratedList::IteratedList() {
	//TODO - Implementation
	this->head = -1;
	this->capacity = 10;
	this->listSize = 0;
	this->elems = new TElem[this->capacity];
	this->next = new int[this->capacity];

	for (int i = 0; i < this->capacity - 1; i++)
		this->next[i] = i + 1;

	this->next[this->capacity - 1] = -1;
	this->firstEmpty = 0;
}

// BC = WC = TC = Theta(1)
int IteratedList::size() const {
	//TODO - Implementation
	return this->listSize;
}


// BC = WC = TC = Theta(1)
bool IteratedList::isEmpty() const {
	//TODO -  Implementation
	return this->listSize == 0;
}

// BC = WC = TC = Theta(1)
ListIterator IteratedList::first() const {
	return ListIterator(*this);
}

// BC = WC = TC = Theta(1)
TElem IteratedList::getElement(ListIterator pos) const {
	//TODO - Implementation

	//throw exception if position not valid
	if (!pos.valid())
		throw std::exception("Invalid iterator position!");
	//return the wanted element
	return this->elems[pos.getPosition()];
}



// BC = Theta(1) - the removed element was the first one
// WC = Theta(n) - the removed element was the last one
// TC = O(n)
TElem IteratedList::remove(ListIterator& pos) {
	//TODO - Implementation
	
	//throw exception if position not valid
	if (!pos.valid())
		throw std::exception("Invalid iterator position!");

	int currentPosition = pos.getPosition();
	TElem removedElement = this->elems[currentPosition];

	int prev = -1;
	int current = this->head;
	// go with the loop as long as we didn't reach the wanted element or reached the end of the slla
	//look for the node before the one we remove
	while (current != currentPosition && current != -1)
	{
		prev = current;
		current = this->next[current];
	}

	//set the new links
	if (prev == -1)    //if the removed node is the head
		this->head = this->next[currentPosition];
	//otherwise
	else
		this->next[prev] = this->next[currentPosition];

	int nextPsition = this->next[currentPosition];

	//free the space
	this->next[currentPosition] = this->firstEmpty;
	this->firstEmpty = currentPosition;
	this->listSize--;

	//iterator goes to the element immediately after the removed one
	pos.setPosition(nextPsition);

	return removedElement;
}


// BC = Theta(1) : the element we're looking for is the head
// Wc = Theta(n), where n = the number of elements in the list : the element we're looking for is on the last position
//																 or does not exist in the list
// TC = O(n)
ListIterator IteratedList::search(TElem e) const {
	//TODO - Implementation

	int current = this->head;
	while (current != -1) {
		if (this->elems[current] == e) {
			ListIterator it(*this);
			it.setPosition(current);
			return it;  //return valid iterator
		}
		current = this->next[current];
	}
	ListIterator it(*this);
	it.setPosition(-1);  // element not found, set invalid position and we will return an invalid iterator
	return it;
}


// BC = WC = TC = Theta(1)
TElem IteratedList::setElement(ListIterator pos, TElem e) {
    //TODO - Implementation

	//throw exception if position not valid
	if (!pos.valid())
		throw std::exception("Invalid iterator position!");

	//update the element
	int currentPos = pos.getPosition();
	TElem oldElement = this->elems[currentPos];
	this->elems[currentPos] = e;
	
	//return the old element
	return oldElement;
}


// BC = WC = TC = Theta(1)
void IteratedList::addToPosition(ListIterator& pos, TElem e) {
    //TODO - Implementation

	//throw exception if position not valid
	if (!pos.valid())
		throw std::exception("Invalid iterator position!");

	int newPosition = allocate();
	int currentPosition = pos.getPosition();

	this->elems[newPosition] = e;
	this->next[newPosition] = this->next[currentPosition];
	this->next[currentPosition] = newPosition;

	this->listSize++;

	pos.setPosition(newPosition);
}


// BC = Theta(1) : if the list is empty
// WC = Theta(n), where n = the number of elements in the list
// TC = O(n)
void IteratedList::addToEnd(TElem e) {
	int newPosition = allocate();
	elems[newPosition] = e;
	this->next[newPosition] = -1;

	if (this->head == -1)
		this->head = newPosition;
	else {
		// find last node and link it
		int current = this->head;
		while (this->next[current] != -1)
			current = this->next[current];
		this->next[current] = newPosition;  // link last node to new node
	}
	this->listSize++;
}


// BC = Theta(1)
// WC = Theta(1)
// TC = Theta(1)
void IteratedList::addToBeginning(TElem e)
{
	int newPosition = allocate();
	this->elems[newPosition] = e;
	this->next[newPosition] = this->head;

	this->head = newPosition;

	this->listSize++;
}


// BC = WC = TC = Theta(1)
IteratedList::~IteratedList() {
	//TODO - Implementation
	delete[] this->elems;
	delete[] this->next;
}
