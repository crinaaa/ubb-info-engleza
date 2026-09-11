#include "ui.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//helper for parsing the lines
int readLine(const char* prompt, char* buffer, size_t size)
{
	if (prompt) printf("%s", prompt);
	if (!fgets(buffer, (int)size, stdin)) return 0;
	size_t len = strlen(buffer);
	if (len > 0 && buffer[len - 1] == '\n') buffer[len - 1] = '\0';
	return 1;
}

//transform a string to lowercase
void toLowerStr(char* s)
{
	for (; *s; ++s)
		if (*s >= 'A' && *s <= 'Z') 
			*s = (char)(*s - 'A' + 'a');
}

int isValidType(const char* type)
{
	return (strcmp(type, "house") == 0 ||
		strcmp(type, "apartment") == 0 ||
		strcmp(type, "penthouse") == 0);
}

void printAllowedTypes(void)
{
	printf("Allowed types: house, apartment, penthouse (case-insensitive).\n");
}

UI* createUI(Service* service)
{
	UI* ui = (UI*)malloc(sizeof(UI));
	if (!ui) return NULL;
	ui->service = service;
	return ui;
}

void destroyUI(UI* ui)
{
	if (ui) free(ui);
}

void printEstate(Estate* estate)
{
	if (!estate) return;
	printf("Type: %s | Address: %s | Surface: %8.2f sqm | Price: $%.2f\n",
		getTypeOfEstate(estate), getAddressOfEstate(estate),
		getSurfaceOfEstate(estate), getPriceOfEstate(estate));
}


void addEstateUI(UI* ui)
{
	char type[50], address[200], buf[128];
	double surface, price;

	if (!readLine("\nEnter estate type (house/apartment/penthouse): ", type, sizeof(type))) 
		{ printf("Input error!\n"); 
		return; }
	toLowerStr(type);

	if (type[0] == '\0' || !isValidType(type)) 
		{ printf("Invalid estate type. "); 
		printAllowedTypes(); 
		return; }

	if (!readLine("\nEnter the address: ", address, sizeof(address))) 
		{ printf("Input error!\n"); 
		return; }

	if (address[0] == '\0') 
		{ printf("Address cannot be empty.\n"); 
		return; }

	if (!readLine("Enter the surface (square meters): ", buf, sizeof(buf))) 
		{ printf("Input error!\n"); 
		return; }

	surface = atof(buf);

	if (surface <= 0.0) 
		{ printf("Surface must be a positive number.\n"); 
		return; }

	if (!readLine("Enter the price: ", buf, sizeof(buf)))
		{ printf("Input error!\n");
		return; }

	price = atof(buf);

	if (price <= 0.0) 
		{ printf("Price must be a positive number.\n");
		return; }

	if (serviceAddEstate(ui->service, type, address, surface, price))
		printf("Estate added successfully!\n");
	else
		printf("Could not add estate.\n");
}

void deleteEstateUI(UI* ui)
{
	char address[200];
	if (!readLine("Enter the address of the estate you wish to delete: ", address, sizeof(address))) { printf("Input error!\n"); return; }
	if (address[0] == '\0') { printf("Address cannot be empty.\n"); return; }
	if (serviceDeleteEstate(ui->service, address)) printf("Estate deleted successfully.\n"); else printf("Estate not found.\n");
}

void updateEstateUI(UI* ui)
{
	char address[200], newType[50], buf[128];
	double newSurface, newPrice;

	if (!readLine("\nEnter the address of the estate you wish to update: ", address, sizeof(address))) 
		{ printf("Input error!\n"); 
		return; }

	if (address[0] == '\0')
		{ printf("Address cannot be empty.\n");
		return; }

	if (!readLine("\nEnter the new type of the estate (house/apartment/penthouse): ", newType, sizeof(newType)))
		{ printf("Input error!\n");
		return; }

	toLowerStr(newType);
	if (newType[0] == '\0' || !isValidType(newType))
		{ printf("Invalid estate type. "); 
		printAllowedTypes(); 
		return; }

	if (!readLine("Enter the new surface (square meters): ", buf, sizeof(buf)))
		{ printf("Input error!\n"); 
		return; }

	newSurface = atof(buf);

	if (newSurface <= 0.0) 
		{ printf("Surface must be a positive number.\n");
		return; }

	if (!readLine("Enter the new price: ", buf, sizeof(buf)))
		{ printf("Input error!\n");
		return; }
	newPrice = atof(buf);

	if (newPrice <= 0.0)
		{ printf("Price must be a positive number.\n");
		return; }

	if (serviceUpdateEstate(ui->service, address, newType, newSurface, newPrice))
		printf("Estate updated successfully!\n");
	else
		printf("Could not update estate.\n");
}

void displayAllEstatesUI(UI* ui)
{
	DynamicVector* estates = getAllEstatesService(ui->service);
	if (getLength(estates) == 0) { printf("No estates in the system!\n"); destroyDynamicVector(estates); return; }
	for (int i = 0; i < getLength(estates); ++i)
	{
		Estate* estate = (Estate*)getElement(estates, i);
		printf("%d.", i + 1);
		printEstate(estate);
	}
	destroyDynamicVector(estates);
}

