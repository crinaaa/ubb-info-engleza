//#include "DynamicVector.h"
//#include <stdexcept>
//
//void DynamicVector::resize()
//{
//	this->capacity *= 2;
//	TrenchCoat* newData = new TrenchCoat[this->capacity];
//	for (int i=0;i<this->size;i++)
//		newData[i] = this->data[i];
//	delete[] this->data;
//	this->data = newData;
//}
//
//DynamicVector::DynamicVector()
//{
//	this->data = new TrenchCoat[10];
//	this->capacity = 10;
//	this->size = 0;
//}
//
//DynamicVector::DynamicVector(const DynamicVector& other)
//{
//	this->capacity = other.capacity;
//	this->size = other.size;
//	this->data = new TrenchCoat[other.capacity];
//
//	for (int i = 0; i < this->size; i++)
//		this->data[i] = other.data[i];
//}
//
//DynamicVector& DynamicVector::operator=(const DynamicVector& other)
//{
//	if (this == &other)
//		return *this;
//
//	delete[] this->data;
//	this->capacity = other.capacity;
//	this->size = other.size;
//	this->data = new TrenchCoat[capacity];
//	for (int i = 0; i < this->size; i++)
//		this->data[i] = other.data[i];
//	return *this;
//}
//
//DynamicVector::~DynamicVector()
//{
//	delete[] this->data;
//}
//
//void DynamicVector::add(const TrenchCoat& coat)
//{
//	if (this->capacity == this->size)
//		this->resize();
//	this->data[this->size++] = coat;
//}
//
//void DynamicVector::remove(int index)
//{
//	if (index < 0 || index >= this->size)
//		throw std::invalid_argument("Index out of bounds.");
//
//	for (int i = index; i < this->size - 1; i++)
//		this->data[i] = this->data[i + 1];
//	this->size--;
//}
//
//void DynamicVector::update(int index, const TrenchCoat& coat)
//{
//	if (index < 0 || index >= this->size)
//		throw std::invalid_argument("Index out of bounds.");
//	this->data[index] = coat;
//}
//
//TrenchCoat& DynamicVector::get(int index) const
//{
//	if (index< 0 || index>= this->size)
//		throw std::invalid_argument("Index out of bounds.");
//	return this->data[index];
//}
//
////v=v+e
////DynamicVector DynamicVector::operator+(const TrenchCoat& coat) const
////{
////	DynamicVector result(*this);
////	result.add(coat);
////	return result;
////}
//
////v=e+v
////DynamicVector operator+(const TrenchCoat& coat, const DynamicVector& vec)
////{
////	DynamicVector result(vec);
////	result.add(coat);
////	return result;
////}