#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "estate.h"
#include "dynamic_vector.h"
#include "repository.h"
#include "service.h"
#include "tests.h"


void test_estate(void)
{
    Estate* e = createEstate("house", "1 Test St", 42.5, 1234.0);
    assert(e != NULL);
    assert(strcmp(getTypeOfEstate(e), "house") == 0);
    assert(strcmp(getAddressOfEstate(e), "1 Test St") == 0);
    assert(getSurfaceOfEstate(e) == 42.5);
    assert(getPriceOfEstate(e) == 1234.0);

    Estate* c = copyEstate(e);
    assert(c != NULL);
    assert(strcmp(getAddressOfEstate(c), getAddressOfEstate(e)) == 0);

    destroyEstate(e);
    destroyEstate(c);
}

void test_dynamic_vector(void)
{
    DynamicVector* dv = createDynamicVector(2, (DestroyElementFunctionPointer)destroyEstate);
    assert(dv != NULL);
    assert(getLength(dv) == 0);

    Estate* a = createEstate("house", "A", 10, 100);
    Estate* b = createEstate("apartment", "B", 20, 200);
    addElement(dv, a);
    addElement(dv, b);
    assert(getLength(dv) == 2);

    Estate* ra = (Estate*)getElement(dv, 0);
    Estate* rb = (Estate*)getElement(dv, 1);
    assert(strcmp(getAddressOfEstate(ra), "A") == 0);
    assert(strcmp(getAddressOfEstate(rb), "B") == 0);


    Estate* b2 = createEstate("apartment", "B2", 21, 210);
    updateElement(dv, 1, b2);
    assert(strcmp(getAddressOfEstate((Estate*)getElement(dv, 1)), "B2") == 0);

    deleteElement(dv, 0);
    assert(getLength(dv) == 1);
    assert(strcmp(getAddressOfEstate((Estate*)getElement(dv, 0)), "B2") == 0);

    destroyDynamicVector(dv); 
}

void test_repository(void)
{
    EstateRepo* repo = createRepo();
    assert(repo != NULL);
    assert(getLength(repo->estates) == 0);

    Estate* e1 = createEstate("house", "addr1", 11, 111);
    Estate* e2 = createEstate("apartment", "addr2", 22, 222);
    assert(addEstate(repo, e1) == 1);
    assert(addEstate(repo, e2) == 1);
    assert(getLength(repo->estates) == 2);

    int pos = findEstatePositionByAddress(repo, "addr2");
    assert(pos == 1);

    Estate* e1new = createEstate("penthouse", "addr1", 111, 1111);
    assert(updateEstate(repo, "addr1", e1new) == 1);
    Estate* check = (Estate*)getElement(repo->estates, 0);
    assert(strcmp(getTypeOfEstate(check), "penthouse") == 0);

    assert(deleteEstate(repo, "addr2") == 1);
    assert(getLength(repo->estates) == 1);

    EstateRepo* repo_copy = copyRepo(repo);
    assert(repo_copy != NULL);
    assert(getLength(repo_copy->estates) == getLength(repo->estates));

    destroyRepo(repo);
    destroyRepo(repo_copy);
}

void test_service(void)
{
    EstateRepo* repo = createRepo();
    assert(repo != NULL);

    Service* s = createService(repo);
    assert(s != NULL);

    assert(serviceAddEstate(s, "house", "Saddr", 12.0, 120.0) == 1);
    DynamicVector* all = getAllEstatesService(s);
    assert(getLength(all) == 1);
    destroyDynamicVector(all);

    assert(serviceUndo(s) == 1);
    all = getAllEstatesService(s);
    assert(getLength(all) == 0);
    destroyDynamicVector(all);

    assert(serviceRedo(s) == 1);
    all = getAllEstatesService(s);
    assert(getLength(all) == 1);
    destroyDynamicVector(all);

    destroyService(s);
    destroyRepo(repo);
}

//int main(void)
//{
//    puts("Running minimal tests (assert-based)...");
//    test_estate();
//    test_dynamic_vector();
//    test_repository();
//    test_service();
//    puts("All tests passed.");
//    return 0;
//}