import eesyapi




def test_import():
    assert eesyapi is not None

#checks pckage was imported correctly



def test_functions_exist():
    assert hasattr(eesyapi, "api_url")
    assert hasattr(eesyapi, "get_publications")


    #checks main functions are available after importing eesyapi to see if it was successful