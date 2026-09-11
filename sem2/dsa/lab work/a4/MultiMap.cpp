#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <exception>
#include <iostream>

using namespace std;

//BC = WC = TC = Theta(1)
int MultiMap::hash(TKey key) const
{
	return abs(key) % capacity;
}


//BC = WC = TC = Theta(n), where n = capacity of the hash table
void MultiMap::rehash()
{
	int oldCapacity = capacity;
	//double the capacity
	capacity *= 2;
	//create an empty table
	Node** newTable = new Node * [capacity] {};

	for (int i = 0; i < oldCapacity; i++)
	{
		Node* entry = table[i];
		while (entry != nullptr)
		{
			Node* next = entry->next;
			int index = hash(entry->key);
			entry->next = newTable[index];
			newTable[index] = entry;
			entry = next;
		}
	}

	//free old table and make it point to next one
	delete[] table;
	table = newTable;
}


//BC = WC = TC = Theta(n), where n = capacity of the hash table
MultiMap::MultiMap() : capacity(10), numberOfElements(0)
{
	//TODO - Implementation
	table = new Node* [capacity] {};
	loadFactorThreshold = 0.75;
}


//BC = Theta(1) - no collisions, no rehash
//WC = Theta(n) - all keys in the same entry
//TC = O(n)
void MultiMap::add(TKey c, TValue v) {
	//TODO - Implementation
	if (numberOfElements / capacity > loadFactorThreshold)
		rehash();

	//find the index
	int index = hash(c);
	Node* entry = table[index];

	//look for the node
	while (entry != nullptr && entry->key != c)
	{
		entry = entry->next;
	}

	if (entry == nullptr)
	{
		//we don't have the key
		entry = new Node(c);
		entry->next = table[index];
		table[index] = entry;
	}

	entry->addValue(v);
	numberOfElements++;

	
}


//BC = Theta(1) - only one node in the bucket and only one element 
//WC = Theta(n)
//TC = O(n)
bool MultiMap::remove(TKey c, TValue v) {
	//TODO - Implementation
	int index = hash(c);
	//the node we're currently looking at
	Node* entry = table[index];
	//needed to reset the links
	Node* prev = nullptr;

	while (entry != nullptr)
	{
		if (entry->key == c)
		{
			for (int i = 0; i < entry->valuesCount; i++)
			{
				if (entry->values[i] == v)
				{
					//move one position to the left
					for (int j = i; j < entry->valuesCount-1; j++)
					{
						entry->values[j] = entry->values[j + 1];
					}
					entry->valuesCount--;
					numberOfElements--;

					if (entry->valuesCount == 0)
					{
						//check if we removed the head
						if (prev == nullptr)
						{
							table[index] = entry->next;
						}
						else
						{
							prev->next = entry->next;
						}
						delete entry;
					}
					return true;
				}
			}
		}
		prev = entry;
		entry = entry->next;
	}

	return false;
}


//BC = Theta(1) - nothing in the bucket
//WC = Theta(n) - all the nodes are in the same bucket (n = number of nodes in the table)
//TC = O(n)
vector<TValue> MultiMap::search(TKey c) const {
	//TODO - Implementation
	
	int index = hash(c);
	Node* entry = table[index];

	while (entry != nullptr)
	{
		if (entry->key == c)
		{
			vector<TValue> values(entry->values, entry->values + entry->valuesCount);
			return values;
		}
		entry = entry->next;
	}

	return vector<TValue>();
}


//BC = WC = TC = Theta(1)
int MultiMap::size() const {
	//TODO - Implementation
	return this->numberOfElements;
}

//BC = WC = TC = Theta(1)
bool MultiMap::isEmpty() const {
	//TODO - Implementation
	return this->numberOfElements == 0;
}

//BC = WC = TC = Theta(1)
MultiMapIterator MultiMap::iterator() const {
	return MultiMapIterator(*this);
}

//BC = WC = TC = Theta(n), where n = the capacity of the table
MultiMap::~MultiMap() {
	//TODO - Implementation
	
	for (int i = 0; i < capacity; i++)
	{
		Node* current = table[i];
		while (current != nullptr)
		{
			Node* next = current->next;
			delete current;
			current = next;
		}
	}
	delete[] table;
}


//BC = Theta(1) 
// WC = Theta(n)
// TC = Theta(1) amortized
void MultiMap::Node::addValue(TValue value) {
	if (valuesCount == valuesCapacity) {
		valuesCapacity *= 2;
		TValue* newValues = new TValue[valuesCapacity];
		for (int i = 0; i < valuesCount; i++)
			newValues[i] = values[i];
		delete[] values;
		values = newValues;
	}
	values[valuesCount] = value;
	valuesCount++;
}