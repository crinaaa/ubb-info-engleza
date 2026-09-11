#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <exception>
#include <iostream>

using namespace std;

//BC = WC = Total complexity =  Theta(1)
MultiMap::MultiMap() {
	//TODO - Implementation
	this->head = nullptr;
	this->length = 0; 
}


//BC = WC = Total complexity =  Theta(1)
void MultiMap::add(TKey c, TValue v) {
	//TODO - Implementation
	Node* newNode = new Node;
	newNode->elem.first = c;
	newNode->elem.second = v;
	newNode->next = this->head;
	this->head = newNode;
	this->length++;
}


//BC = Theta(1), when we find the pair on the first position
//WC = Theta(n), when the pair is on the last position/does not exist (where n is the length of the SLL)
//Total Complexity = O(n), where n is the length of the SLL
bool MultiMap::remove(TKey c, TValue v) {
	//TODO - Implementation
	Node* current = this->head;
	Node* previous = nullptr;

	while (current != nullptr)
	{
		if (current->elem.first == c && current->elem.second == v)
		{
			//the case where the element is on the first position => we delete the head
			if (previous == nullptr)
				this->head = current->next;

			//if the element is after the head
			else
				previous->next = current->next;

			delete current;
			this->length--;
			return true;
		}

		//move forward in the list
		previous = current;
		current = current->next;
	}
	return false;
}


//BC = WC = Total Complexity = Theta(n), where n = length of the SLL
vector<TValue> MultiMap::search(TKey c) const {
	//TODO - Implementation
	vector<TValue> foundValues;
	Node* current = this->head;
	while (current != nullptr)
	{
		if (current->elem.first == c)
			foundValues.push_back(current->elem.second);

		current = current->next;
	}
	return foundValues;
}


//BC = WC = Total complexity =  Theta(1)
int MultiMap::size() const {
	//TODO - Implementation
	return this->length;
}


//BC = WC = Total complexity =  Theta(1)
bool MultiMap::isEmpty() const {
	//TODO - Implementation
	return this->length == 0;
}


//BC = WC = Total complexity =  Theta(1)
MultiMapIterator MultiMap::iterator() const {
	return MultiMapIterator(*this);
}


//BC = WC = Total Complexity = Theta(n), where n = length of the SLL
MultiMap::~MultiMap() {
	//TODO - Implementation
	Node* current = this->head;
	while (current != nullptr)
	{
		Node* next = current->next;
		delete current;
		current = next;
	}
}

