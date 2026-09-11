#include "ConsoleUI.h"
#include "IRepository.h"
#include "FileRepository.h"
#include "Service.h"
#include "TrenchCoat.h"
#include "Tests.h"
#include "Exceptions.h"

#define _CRTDBG_MAP_ALLOC
#include <cstdlib>
#include <crtdbg.h>

int main()
{
    //Tests t;
    //t.test_all();

	/*IRepository repo;
	Service service(repo);
	ConsoleUI ui(service);

    repo.add_trench_coat(TrenchCoat ("S", "beige", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30722749?vid=88127765&view=adp&om_channel=PLA&force-language=1&rh=09&dsw=2058&lmk=607&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VCPu5QSJ9ud5HuUwxhuFemPP&gclid=Cj0KCQjwyr3OBhD0ARIsALlo-OnCP1gyVEeEudvMYnmn39GBn33GHUAZK6iOW9n29SjJe57Gi6IPcoEaAg01EALw_wcB", 120.0, 3));
    repo.add_trench_coat(TrenchCoat("S", "black", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30886299?vid=88417768&view=adp&om_channel=PLA&force-language=1&rh=1&dsw=2063&lmk=6045&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VAmd9AuCREz7gWLTLNMBAyj0&gclid=CjwKCAjw-dfOBhAjEiwAq0RwIzcdlZa9F4sxWwWsAaxd-ExLV2yesdz6rmD8sVgASmHyP0WMqvVD5hoC958QAvD_BwE", 130.0, 2));
    repo.add_trench_coat(TrenchCoat("M", "beige", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30722749?vid=88127765&view=adp&om_channel=PLA&force-language=1&rh=09&dsw=2058&lmk=607&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VCPu5QSJ9ud5HuUwxhuFemPP&gclid=Cj0KCQjwyr3OBhD0ARIsALlo-OnCP1gyVEeEudvMYnmn39GBn33GHUAZK6iOW9n29SjJe57Gi6IPcoEaAg01EALw_wcB", 150.0, 5));
    repo.add_trench_coat(TrenchCoat("M", "black", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30886299?vid=88417768&view=adp&om_channel=PLA&force-language=1&rh=1&dsw=2063&lmk=6045&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VAmd9AuCREz7gWLTLNMBAyj0&gclid=CjwKCAjw-dfOBhAjEiwAq0RwIzcdlZa9F4sxWwWsAaxd-ExLV2yesdz6rmD8sVgASmHyP0WMqvVD5hoC958QAvD_BwE", 160.0, 4));
    repo.add_trench_coat(TrenchCoat("M", "navy", "https://www.stradivarius.com/ro/en/basic-short-trench-coat-l01801586?srsltid=AfmBOop5bgFttvLfzF7HWQH8Ag1mPn28_Rgp1LuBClWxXlsiUP0YPCO0", 155.0, 3));
    repo.add_trench_coat(TrenchCoat("L", "beige", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30722749?vid=88127765&view=adp&om_channel=PLA&force-language=1&rh=09&dsw=2058&lmk=607&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VCPu5QSJ9ud5HuUwxhuFemPP&gclid=Cj0KCQjwyr3OBhD0ARIsALlo-OnCP1gyVEeEudvMYnmn39GBn33GHUAZK6iOW9n29SjJe57Gi6IPcoEaAg01EALw_wcB", 170.0, 2));
    repo.add_trench_coat(TrenchCoat("L", "black", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30886299?vid=88417768&view=adp&om_channel=PLA&force-language=1&rh=1&dsw=2063&lmk=6045&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VAmd9AuCREz7gWLTLNMBAyj0&gclid=CjwKCAjw-dfOBhAjEiwAq0RwIzcdlZa9F4sxWwWsAaxd-ExLV2yesdz6rmD8sVgASmHyP0WMqvVD5hoC958QAvD_BwE", 180.0, 6));
    repo.add_trench_coat(TrenchCoat("L", "olive", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30176113", 175.0, 1));
    repo.add_trench_coat(TrenchCoat("XL", "beige", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30722749?vid=88127765&view=adp&om_channel=PLA&force-language=1&rh=09&dsw=2058&lmk=607&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VCPu5QSJ9ud5HuUwxhuFemPP&gclid=Cj0KCQjwyr3OBhD0ARIsALlo-OnCP1gyVEeEudvMYnmn39GBn33GHUAZK6iOW9n29SjJe57Gi6IPcoEaAg01EALw_wcB", 190.0, 2));
    repo.add_trench_coat(TrenchCoat("XL", "black", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30886299?vid=88417768&view=adp&om_channel=PLA&force-language=1&rh=1&dsw=2063&lmk=6045&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VAmd9AuCREz7gWLTLNMBAyj0&gclid=CjwKCAjw-dfOBhAjEiwAq0RwIzcdlZa9F4sxWwWsAaxd-ExLV2yesdz6rmD8sVgASmHyP0WMqvVD5hoC958QAvD_BwE", 200.0, 3));
    repo.add_trench_coat(TrenchCoat("XL", "camel", "https://www.aboutyou.ro/p/only/palton-de-primavara-toamna-onldisa-30722749?vid=88127764&view=adp&om_channel=PLA&force-language=1&rh=1&dsw=2061&lmk=6073&utm_content=181785709330&utm_source=google&utm_medium=cpc&utm_campaign=PLA_RO_Best_S24&gad_source=1&gad_campaignid=15777446761&gbraid=0AAAAAC2l9VAmd9AuCREz7gWLTLNMBAyj0&gclid=CjwKCAjw-dfOBhAjEiwAq0RwIx9xsFAPRrR4a0KqaD-jkDq9joD4XhMsq8RFjKM9kJQzwkTRumS2bBoC2RMQAvD_BwE", 210.0, 1));

	ui.run();*/


    //int* p;
    //p = new int[10];
    //_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);

    FileRepository repo("coats.txt");
    Service service(repo);
    ConsoleUI ui(service);
    ui.run();

    return 0;
}