void displayEstatesByTypeAndSurfaceUI(UI* ui)
{
	char type[50], buf[128];
	double surface;

	if (!readLine("\nEnter the type of the estate (house/apartment/penthouse): ", type, sizeof(type))) { printf("Input error!\n"); return; }
	toLowerStr(type);
	if (type[0] == '\0' || !isValidType(type)) { printf("Invalid estate type. "); printAllowedTypes(); return; }

	if (!readLine("Enter the minimum surface (square meters): ", buf, sizeof(buf))) { printf("Input error!\n"); return; }
	surface = atof(buf);
	if (surface < 0.0) { printf("Minimum surface must be a non-negative number.\n"); return; }

	DynamicVector* estates = getEstatesByTypeAndSurfaceService(ui->service, type, surface);
	if (getLength(estates) == 0) printf("No estates match the criteria!\n");
	else for (int i = 0; i < getLength(estates); ++i) { Estate* e = (Estate*)getElement(estates, i); printf("%d.", i + 1); printEstate(e); }
	destroyDynamicVector(estates);
}

void displayEstatesByTypeSortedByAddressUI(UI* ui)
{
	char type[50];
	if (!readLine("\nEnter the type of the estate to list (house/apartment/penthouse): ", type, sizeof(type))) { printf("Input error!\n"); return; }
	toLowerStr(type);
	if (type[0] == '\0' || !isValidType(type)) { printf("Invalid estate type. "); printAllowedTypes(); return; }

	DynamicVector* estates = getEstatesByTypeSortedByAddressService(ui->service, type);
	if (!estates) { printf("An error occurred while retrieving estates.\n"); return; }
	if (getLength(estates) == 0) printf("No estates of type '%s' found.\n", type);
	else for (int i = 0; i < getLength(estates); ++i) { Estate* e = (Estate*)getElement(estates, i); printf("%d.", i + 1); printEstate(e); }
	destroyDynamicVector(estates);
}

void displayEstatesByAddressSubstringUI(UI* ui)
{
	char substring[200];
	if (!readLine("\nEnter the substring to search for in addresses (empty = all): ", substring, sizeof(substring))) return;
	DynamicVector* estates = getEstatesByAddressSubstringService(ui->service, substring);
	if (getLength(estates) == 0) printf("No estates match the criteria!\n");
	else for (int i = 0; i < getLength(estates); ++i) { Estate* e = (Estate*)getElement(estates, i); printf("%d.", i + 1); printEstate(e); }
	destroyDynamicVector(estates);
}

void displayEstatesBySurfaceSortedByPriceUI(UI* ui)
{
	char buf[128];
	double surface;
	if (!readLine("\nEnter the surface (square meters): ", buf, sizeof(buf))) { printf("Input error!\n"); return; }
	surface = atof(buf);
	if (surface < 0.0) { printf("Minimum surface must be a non-negative number.\n"); return; }
	DynamicVector* estates = getEstatesBySurfaceSortedByPriceService(ui->service, surface);
	if (getLength(estates) == 0) printf("No estates match the criteria!\n");
	else for (int i = 0; i < getLength(estates); ++i) { Estate* e = (Estate*)getElement(estates, i); printf("%d.", i + 1); printEstate(e); }
	destroyDynamicVector(estates);
}

void undoUI(UI* ui) { if (serviceUndo(ui->service)) printf("Undo successful!\n"); else printf("Nothing to undo!\n"); }
void redoUI(UI* ui) { if (serviceRedo(ui->service)) printf("Redo successful!\n"); else printf("Nothing to redo!\n"); }

void printMenu()
{
	printf("\n1. Add an estate.\n");
	printf("2. Delete an estate.\n");
	printf("3. Update an estate.\n");
	printf("4. Display all estates whose address contains a given string.\n");
	printf("5. See all estates of a given type, having a minimum given surface.\n");
	printf("6. Undo.\n");
	printf("7. Redo.\n");
	printf("8. Display all estates.\n");
	printf("9. Display all estates of a given type, sorted ascending by address.\n");
	printf("10. For a given surface, display all offers, sorted ascending by price.\n");
	printf("0. Exit.\n");
	printf("Choose an option:\n");
}

void run(UI* ui)
{
	char buf[64];
	int option;
	for (;;)
	{
		printMenu();
		if (!readLine("", buf, sizeof(buf))) { printf("Input error.\n"); continue; }
		option = atoi(buf);
		switch (option)
		{
		case 1: addEstateUI(ui); break;
		case 2: deleteEstateUI(ui); break;
		case 3: updateEstateUI(ui); break;
		case 4: displayEstatesByAddressSubstringUI(ui); break;
		case 5: displayEstatesByTypeAndSurfaceUI(ui); break;
		case 6: undoUI(ui); break;
		case 7: redoUI(ui); break;
		case 8: displayAllEstatesUI(ui); break;
		case 9: displayEstatesByTypeSortedByAddressUI(ui); break;
		case 10: displayEstatesBySurfaceSortedByPriceUI(ui); break;
		case 0: printf("Exiting the app!\n"); return;
		default: printf("Invalid option! Try again!\n"); break;
		}
	}
}