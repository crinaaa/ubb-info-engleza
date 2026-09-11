#include "MultiMapIterator.h"
#include "MultiMap.h"

//BC = Theta(1)
//WC = Theta(n)
//TC = O(n)
MultiMapIterator::MultiMapIterator(const MultiMap& c): col(c), currentTableIndex(0), currentNode(nullptr),
			currentValueIndex(0)
{
	//TODO - Implementation
	first();
}


//BC = WC = TC = Theta(1)
TElem MultiMapIterator::getCurrent() const{
	//TODO - Implementation
	if (!valid())
		throw std::exception("Invalid iterator!");
	return std::make_pair(currentNode->key, currentNode->values[currentValueIndex]);
}

//BC = WC = TC = Theta(1)
bool MultiMapIterator::valid() const {
	//TODO - Implementation
	return currentNode != nullptr;
}


//BC = Theta(1) - we still have values in the values array
//WC = Theta(n) - the next non-empty bucket is at the very end(or there is not another one) : where n = capacity of the table
//TC = O(n)
void MultiMapIterator::next() {
	//TODO - Implementation

	if (!valid())
		throw std::exception("Invalid iterator!");

	if (currentValueIndex < currentNode->valuesCount - 1)
		currentValueIndex++;
	else
	{
		currentValueIndex = 0;
		currentNode = currentNode->next;
		if (!currentNode)  //no next node in the list, go to the next bucket
		{
			currentTableIndex++;
			while (currentTableIndex < col.capacity && !col.table[currentTableIndex])
				currentTableIndex++;
			if (currentTableIndex < col.capacity)
				currentNode = col.table[currentTableIndex];
			else
				currentNode = nullptr;
		}
	}
}

//BC = Theta(1) : the first position in the table is non-empty
//WC = Theta(n): we have only empty positions, or only the last one is occupied (n = capacity of the table)
//TC = O(n)
void MultiMapIterator::first() {
	//TODO - Implementation

	//walk until we found an non-empty position
	currentTableIndex = 0;
	while (currentTableIndex < col.capacity && !col.table[currentTableIndex]) {
		currentTableIndex++;
	}

	//position the node in that bucket
	if (currentTableIndex < col.capacity) {
		currentNode = col.table[currentTableIndex];
		currentValueIndex = 0;
	}
	else {  //if table is empty
		currentNode = nullptr;
	}
}

