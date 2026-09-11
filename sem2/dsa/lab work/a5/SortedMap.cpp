#include "SMIterator.h"
#include "SortedMap.h"
#include <exception>
using namespace std;


//BC = WC = TC = Theta(n)
void SortedMap::destroyTree(BSTNode* node)
{
	if (node == nullptr)
		return;

	destroyTree(node->left);
	destroyTree(node->right);
	delete node;
}

//BC = WC = TC = Theta(1)
SortedMap::SortedMap(Relation r) : root(nullptr), rel(r), BSTsize(0) {
	//TODO - Implementation
}

//BC = Theta(1) -> the k corresponds to the root
//WC = Theta(n) -> tree is linear and key is a leaf (or does not exist)
//TC = O(n)
TValue SortedMap::add(TKey k, TValue v) {
	//TODO - Implementation
	BSTNode* parent = nullptr;
	BSTNode* current = root;
	bool goLeft = false;

	while (current != nullptr)
	{
		if (current->key == k)
		{
			//key already exists so we simply replace the value
			TValue old = current->value;
			current->value = v;
			return old;
		}
		parent = current;
		if (rel(k, current->key))
		{
			goLeft = true;
			current = current->left;
		}
		else
		{
			goLeft = false;
			current = current->right;
		}
	}

	//if the key is not found
	//we create a new node
	BSTNode* node = new BSTNode(k, v);
	if (parent == nullptr)
	{
		//if the tree was empty
		root = node;
	}
	else if (goLeft == true)
	{
		parent->left = node;
	}
	else
	{
		parent->right = node;
	}
	BSTsize++;
	return NULL_TVALUE;
}

//BC = Theta(1) -> the root has the key k
//WC = Theta(n) -> tree is linear and key is a leaf (or does not exist)
//TC = O(n)
TValue SortedMap::search(TKey k) const {
	//TODO - Implementation

	BSTNode* current = root;
	while (current != nullptr)
	{
		if (current->key == k)
			return current->value;
		if (rel(k, current->key))
			current = current->left;
		else
			current = current->right;
	}

	return NULL_TVALUE;
}


//BC = Theta(1) -> key is at the root and has at most 1 child
//WC = Theta(n) -> tree is linear and key is a leaf (or does not exist)
//TC = O(n)
TValue SortedMap::remove(TKey k) {
	//TODO - Implementation

	BSTNode* parent = nullptr;
	BSTNode* current = root;
	bool goLeft = false;

	//find the node
	while (current != nullptr && current->key != k)
	{
		parent = current;
		if (rel(k, current->key))
		{
			goLeft = true;
			current = current->left;
		}
		else
		{
			goLeft = false;
			current = current->right;
		}
	}

	//if the key was not found
	if (current == nullptr)
		return NULL_TVALUE;

	TValue old = current->value;
	
	//if the node has 2 children
	//we replace it with the leftmost node in the right subtree
	//we need to find its successsor
	if (current->left != nullptr && current->right != nullptr)
	{
		BSTNode* succParent = current;
		BSTNode* succ = current->right;
		while (succ->left != nullptr)
		{
			succParent = succ;
			succ = succ->left;
		}
		//copy the successor info into the current node
		current->key = succ->key;
		current->value = succ->value;

		//delete the successor (it has at most a right child)
		if (succParent == current)   //if the successor is the direct child
			succParent->right = succ->right;
		else
			succParent->left = succ->right;
		delete succ;
	}

	//if the node has 0 or 1 child
	else
	{
		BSTNode* child;
		if (current->left != nullptr)
			child = current->left;
		else
			child = current->right;

		if (parent == nullptr)
			root = child;
		else if (goLeft)
			parent->left = child;
		else
			parent->right = child;
		delete current;
	}

	BSTsize--;
	return old;
}

//BC = WC = TC = Theta(1)
int SortedMap::size() const {
	//TODO - Implementation
	return this->BSTsize;
}

//BC = WC = TC = Theta(1)
bool SortedMap::isEmpty() const {
	//TODO - Implementation
	return this->BSTsize == 0;
}

//BC = WC = TC = Theta(n)
SMIterator SortedMap::iterator() const {
	return SMIterator(*this);
}

//BC = WC = TC = Theta(n)
SortedMap::~SortedMap() {
	//TODO - Implementation
	destroyTree(root);
}