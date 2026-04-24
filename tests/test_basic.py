import eesyapi


def test_import():
    # just checks it imports
    assert eesyapi is not None


def test_api_url():
    #try run api_url
    result = eesyapi.api_url()

    #should give something back
    assert result is not None
    assert "http" in result


def test_get_publications():
    # run publications function
    data = eesyapi.get_publications()

    #not really checking much just that it run
    assert data is not None


def test_get_data_catalogue():
    #using id from earlier
    publication_id = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"

    data = eesyapi.get_data_catalogue(publication_id)

    #again just checking it runs
    assert data is not None


def test_first_dataset_id():
    
    publication_id = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"

    catalogue = eesyapi.get_data_catalogue(publication_id)

    first = catalogue[0]   
    assert "id" in first


def test_get_dataset():
    #uses first dataset id
    publication_id = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"

    catalogue = eesyapi.get_data_catalogue(publication_id)
    dataset_id = catalogue[0]["id"]

    result = eesyapi.get_dataset(dataset_id)

    assert result is not None


def test_get_meta():
    
    publication_id = "8b7474f9-5870-4ecc-7557-08da5f64dcf1"

    catalogue = eesyapi.get_data_catalogue(publication_id)
    dataset_id = catalogue[0]["id"]

    result = eesyapi.get_meta(dataset_id)

    assert result is not None