#include "SMIterator.h"
#include "SortedMap.h"
#include <exception>

using namespace std;


//BC = WC = TC = Theta(n)
SMIterator::SMIterator(const SortedMap& m): map(m), currentIndex(0), totalSize(m.BSTsize) {
	//TODO - Implementation
	elems = new TElem[totalSize];
	int index = 0;
	inorder(map.root, index);
}


//BC = WC = TC = Theta(n)
void SMIterator::inorder(const SortedMap::BSTNode* node, int& index)  //left, root, right
{
	if (node == nullptr)
		return;

	inorder(node->left, index);  //go left first
	elems[index++] = TElem(node->key, node->value);  //store the current value
	inorder(node->right, index);  //go right
}

//BC = WC = TC = Theta(1)
void SMIterator::first(){
	//TODO - Implementation
	currentIndex = 0;
}

//BC = WC = TC = Theta(1)
void SMIterator::next(){
	//TODO - Implementation
	if (!valid())
		throw exception();
	currentIndex++;
}

//BC = WC = TC = Theta(1)
bool SMIterator::valid() const{
	//TODO - Implementation
	return currentIndex < totalSize;
}

//BC = WC = TC = Theta(1)
TElem SMIterator::getCurrent() const{
	//TODO - Implementation
	if (!valid())
		throw exception();
	return elems[currentIndex];
}

//BC = WC = TC = Theta(1)
SMIterator::~SMIterator() {
	delete[] elems;
}