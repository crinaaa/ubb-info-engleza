#pragma once
#include "SortedMap.h"

//DO NOT CHANGE THIS PART
class SMIterator{
	friend class SortedMap;
private:
	const SortedMap& map;
	SMIterator(const SortedMap& mapionar);

	//TODO - Representation
	TElem* elems;      // array of all (key,value) pairs in sorted order
	int currentIndex;  // current position in the array of elems
	int totalSize;     // total number of elements

	void inorder(const SortedMap::BSTNode* node, int& index);

public:
	void first();
	void next();
	bool valid() const;
    TElem getCurrent() const;
	~SMIterator();
};

