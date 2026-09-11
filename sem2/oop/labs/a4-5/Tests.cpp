#include "TrenchCoat.h"
#include "DynamicVector.h"
#include "Repository.h"
#include "Service.h"
#include <cassert>
#include <stdexcept>
#include <iostream>

#include "Tests.h"
#include <cassert>
#include <stdexcept>


void test_add_req()
{
    Repository repo;
    Service service{ repo };

    TrenchCoat shortCoat("S", "Blue", "link", 100, 5);
    shortCoat.setLengthCoat(10);
    repo.add_trench_coat(shortCoat);

    TrenchCoat longCoat("L", "Black", "link", 200, 5);
    longCoat.setLengthCoat(50);
    repo.add_trench_coat(longCoat);


    DynamicVector<TrenchCoat> result = service.filter_by_length(30);
    assert(result.getLength() == 1);
    assert(result.get(0).get_colour() == "Blue");

    //empty result
    DynamicVector<TrenchCoat> none = service.filter_by_length(5);
    assert(none.getLength() == 0);
}


static void tc_equality_operator()
{
    TrenchCoat a("M", "beige", "http://a.com/1", 100.0, 3);
    TrenchCoat b("M", "beige", "http://b.com/2", 200.0, 9); 
    TrenchCoat c("L", "beige", "http://a.com/1", 100.0, 3);
    TrenchCoat d("M", "black", "http://a.com/1", 100.0, 3); 

    assert(a == b); 
    assert(!(a == c)); 
    assert(!(a == d));   
}


static void tc_setters_and_getters()
{
    TrenchCoat c;
    c.set_size("XXL");
    c.set_colour("olive");
    c.set_photoLink("http://new.com/coat.jpg");
    c.set_price(249.50);
    c.set_quantity(12);
    c.setLengthCoat(12);

    assert(c.get_size() == "XXL");
    assert(c.get_colour() == "olive");
    assert(c.get_photoLink() == "http://new.com/coat.jpg");
    assert(c.get_price() == 249.50);
    assert(c.get_quantity() == 12);
    assert(c.getLengthCoat() == 12);
}


static void tc_to_string()
{
    TrenchCoat c("S", "red", "http://x.com/s-red.jpg", 55.0, 4);
    std::string s = c.to_string();
    assert(s.find("S") != std::string::npos);
    assert(s.find("red") != std::string::npos);
    assert(s.find("http://x.com/s-red.jpg") != std::string::npos);
    assert(s.find("55") != std::string::npos);
    assert(s.find("4") != std::string::npos);
}


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

void tc_to_string_user() {
    TrenchCoat coat("M", "Beige", "link", 150.0, 5);
    coat.setLengthCoat(105);

    std::string result = coat.to_string_user();

    assert(result.find("M") != std::string::npos);
    assert(result.find("Beige") != std::string::npos);
    assert(result.find("105") != std::string::npos);
}

void test_trenchcoat_layer()
{
    tc_equality_operator();
    tc_setters_and_getters();
    tc_to_string();
    tc_to_string_user();
}






static void dv_add_triggers_resize()
{
    DynamicVector<TrenchCoat> v;
    for (int i = 0; i < 15; i++)
        v.add(TrenchCoat("M", "c" + std::to_string(i), "http://x.com/" + std::to_string(i), 10.0 * i, i));

    assert(v.getLength() == 15);
    for (int i = 0; i < 15; i++)
        assert(v.get(i).get_colour() == "c" + std::to_string(i));
}


static void dv_get_valid()
{
    DynamicVector<TrenchCoat> v;
    TrenchCoat c0("XS", "a", "u", 1.0, 0);
    TrenchCoat c1("S", "b", "u", 2.0, 1);
    TrenchCoat c2("M", "c", "u", 3.0, 2);
    v.add(c0); v.add(c1); v.add(c2);
    assert(v.get(0) == c0);
    assert(v.get(1) == c1);
    assert(v.get(2) == c2);
}


static void dv_get_negative_index_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("M", "x", "u", 1.0, 1));
    try { v.get(-1); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_get_out_of_range_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("M", "x", "u", 1.0, 1));
    try { v.get(1); assert(false); }  // index == size
    catch (const std::invalid_argument&) {}
}


