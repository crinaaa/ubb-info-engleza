#pragma once
#include "TrenchCoat.h"
#include <stdexcept>

template <typename T>
class DynamicVector
{
private:
	T* data;
	int capacity;
	int size;
	void resize();
public:
	//constructor
	DynamicVector();
	//destructor
	~DynamicVector();
	//copy constructor
	DynamicVector(const DynamicVector& other);
	//assignment operator
	DynamicVector& operator=(const DynamicVector& other);

	//add an element to the end of the vector
	void add(const T& coat);
	//remove an element from a specific index
	void remove(int index);
	//update an element on a specific index
	void update(int index, const T& coat);

	//get the number of elements in the vector
	int getLength() const;
	//get the element at a specific index
	T& get(int index) const;
};


template<typename T>
inline void DynamicVector<T>::resize()
{
	this->capacity *= 2;
	TrenchCoat* newData = new TrenchCoat[this->capacity];
	for (int i = 0; i < this->size; i++)
		newData[i] = this->data[i];
	delete[] this->data;
	this->data = newData;
}

template<typename T>
inline DynamicVector<T>::DynamicVector()
{
	this->capacity = 10;
	this->size = 0;
	this->data = new T[this->capacity];
}

template<typename T>
inline DynamicVector<T>::~DynamicVector()
{
	delete[] this->data;
}

template<typename T>
inline DynamicVector<T>::DynamicVector(const DynamicVector& other)
{
	this->capacity = other.capacity;
	this->size = other.size;
	this->data = new T[this->capacity];
	for (int i = 0; i < other.size; i++)
		this->data[i] = other.data[i];
}

template<typename T>
inline DynamicVector<T> &DynamicVector<T>::operator= (const DynamicVector& other)
{
	if (this == &other)
		return* this;

	this->capacity = other.capacity;
	this->size = other.size;
	delete[] this->data;
	this->data = new T[this->capacity];
	for (int i = 0; i < other.size; i++)
		this->data[i] = other.data[i];
	return *this;
}

template<typename T>
inline void DynamicVector<T>::add(const T& coat)
{
	if (this->size == this->capacity)
		resize();
	this->data[this->size++] = coat;
}

template<typename T>
inline void DynamicVector<T>::remove(int index)
{
	if (index < 0 || index >= this->size)
		throw std::invalid_argument("Invalid position!");
	for (int i = index; i < this->size - 1; i++)
		this->data[i] = this->data[i + 1];
	this->size--;
}

template<typename T>
inline void DynamicVector<T>::update(int index, const T& coat)
{
	if (index < 0 || index >= this->size)
		throw std::invalid_argument("Invalid position!");
	this->data[index] = coat;
}

template<typename T>
inline int DynamicVector<T>::getLength() const
{
	return this->size;
}

template<typename T>
inline T& DynamicVector<T>::get(int index) const
{
	if (index < 0 || index >= this->size)
		throw std::invalid_argument("Invalid position!");
	return this->data[index];
}
