#include "ListIterator.h"
#include "IteratedList.h"
#include <exception>


// BC = WC = TC = Theta(1)
ListIterator::ListIterator(const IteratedList& list) : list(list) {
	//TODO - Implementation
	this->current = list.head;
}

// BC = WC = TC = Theta(1)
void ListIterator::first() {
	//TODO - Implementation
	this->current = list.head;
}

// BC = WC = TC = Theta(1)
void ListIterator::next() {
	//TODO - Implementation
	if (!valid())
		throw std::exception("Invalid iterator!");
	this->current = list.next[this->current];
}

// BC = WC = TC = Theta(1)
bool ListIterator::valid() const {
	//TODO - Implementation
	return this->current != -1;
}

// BC = WC = TC = Theta(1)
TElem ListIterator::getCurrent() const {
	//TODO - Implementation
	if (!valid())
		throw std::exception("Invalid iterator!");
	return list.elems[this->current]; 
}

// BC = WC = TC = Theta(1)
int ListIterator::getPosition()
{
	return this->current;
}

// BC = WC = TC = Theta(1)
void ListIterator::setPosition(int pos)
{
	this->current = pos;
}