static void dv_get_empty_throws()
{
    DynamicVector<TrenchCoat> v;
    try { v.get(0); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_update_valid()
{
    DynamicVector<TrenchCoat> v;
    TrenchCoat old_c("S", "white", "u", 50.0, 1);
    TrenchCoat new_c("S", "red", "u", 60.0, 2);
    v.add(old_c);
    v.update(0, new_c);
    assert(v.get(0) == new_c);
}


static void dv_update_negative_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("S", "x", "u", 1.0, 1));
    try { v.update(-1, TrenchCoat()); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_update_out_of_range_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("S", "x", "u", 1.0, 1));
    try { v.update(1, TrenchCoat()); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_remove_first()
{
    DynamicVector<TrenchCoat> v;
    TrenchCoat c0("S", "a", "u", 1.0, 0);
    TrenchCoat c1("M", "b", "u", 2.0, 1);
    TrenchCoat c2("L", "c", "u", 3.0, 2);
    v.add(c0); v.add(c1); v.add(c2);
    v.remove(0);
    assert(v.getLength() == 2);
    assert(v.get(0) == c1);
    assert(v.get(1) == c2);
}


static void dv_remove_last()
{
    DynamicVector<TrenchCoat> v;
    TrenchCoat c0("S", "a", "u", 1.0, 0);
    TrenchCoat c1("M", "b", "u", 2.0, 1);
    v.add(c0); v.add(c1);
    v.remove(1);
    assert(v.getLength() == 1);
    assert(v.get(0) == c0);
}

static void dv_remove_middle()
{
    DynamicVector<TrenchCoat> v;
    TrenchCoat c0("S", "a", "u", 1.0, 0);
    TrenchCoat c1("M", "b", "u", 2.0, 1);
    TrenchCoat c2("L", "c", "u", 3.0, 2);
    v.add(c0); v.add(c1); v.add(c2);
    v.remove(1);
    assert(v.getLength() == 2);
    assert(v.get(0) == c0);
    assert(v.get(1) == c2);
}


static void dv_remove_negative_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("S", "x", "u", 1.0, 1));
    try { v.remove(-1); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_remove_out_of_range_throws()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("S", "x", "u", 1.0, 1));
    try { v.remove(1); assert(false); }
    catch (const std::invalid_argument&) {}
}

