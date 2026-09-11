#include<stdio.h>
#include "repository.h"
#include "service.h"
#include "ui.h"
#include "tests.h"
#include <crtdbg.h>
#define _CRTDBG_MAP_ALLOC

void populateInitialData(EstateRepo* repo)
{
	addEstate(repo, createEstate("house", "123 Oak Street, Los Angeles", 250.5, 550000));
	addEstate(repo, createEstate("apartment", "456 Maple Avenue, New York", 250.5, 320000));
	addEstate(repo, createEstate("penthouse", "789 Park Boulevard, Miami", 180.0, 1200000));
	addEstate(repo, createEstate("house", "321 Elm Road, Chicago", 300.0, 450000));
	addEstate(repo, createEstate("apartment", "654 Pine Street, Boston", 75.5, 280000));
	addEstate(repo, createEstate("penthouse", "147 Broadway, San Francisco", 200.0, 1500000));
	addEstate(repo, createEstate("house", "987 Cedar Lane, Seattle", 250.5, 680000));
	addEstate(repo, createEstate("apartment", "258 Market Street, Portland", 90.0, 350000));
	addEstate(repo, createEstate("house", "369 Lake View Drive, Austin", 280.0, 520000));
	addEstate(repo, createEstate("apartment", "741 River Road, Denver", 65.0, 240000));
	addEstate(repo, createEstate("house", "852 Mountain Way, Phoenix", 250.5, 480000));
	addEstate(repo, createEstate("penthouse", "963 Ocean Drive, San Diego", 190.0, 1350000));
}

int main()
{
	test_estate();
	test_dynamic_vector();
	test_repository();
	test_service();
	//printf("All tests passed!");

	//create repo with initial data
	EstateRepo* repo = createRepo();
	populateInitialData(repo);

	//create service
	Service* service = createService(repo);

	//create UI and main function
	UI* ui = createUI(service);
	run(ui);

	//free the memory
	destroyUI(ui);
	destroyService(service);
	destroyRepo(repo);

	//int* p;
	//p = (int*)malloc(sizeof(int) * 10);
	_CrtDumpMemoryLeaks();
	//_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);

	return 0;
}