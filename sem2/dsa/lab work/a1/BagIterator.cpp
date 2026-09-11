#include <exception>
#include "BagIterator.h"
#include "Bag.h"

using namespace std;


BagIterator::BagIterator(const Bag& c): bag(c)
{
	//TODO - Implementation
	this->currentIndex = 0;
}
//BC = WC = TC = Theta(1)


void BagIterator::first() {
	//TODO - Implementation
	this->currentIndex = 0;
}
//BC = WC = TC = Theta(1)



void BagIterator::next() {
	//TODO - Implementation
	if (!this->valid())
		throw exception();
	this->currentIndex++;
}
//BC = WC = TC = Theta(1)



bool BagIterator::valid() const {
	//TODO - Implementation
	return this->currentIndex < this->bag.bagSize;
}
//BC = WC = TC = Theta(1)



TElem BagIterator::getCurrent() const
{
	//TODO - Implementation
	if (!this->valid())
		throw exception();
	return this->bag.elems[this->bag.positions[this->currentIndex]];
}
//BC = WC = TC = Theta(1)
