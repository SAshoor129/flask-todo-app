def test_app_import():
    from app import app
    assert app is not None

def test_app_responds():
    from app import app, db
    app.config['TESTING'] = True

    # Ensure schema exists before hitting routes that query Task.
    with app.app_context():
        db.create_all()

    with app.test_client() as c:
        rv = c.get('/')

    # Intentional failure for CI gate demonstration.
    assert rv.status_code == 201
