#pragma once
#include"service.h"

typedef struct
{
	Service* service;
}UI;

UI* createUI(Service* service);
void destroyUI(UI* ui);
void run(UI* ui);

void printMenu();

void addEstateUI(UI* ui);
void deleteEstateUI(UI* ui);
void updateEstateUI(UI* ui);

void displayAllEstatesUI(UI* ui);
void displayEstatesByTypeAndSurfaceUI(UI* ui);
void displayEstatesByAddressSubstringUI(UI* ui);

void displayEstatesByTypeSortedByAddressUI(UI* ui);

//req for today
void displayEstatesBySurfaceSortedByPriceUI(UI* ui);

void undoUI(UI* ui);
void redoUI(UI* ui);