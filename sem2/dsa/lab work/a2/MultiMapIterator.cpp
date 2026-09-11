#include "MultiMapIterator.h"
#include "MultiMap.h"
#include <stdexcept>


//BC = WC = Total complexity =  Theta(1)
MultiMapIterator::MultiMapIterator(const MultiMap& c): col(c) {
	//TODO - Implementation
	this->current = col.head;
}


//BC = WC = Total complexity =  Theta(1)
TElem MultiMapIterator::getCurrent() const{
	//TODO - Implementation
	if (!valid())
		throw exception();
	return this->current->elem;
}


//BC = WC = Total complexity =  Theta(1)
bool MultiMapIterator::valid() const {
	//TODO - Implementation
	return this->current != nullptr;
}


//BC = WC = Total complexity =  Theta(1)
void MultiMapIterator::next() {
	//TODO - Implementation
	if (!valid())
		throw exception();
	this->current = this->current->next;
}


//BC = WC = Total complexity =  Theta(1)
void MultiMapIterator::first() {
	//TODO - Implementation
	this->current = col.head;
}

