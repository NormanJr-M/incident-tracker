def test_package_has_version(): 
    import incident_tracker
    assert incident_tracker.__version__=="0.1.0"
    