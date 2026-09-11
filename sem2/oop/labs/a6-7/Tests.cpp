//#include <cassert>
//#include <iostream>
//#include <vector>
//#include <string>
//#include <stdexcept>
//#include "Tests.h"
//
//#include "Tests.h"
//#include <cassert>
//#include <iostream>
//#include <stdexcept>
//
//void Tests::testDomain() {
//    // 1. Test Default Constructor (TrenchCoat.cpp line 3)
//    TrenchCoat defaultCoat;
//    assert(defaultCoat.get_size() == "");
//    assert(defaultCoat.get_price() == 0);
//
//    // 2. Test Parameterized Constructor
//    TrenchCoat c{ "M", "Blue", "link", 100.0, 5 };
//    ;
//
//    // 3. Test ALL Setters (Ensures TrenchCoat.cpp setters are covered)
//    c.set_size("L");
//    c.set_colour("Red");
//    c.set_photoLink("new_url");
//    c.set_price(150.0);
//    c.set_quantity(2);
//    
//
//    // 4. Test ALL Getters
//    assert(c.get_size() == "L");
//    assert(c.get_colour() == "Red");
//    assert(c.get_photoLink() == "new_url");
//    assert(c.get_price() == 150.0);
//    assert(c.get_quantity() == 2);
//    
//    // 5. Test Equality and String conversion
//    TrenchCoat c2{ "L", "Red", "other", 0, 0 };
//    assert(c == c2);
//    assert(!c.to_string().empty());
//    assert(!c.to_string_user().empty());
//
//    std::cout << "Domain tests passed (Constructors, Setters, & Getters covered).\n";
//}
//
//void Tests::testRepository() {
//    Repository repo;
//    TrenchCoat c{ "S", "Green", "url", 50.0, 1 };
//
//    // 1. Test add and get_all_trench_coats()
//    repo.add_trench_coat(c);
//    std::vector<TrenchCoat>& all = repo.get_all_trench_coats();
//    assert(all.size() == 1);
//    assert(all[0].get_size() == "S");
//
//    // 2. Test find_trench_coat
//    assert(repo.find_trench_coat("S", "Green") != nullptr);
//    assert(repo.find_trench_coat("XL", "Black") == nullptr);
//
//    // 3. Test update_trench_coat (Success branch)
//    TrenchCoat updated{ "S", "Green", "url", 70.0, 5 };
//    repo.update_trench_coat(c, updated);
//    assert(repo.find_trench_coat("S", "Green")->get_price() == 70.0);
//
//    // 4. Test update_trench_coat (Non-existent branch)
//    TrenchCoat ghost{ "None", "None", "url", 0, 0 };
//    repo.update_trench_coat(ghost, updated); // Hits the 'return' line
//
//    // 5. Test remove_trench_coat
//    repo.remove_trench_coat(updated);
//    assert(repo.get_all_trench_coats().size() == 0);
//
//    std::cout << "Repository tests passed (Removal & Retrieval covered).\n";
//}
//
//void Tests::testService() {
//    Repository repo;
//    Service serv{ repo };
//
//    // 1. Add data to the repository to test filtering
//    serv.add("S", "Red", "link1", 100, 10);
//    serv.add("M", "Blue", "link2", 150, 5);
//    serv.add("S", "Green", "link3", 120, 3);
//
//    // 2. Test Branch: Empty size string (Hits: if (size.empty()) return all;)
//    // This ensures that all coats in the repo are returned.
//    std::vector<TrenchCoat> allCoats = serv.get_coats_by_size("");
//    assert(allCoats.size() == 3);
//
//    // 3. Test Branch: Specific size (Hits: std::copy_if and the lambda logic)
//    // This tests that the logic correctly identifies matches.
//    std::vector<TrenchCoat> smallCoats = serv.get_coats_by_size("S");
//    assert(smallCoats.size() == 2);
//    assert(smallCoats[0].get_colour() == "Red");
//    assert(smallCoats[1].get_colour() == "Green");
//
//    // 4. Test Branch: Non-existent size
//    // This tests the lambda logic when it returns 'false' for every element.
//    std::vector<TrenchCoat> xxlCoats = serv.get_coats_by_size("XXL");
//    assert(xxlCoats.empty());
//
//    // --- Verification of other collection getters ---
//    // Coverage for get_all_coats()
//    assert(serv.get_all_coats().size() == 3);
//
//    // Coverage for get_basket()
//    serv.add_to_basket(allCoats[0]);
//    assert(serv.get_basket().size() == 1);
//
//
//    //test exceptions
//    try { serv.add("M", "", "http://a.com/1", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Colour") != std::string::npos);
//    }
//
//
//    try { serv.add("M", "beige", "", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Photo") != std::string::npos);
//    }
//
//
//    try { serv.add("", "beige", "http://a.com/1", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Size") != std::string::npos);
//    }
//
//
//    try { serv.add("M", "beige", "http://a.com/1", -1.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Price") != std::string::npos);
//    }
//
//
//    try { serv.add("M", "beige", "http://a.com/1", 150.0, -1); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Quantity") != std::string::npos);
//    }
//
//    //add duplicates
//    serv.add("M", "beige", "http://a.com/1", 150.0, 5);
//    try { serv.add("M", "beige", "http://a.com/2", 160.0, 3); assert(false); }
//    catch (const std::invalid_argument&) {}
//
//    std::cout << "Service collection and filtering tests passed.\n";
//}
//
//static void tc_setters_and_getters()
//{
//    TrenchCoat c;
//    c.set_size("XXL");
//    c.set_colour("olive");
//    c.set_photoLink("http://new.com/coat.jpg");
//    c.set_price(249.50);
//    c.set_quantity(12);
//
//    assert(c.get_size() == "XXL");
//    assert(c.get_colour() == "olive");
//    assert(c.get_photoLink() == "http://new.com/coat.jpg");
//    assert(c.get_price() == 249.50);
//    assert(c.get_quantity() == 12);
//}
//
//static void tc_equality_operator()
//{
//    TrenchCoat a("M", "beige", "http://a.com/1", 100.0, 3);
//    TrenchCoat b("M", "beige", "http://b.com/2", 200.0, 9); 
//    TrenchCoat c("L", "beige", "http://a.com/1", 100.0, 3);
//    TrenchCoat d("M", "black", "http://a.com/1", 100.0, 3); 
//
//    assert(a == b); 
//    assert(!(a == c)); 
//    assert(!(a == d));   
//}
//
//static void tc_to_string()
//{
//    TrenchCoat c("S", "red", "http://x.com/s-red.jpg", 55.0, 4);
//    std::string s = c.to_string();
//    assert(s.find("S") != std::string::npos);
//    assert(s.find("red") != std::string::npos);
//    assert(s.find("http://x.com/s-red.jpg") != std::string::npos);
//    assert(s.find("55") != std::string::npos);
//    assert(s.find("4") != std::string::npos);
//}
//
//
//static void tc_to_string_user()
//{
//    TrenchCoat c("S", "red", "http://x.com/s-red.jpg", 55.0, 4);
//    std::string s = c.to_string_user();
//    assert(s.find("S") != std::string::npos);
//    assert(s.find("red") != std::string::npos);
//    assert(s.find("55") != std::string::npos);
//    assert(s.find("4") != std::string::npos);
//    assert(s.find("http://x.com/s-red.jpg") == std::string::npos);
//}
//
//
//static void svc_add_negative_price()
//{
//    Repository repo; Service svc(repo);
//    try { svc.add("M", "beige", "http://a.com/1", -1.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Price") != std::string::npos);
//    }
//}
//
//static void svc_add_negative_quantity()
//{
//    Repository repo; Service svc(repo);
//    try { svc.add("M", "beige", "http://a.com/1", 150.0, -1); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Quantity") != std::string::npos);
//    }
//}
//
//static void svc_add_duplicate()
//{
//    Repository repo; Service svc(repo);
//    svc.add("M", "beige", "http://a.com/1", 150.0, 5);
//    try { svc.add("M", "beige", "http://a.com/2", 160.0, 3); assert(false); }
//    catch (const std::invalid_argument&) {}
//}
//
//
////static void svc_remove_success()
////{
////    Repository repo; Service svc(repo);
////    svc.add("L", "black", "http://a.com/1", 180.0, 0);
////    svc.remove("L", "black");
////    assert(svc.get_all_coats().getLength() == 0);
////}
//
//
//static void svc_remove_empty_size()
//{
//    Repository repo; Service svc(repo);
//    try { svc.remove("", "black"); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Size") != std::string::npos);
//    }
//}
//
//
//static void svc_remove_empty_colour()
//{
//    Repository repo; Service svc(repo);
//    try { svc.remove("L", ""); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Colour") != std::string::npos);
//    }
//}
//
//
//static void svc_remove_not_found()
//{
//    Repository repo; Service svc(repo);
//    try { svc.remove("L", "black"); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("No trench coat") != std::string::npos);
//    }
//}
//
//
//static void svc_remove_nonzero_quantity()
//{
//    Repository repo; Service svc(repo);
//    svc.add("L", "black", "http://a.com/1", 180.0, 3);
//    try { svc.remove("L", "black"); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("still are") != std::string::npos);
//    }
//}
//
//
//
//
//static void svc_update_empty_size()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("", "beige", "http://a.com/1", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Size") != std::string::npos);
//    }
//}
//
//static void svc_update_empty_colour()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("M", "", "http://a.com/1", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Colour") != std::string::npos);
//    }
//}
//
//
//static void svc_update_empty_photo()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("M", "beige", "", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Photo") != std::string::npos);
//    }
//}
//
//
//static void svc_update_negative_price()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("M", "beige", "http://a.com/1", -5.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Price") != std::string::npos);
//    }
//}
//
//
//static void svc_update_negative_quantity()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("M", "beige", "http://a.com/1", 150.0, -3); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("Quantity") != std::string::npos);
//    }
//}
//
//
//static void svc_update_not_found()
//{
//    Repository repo; Service svc(repo);
//    try { svc.update("M", "beige", "http://a.com/1", 150.0, 5); assert(false); }
//    catch (const std::invalid_argument& e)
//    {
//        assert(std::string(e.what()).find("No trench coat") != std::string::npos);
//    }
//}
////
////
////static void svc_get_all_coats_ref()
////{
////    Repository repo; Service svc(repo);
////    DynamicVector<TrenchCoat>& ref = svc.get_all_coats();
////    assert(ref.getLength() == 0);
////    svc.add("S", "red", "http://a.com/1", 50.0, 1);
////    assert(ref.getLength() == 1);
////}
////
////
////static void svc_get_by_size_all()
////{
////    Repository repo; Service svc(repo);
////    svc.add("S", "red", "http://a.com/1", 50.0, 1);
////    svc.add("M", "blue", "http://a.com/2", 80.0, 2);
////    svc.add("L", "grey", "http://a.com/3", 110.0, 3);
////    assert(svc.get_coats_by_size("").getLength() == 3);
////}
////
////
////static void svc_get_by_size_filtered()
////{
////    Repository repo; Service svc(repo);
////    svc.add("M", "red", "http://a.com/1", 80.0, 2);
////    svc.add("M", "blue", "http://a.com/2", 85.0, 1);
////    svc.add("L", "grey", "http://a.com/3", 110.0, 3);
////    DynamicVector<TrenchCoat> result = svc.get_coats_by_size("M");
////    assert(result.getLength() == 2);
////    for (int i = 0; i < result.getLength(); i++)
////        assert(result.get(i).get_size() == "M");
////}
////
////
////static void svc_get_by_size_no_match()
////{
////    Repository repo; Service svc(repo);
////    svc.add("S", "red", "http://a.com/1", 50.0, 2);
////    assert(svc.get_coats_by_size("XXL").getLength() == 0);
////}
////
////
////static void svc_get_by_size_empty_repo()
////{
////    Repository repo; Service svc(repo);
////    assert(svc.get_coats_by_size("M").getLength() == 0);
////}
////
////
////static void svc_add_to_basket_success()
////{
////    Repository repo; Service svc(repo);
////    svc.add("M", "beige", "http://a.com/1", 150.0, 3);
////    TrenchCoat c = svc.get_all_coats().get(0);
////    svc.add_to_basket(c);
////    assert(svc.get_basket().getLength() == 1);
////    assert(svc.get_total_price() == 150);
////    assert(svc.get_all_coats().get(0).get_quantity() == 2);
////}
////
////
////static void svc_add_to_basket_twice()
////{
////    Repository repo; Service svc(repo);
////    svc.add("M", "navy", "http://a.com/1", 100.0, 5);
////    svc.add_to_basket(svc.get_all_coats().get(0));
////    svc.add_to_basket(svc.get_all_coats().get(0));
////    assert(svc.get_basket().getLength() == 2);
////    assert(svc.get_total_price() == 200);
////    assert(svc.get_all_coats().get(0).get_quantity() == 3);
////}
////
////
////static void svc_add_to_basket_not_in_repo()
////{
////    Repository repo; Service svc(repo);
////    TrenchCoat ghost("XL", "red", "u", 1.0, 5);
////    try { svc.add_to_basket(ghost); assert(false); }
////    catch (const std::invalid_argument& e)
////    {
////        assert(std::string(e.what()).find("not found") != std::string::npos);
////    }
////}
////
////
////static void svc_add_to_basket_out_of_stock()
////{
////    Repository repo; Service svc(repo);
////    svc.add("S", "olive", "http://a.com/1", 90.0, 0);
////    TrenchCoat c = svc.get_all_coats().get(0);
////    try { svc.add_to_basket(c); assert(false); }
////    catch (const std::invalid_argument& e)
////    {
////        assert(std::string(e.what()).find("stock") != std::string::npos);
////    }
////    assert(svc.get_basket().getLength() == 0);
////    assert(svc.get_total_price() == 0);
////}
////
////
////static void svc_get_basket_returns_copy()
////{
////    Repository repo; Service svc(repo);
////    svc.add("M", "beige", "http://a.com/1", 150.0, 2);
////    svc.add_to_basket(svc.get_all_coats().get(0));
////
////    DynamicVector<TrenchCoat> copy = svc.get_basket();
////    copy.remove(0);                      
////
////    assert(svc.get_basket().getLength() == 1);
////}
////
////static void svc_get_basket_empty()
////{
////    Repository repo; Service svc(repo);
////    assert(svc.get_basket().getLength() == 0);
////}
////
////static void svc_total_price_zero()
////{
////    Repository repo; Service svc(repo);
////    assert(svc.get_total_price() == 0);
////}
////
////static void svc_total_price_accumulates()
////{
////    Repository repo; Service svc(repo);
////    svc.add("S", "red", "http://a.com/1", 50.0, 3);
////    svc.add("M", "blue", "http://a.com/2", 100.0, 3);
////
////    svc.add_to_basket(svc.get_all_coats().get(0)); 
////    svc.add_to_basket(svc.get_all_coats().get(1));
////    assert(svc.get_total_price() == 150);
////}
////
//void test_service_layer()
//{
//    svc_add_negative_price();
//    svc_add_negative_quantity();
//    svc_add_duplicate();
//    svc_remove_empty_size();
//    svc_remove_empty_colour();
//    svc_remove_not_found();
//    svc_remove_nonzero_quantity();
//
//    svc_update_empty_size();
//    svc_update_empty_colour();
//    svc_update_empty_photo();
//    svc_update_negative_price();
//    svc_update_negative_quantity();
//    svc_update_not_found();
//
//    /*
//    svc_get_all_coats_ref();
//
//    svc_get_by_size_all();
//    svc_get_by_size_filtered();
//    svc_get_by_size_no_match();
//    svc_get_by_size_empty_repo();
//
//    svc_add_to_basket_success();
//    svc_add_to_basket_twice();
//    svc_add_to_basket_not_in_repo();
//    svc_add_to_basket_out_of_stock();
//
//    svc_get_basket_returns_copy();
//    svc_get_basket_empty();
//
//    svc_total_price_zero();
//    svc_total_price_accumulates();*/
//}
////
////
////void run_all_tests()
////{
////    test_add_req();
////    test_trenchcoat_layer();
////    test_dynamicvector_layer();
////    test_repository_layer();
////    test_service_layer();
////    std::cout << "All tests passed.\n";
////}
//
//
//void Tests::test_all() {
//    testDomain();
//    testRepository();
//    testService();
//    tc_setters_and_getters();
//    tc_equality_operator();
//    tc_to_string();
//    tc_to_string_user();
//    test_service_layer();
//}
