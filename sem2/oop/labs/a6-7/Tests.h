#pragma once
#include "TrenchCoat.h"
#include "Repository.h"
#include "Service.h"

class Tests
{
private:
	void testDomain();
	void testRepository();
	void testService();
public:
	void test_all();
};