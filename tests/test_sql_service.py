from app.services.sql_validator import validate_sql

def test_select_query():

    valid, message = validate_sql(
        "SELECT * FROM customers"
    )

    assert valid is True


def test_with_query():

    valid, message = validate_sql(
        """
        WITH data AS (
            SELECT * FROM orders
        )
        SELECT * FROM data
        """
    )

    assert valid is True


def test_delete_blocked():

    valid, message = validate_sql(
        "DELETE FROM customers"
    )

    assert valid is False


def test_drop_blocked():

    valid, message = validate_sql(
        "DROP TABLE customers"
    )

    assert valid is False


def test_update_blocked():

    valid, message = validate_sql(
        "UPDATE customers SET name = 'Test'"
    )

    assert valid is False