static void dv_remove_empty_throws()
{
    DynamicVector<TrenchCoat> v;
    try { v.remove(0); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void dv_copy_constructor_deep()
{
    DynamicVector<TrenchCoat> orig;
    TrenchCoat c("M", "blue", "u", 80.0, 3);
    orig.add(c);

    DynamicVector<TrenchCoat> copy(orig);
    assert(copy.getLength() == 1);
    assert(copy.get(0) == c);


    copy.add(TrenchCoat("L", "green", "u", 90.0, 1));
    assert(orig.getLength() == 1);
    assert(copy.getLength() == 2);
}

static void dv_copy_constructor_empty()
{
    DynamicVector<TrenchCoat> empty;
    DynamicVector<TrenchCoat> copy(empty);
    assert(copy.getLength() == 0);
}


static void dv_assignment_operator_deep()
{
    DynamicVector<TrenchCoat> v1;
    v1.add(TrenchCoat("S", "white", "u", 60.0, 4));

    DynamicVector<TrenchCoat> v2;
    v2.add(TrenchCoat("XL", "black", "u", 200.0, 1));

    v2 = v1;
    assert(v2.getLength() == 1);
    assert(v2.get(0).get_colour() == "white");

    v2.add(TrenchCoat("M", "grey", "u", 90.0, 2));
    assert(v1.getLength() == 1);
}


static void dv_assignment_operator_self()
{
    DynamicVector<TrenchCoat> v;
    v.add(TrenchCoat("S", "x", "u", 1.0, 1));
    v = v; 
    assert(v.getLength() == 1);
}


static void dv_get_length()
{
    DynamicVector<TrenchCoat> v;
    assert(v.getLength() == 0);
    v.add(TrenchCoat("S", "a", "u", 1.0, 1));
    assert(v.getLength() == 1);
    v.remove(0);
    assert(v.getLength() == 0);
}

void test_dynamicvector_layer()
{
    dv_add_triggers_resize();
    dv_get_valid();
    dv_get_negative_index_throws();
    dv_get_out_of_range_throws();
    dv_get_empty_throws();
    dv_update_valid();
    dv_update_negative_throws();
    dv_update_out_of_range_throws();
    dv_remove_first();
    dv_remove_last();
    dv_remove_middle();
    dv_remove_negative_throws();
    dv_remove_out_of_range_throws();
    dv_remove_empty_throws();
    dv_copy_constructor_deep();
    dv_copy_constructor_empty();
    dv_assignment_operator_deep();
    dv_assignment_operator_self();
    dv_get_length();
}




static void repo_add()
{
    Repository repo;
    TrenchCoat c1("M", "beige", "http://a.com/1", 150.0, 5);
    TrenchCoat c2("L", "black", "http://a.com/2", 180.0, 3);
    repo.add_trench_coat(c1);
    repo.add_trench_coat(c2);
    assert(repo.get_all_trench_coats().getLength() == 2);
}


static void repo_find_found()
{
    Repository repo;
    TrenchCoat c("M", "beige", "http://a.com/1", 150.0, 5);
    repo.add_trench_coat(c);
    TrenchCoat* found = repo.find_trench_coat("M", "beige");
    assert(found != nullptr);
    assert(found->get_price() == 150.0);
}


static void repo_find_not_found()
{
    Repository repo;
    repo.add_trench_coat(TrenchCoat("M", "beige", "http://a.com/1", 150.0, 5));
    assert(repo.find_trench_coat("XL", "red") == nullptr);
}


static void repo_find_empty()
{
    Repository repo;
    assert(repo.find_trench_coat("M", "beige") == nullptr);
}


static void repo_remove_found()
{
    Repository repo;
    TrenchCoat c1("M", "beige", "http://a.com/1", 150.0, 5);
    TrenchCoat c2("L", "black", "http://a.com/2", 180.0, 3);
    repo.add_trench_coat(c1);
    repo.add_trench_coat(c2);
    repo.remove_trench_coat(c1);
    assert(repo.get_all_trench_coats().getLength() == 1);
    assert(repo.find_trench_coat("M", "beige") == nullptr);
    assert(repo.find_trench_coat("L", "black") != nullptr);
}


static void repo_remove_not_found()
{
    Repository repo;
    TrenchCoat c("M", "beige", "http://a.com/1", 150.0, 5);
    repo.add_trench_coat(c);
    TrenchCoat ghost("XL", "red", "", 0.0, 0);
    repo.remove_trench_coat(ghost);  
    assert(repo.get_all_trench_coats().getLength() == 1);
}


static void repo_remove_last_element()
{
    Repository repo;
    TrenchCoat c("S", "white", "http://a.com/1", 60.0, 2);
    repo.add_trench_coat(c);
    repo.remove_trench_coat(c);
    assert(repo.get_all_trench_coats().getLength() == 0);
}


static void repo_update_found()
{
    Repository repo;
    TrenchCoat old_c("M", "beige", "http://a.com/1", 150.0, 5);
    repo.add_trench_coat(old_c);

    TrenchCoat new_c("M", "beige", "http://a.com/new.jpg", 175.0, 2);
    repo.update_trench_coat(old_c, new_c);

    TrenchCoat* found = repo.find_trench_coat("M", "beige");
    assert(found != nullptr);
    assert(found->get_price() == 175.0);
    assert(found->get_quantity() == 2);
    assert(found->get_photoLink() == "http://a.com/new.jpg");
}


static void repo_update_not_found()
{
    Repository repo;
    TrenchCoat c("M", "beige", "http://a.com/1", 150.0, 5);
    repo.add_trench_coat(c);

    TrenchCoat ghost("XL", "red", "u", 0.0, 0);
    TrenchCoat replacement("XL", "red", "u", 999.0, 0);
    repo.update_trench_coat(ghost, replacement);
    assert(repo.get_all_trench_coats().getLength() == 1);
    assert(repo.find_trench_coat("XL", "red") == nullptr);
}


static void repo_get_all_returns_ref()
{
    Repository repo;
    repo.add_trench_coat(TrenchCoat("S", "blue", "u", 40.0, 1));
    DynamicVector<TrenchCoat>& ref = repo.get_all_trench_coats();
    assert(ref.getLength() == 1);
    repo.add_trench_coat(TrenchCoat("M", "red", "u", 60.0, 2));
    assert(ref.getLength() == 2);
}

void test_repository_layer()
{
    repo_add();
    repo_find_found();
    repo_find_not_found();
    repo_find_empty();
    repo_remove_found();
    repo_remove_not_found();
    repo_remove_last_element();
    repo_update_found();
    repo_update_not_found();
    repo_get_all_returns_ref();
}



static void svc_add_success()
{
    Repository repo; Service svc(repo);
    svc.add("M", "beige", "http://a.com/1", 150.0, 5);
    assert(svc.get_all_coats().getLength() == 1);
}


static void svc_add_empty_size()
{
    Repository repo; Service svc(repo);
    try { svc.add("", "beige", "http://a.com/1", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Size") != std::string::npos);
    }
}


static void svc_add_empty_colour()
{
    Repository repo; Service svc(repo);
    try { svc.add("M", "", "http://a.com/1", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Colour") != std::string::npos);
    }
}


static void svc_add_empty_photo()
{
    Repository repo; Service svc(repo);
    try { svc.add("M", "beige", "", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Photo") != std::string::npos);
    }
}


static void svc_add_negative_price()
{
    Repository repo; Service svc(repo);
    try { svc.add("M", "beige", "http://a.com/1", -1.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Price") != std::string::npos);
    }
}

static void svc_add_negative_quantity()
{
    Repository repo; Service svc(repo);
    try { svc.add("M", "beige", "http://a.com/1", 150.0, -1); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Quantity") != std::string::npos);
    }
}


static void svc_add_duplicate()
{
    Repository repo; Service svc(repo);
    svc.add("M", "beige", "http://a.com/1", 150.0, 5);
    try { svc.add("M", "beige", "http://a.com/2", 160.0, 3); assert(false); }
    catch (const std::invalid_argument&) {}
}


static void svc_remove_success()
{
    Repository repo; Service svc(repo);
    svc.add("L", "black", "http://a.com/1", 180.0, 0);
    svc.remove("L", "black");
    assert(svc.get_all_coats().getLength() == 0);
}


static void svc_remove_empty_size()
{
    Repository repo; Service svc(repo);
    try { svc.remove("", "black"); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Size") != std::string::npos);
    }
}


static void svc_remove_empty_colour()
{
    Repository repo; Service svc(repo);
    try { svc.remove("L", ""); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Colour") != std::string::npos);
    }
}


static void svc_remove_not_found()
{
    Repository repo; Service svc(repo);
    try { svc.remove("L", "black"); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("No trench coat") != std::string::npos);
    }
}


static void svc_remove_nonzero_quantity()
{
    Repository repo; Service svc(repo);
    svc.add("L", "black", "http://a.com/1", 180.0, 3);
    try { svc.remove("L", "black"); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("still are") != std::string::npos);
    }
}
\
static void svc_update_success()
{
    Repository repo; Service svc(repo);
    svc.add("M", "beige", "http://a.com/1", 150.0, 5);
    svc.update("M", "beige", "http://a.com/new.jpg", 175.0, 2);
    TrenchCoat& c = svc.get_all_coats().get(0);
    assert(c.get_price() == 175.0);
    assert(c.get_quantity() == 2);
    assert(c.get_photoLink() == "http://a.com/new.jpg");
}


static void svc_update_empty_size()
{
    Repository repo; Service svc(repo);
    try { svc.update("", "beige", "http://a.com/1", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Size") != std::string::npos);
    }
}

static void svc_update_empty_colour()
{
    Repository repo; Service svc(repo);
    try { svc.update("M", "", "http://a.com/1", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Colour") != std::string::npos);
    }
}


static void svc_update_empty_photo()
{
    Repository repo; Service svc(repo);
    try { svc.update("M", "beige", "", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Photo") != std::string::npos);
    }
}


static void svc_update_negative_price()
{
    Repository repo; Service svc(repo);
    try { svc.update("M", "beige", "http://a.com/1", -5.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Price") != std::string::npos);
    }
}


static void svc_update_negative_quantity()
{
    Repository repo; Service svc(repo);
    try { svc.update("M", "beige", "http://a.com/1", 150.0, -3); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("Quantity") != std::string::npos);
    }
}


static void svc_update_not_found()
{
    Repository repo; Service svc(repo);
    try { svc.update("M", "beige", "http://a.com/1", 150.0, 5); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("No trench coat") != std::string::npos);
    }
}


static void svc_get_all_coats_ref()
{
    Repository repo; Service svc(repo);
    DynamicVector<TrenchCoat>& ref = svc.get_all_coats();
    assert(ref.getLength() == 0);
    svc.add("S", "red", "http://a.com/1", 50.0, 1);
    assert(ref.getLength() == 1);
}


static void svc_get_by_size_all()
{
    Repository repo; Service svc(repo);
    svc.add("S", "red", "http://a.com/1", 50.0, 1);
    svc.add("M", "blue", "http://a.com/2", 80.0, 2);
    svc.add("L", "grey", "http://a.com/3", 110.0, 3);
    assert(svc.get_coats_by_size("").getLength() == 3);
}


static void svc_get_by_size_filtered()
{
    Repository repo; Service svc(repo);
    svc.add("M", "red", "http://a.com/1", 80.0, 2);
    svc.add("M", "blue", "http://a.com/2", 85.0, 1);
    svc.add("L", "grey", "http://a.com/3", 110.0, 3);
    DynamicVector<TrenchCoat> result = svc.get_coats_by_size("M");
    assert(result.getLength() == 2);
    for (int i = 0; i < result.getLength(); i++)
        assert(result.get(i).get_size() == "M");
}


static void svc_get_by_size_no_match()
{
    Repository repo; Service svc(repo);
    svc.add("S", "red", "http://a.com/1", 50.0, 2);
    assert(svc.get_coats_by_size("XXL").getLength() == 0);
}


static void svc_get_by_size_empty_repo()
{
    Repository repo; Service svc(repo);
    assert(svc.get_coats_by_size("M").getLength() == 0);
}


static void svc_add_to_basket_success()
{
    Repository repo; Service svc(repo);
    svc.add("M", "beige", "http://a.com/1", 150.0, 3);
    TrenchCoat c = svc.get_all_coats().get(0);
    svc.add_to_basket(c);
    assert(svc.get_basket().getLength() == 1);
    assert(svc.get_total_price() == 150);
    assert(svc.get_all_coats().get(0).get_quantity() == 2);
}


static void svc_add_to_basket_twice()
{
    Repository repo; Service svc(repo);
    svc.add("M", "navy", "http://a.com/1", 100.0, 5);
    svc.add_to_basket(svc.get_all_coats().get(0));
    svc.add_to_basket(svc.get_all_coats().get(0));
    assert(svc.get_basket().getLength() == 2);
    assert(svc.get_total_price() == 200);
    assert(svc.get_all_coats().get(0).get_quantity() == 3);
}


static void svc_add_to_basket_not_in_repo()
{
    Repository repo; Service svc(repo);
    TrenchCoat ghost("XL", "red", "u", 1.0, 5);
    try { svc.add_to_basket(ghost); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("not found") != std::string::npos);
    }
}


static void svc_add_to_basket_out_of_stock()
{
    Repository repo; Service svc(repo);
    svc.add("S", "olive", "http://a.com/1", 90.0, 0);
    TrenchCoat c = svc.get_all_coats().get(0);
    try { svc.add_to_basket(c); assert(false); }
    catch (const std::invalid_argument& e)
    {
        assert(std::string(e.what()).find("stock") != std::string::npos);
    }
    assert(svc.get_basket().getLength() == 0);
    assert(svc.get_total_price() == 0);
}


static void svc_get_basket_returns_copy()
{
    Repository repo; Service svc(repo);
    svc.add("M", "beige", "http://a.com/1", 150.0, 2);
    svc.add_to_basket(svc.get_all_coats().get(0));

    DynamicVector<TrenchCoat> copy = svc.get_basket();
    copy.remove(0);                      

    assert(svc.get_basket().getLength() == 1);
}

static void svc_get_basket_empty()
{
    Repository repo; Service svc(repo);
    assert(svc.get_basket().getLength() == 0);
}

static void svc_total_price_zero()
{
    Repository repo; Service svc(repo);
    assert(svc.get_total_price() == 0);
}

static void svc_total_price_accumulates()
{
    Repository repo; Service svc(repo);
    svc.add("S", "red", "http://a.com/1", 50.0, 3);
    svc.add("M", "blue", "http://a.com/2", 100.0, 3);

    svc.add_to_basket(svc.get_all_coats().get(0)); 
    svc.add_to_basket(svc.get_all_coats().get(1));
    assert(svc.get_total_price() == 150);
}

void test_service_layer()
{
    svc_add_success();
    svc_add_empty_size();
    svc_add_empty_colour();
    svc_add_empty_photo();
    svc_add_negative_price();
    svc_add_negative_quantity();
    svc_add_duplicate();

    svc_remove_success();
    svc_remove_empty_size();
    svc_remove_empty_colour();
    svc_remove_not_found();
    svc_remove_nonzero_quantity();

    svc_update_success();
    svc_update_empty_size();
    svc_update_empty_colour();
    svc_update_empty_photo();
    svc_update_negative_price();
    svc_update_negative_quantity();
    svc_update_not_found();

    svc_get_all_coats_ref();

    svc_get_by_size_all();
    svc_get_by_size_filtered();
    svc_get_by_size_no_match();
    svc_get_by_size_empty_repo();

    svc_add_to_basket_success();
    svc_add_to_basket_twice();
    svc_add_to_basket_not_in_repo();
    svc_add_to_basket_out_of_stock();

    svc_get_basket_returns_copy();
    svc_get_basket_empty();

    svc_total_price_zero();
    svc_total_price_accumulates();
}


void run_all_tests()
{
    test_add_req();
    test_trenchcoat_layer();
    test_dynamicvector_layer();
    test_repository_layer();
    test_service_layer();
    std::cout << "All tests passed.\n";
}