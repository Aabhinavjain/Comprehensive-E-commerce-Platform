# tests/test_app.py

def test_login(client):
    """
    Test user login flow.
    """
    # First, register the user
    response = client.post(
        "/auth/register",
        data={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "secret123",
            "confirm_password": "secret123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Your account has been created! You can now log in." in response.data

    # Then, login
    response = client.post(
        "/auth/login",
        data={
            "email": "login@example.com",
            "password": "secret123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data

def test_add_to_cart(client):
    """
    Test adding an item to the cart and viewing the cart.
    """
    # Login first
    response = client.post(
        "/auth/login",
        data={
            "email": "test@example.com",
            "password": "secret123"  # Use raw password as per hashing in conftest.py
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data

    # Add a product to the cart
    response = client.post(
        "/cart/add_to_cart",
        data={"product_id": 1, "quantity": 2},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Product added to cart!" in response.data

def test_checkout_flow(client):
    """
    Test the checkout process: add product to cart, then checkout.
    """
    # Login first
    response = client.post(
        "/auth/login",
        data={
            "email": "test@example.com",
            "password": "secret123"  # Use raw password as per hashing in conftest.py
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data

    # Add a product to the cart
    response = client.post(
        "/cart/add_to_cart",
        data={"product_id": 1, "quantity": 2},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Product added to cart!" in response.data

    # Proceed to checkout
    response = client.post(
        "/cart/checkout",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Order placed successfully!" in response.data
