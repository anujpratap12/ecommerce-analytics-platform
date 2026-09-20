from pathlib import Path

from sqlalchemy import text

from etl.build_features import (
    build_order_features,
    build_product_features,
    load_data,
)
from python.db_connection import engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def test_feature_engineering_integration():
    """
    Verify that cleaned datasets can be loaded and integrated
    into the analytical order and product datasets.
    """
    data = load_data()

    (
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
    ) = data

    order_features = build_order_features(
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
    )

    product_features = build_product_features(
        order_items,
        products,
        sellers,
    )

    # Verify analytical datasets were created.
    assert not order_features.empty
    assert not product_features.empty

    # Verify important business-analysis fields.
    required_order_columns = {
        "order_id",
        "customer_unique_id",
        "order_total_value",
        "freight_cost",
        "delivery_days",
        "is_late",
        "customer_order_number",
        "recency_days",
        "frequency",
        "monetary_value",
        "is_churned",
        "fulfillment_risk",
    }

    required_product_columns = {
        "order_id",
        "product_id",
        "seller_id",
        "item_total_value",
        "freight_ratio",
    }

    assert required_order_columns.issubset(order_features.columns)
    assert required_product_columns.issubset(product_features.columns)

    # Verify analytical datasets can be persisted.
    order_file = PROCESSED_DATA_DIR / "order_analytics.csv"
    product_file = PROCESSED_DATA_DIR / "order_item_analytics.csv"

    order_features.to_csv(order_file, index=False)
    product_features.to_csv(product_file, index=False)

    assert order_file.exists()
    assert product_file.exists()


def test_postgresql_integration():
    """
    Verify that the PostgreSQL database contains the expected
    staging and analytics schemas/tables and that analytics
    tables contain data.
    """
    with engine.connect() as connection:
        # Verify required schemas.
        schemas = connection.execute(
            text(
                """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name IN ('staging', 'analytics')
                ORDER BY schema_name;
                """
            )
        ).scalars().all()

        assert "analytics" in schemas
        assert "staging" in schemas

        # Verify analytics tables exist.
        tables = connection.execute(
            text(
                """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema = 'analytics'
                  AND table_name IN (
                      'order_analytics',
                      'order_item_analytics'
                  )
                ORDER BY table_name;
                """
            )
        ).all()

        table_names = {row[1] for row in tables}

        assert "order_analytics" in table_names
        assert "order_item_analytics" in table_names

        # Verify analytics tables contain records.
        order_count = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM analytics.order_analytics;
                """
            )
        ).scalar_one()

        product_count = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM analytics.order_item_analytics;
                """
            )
        ).scalar_one()

        assert order_count > 0
        assert product_count > 0


def test_postgresql_analytics_data_integrity():
    """
    Verify basic integrity conditions on the loaded analytical data.
    """
    with engine.connect() as connection:
        # Every analytical order should have an order_id.
        missing_order_ids = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM analytics.order_analytics
                WHERE order_id IS NULL;
                """
            )
        ).scalar_one()

        assert missing_order_ids == 0

        # Order totals should not be negative.
        negative_order_values = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM analytics.order_analytics
                WHERE order_total_value < 0;
                """
            )
        ).scalar_one()

        assert negative_order_values == 0

        # Late-delivery flag should only contain 0/1.
        invalid_late_flags = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM analytics.order_analytics
                WHERE is_late NOT IN (0, 1);
                """
            )
        ).scalar_one()

        assert invalid_late_flags == 0


def test_business_analytics_integration():
    """
    Validate that the PostgreSQL analytics layer can execute
    a business-facing aggregation and return valid results.
    """
    with engine.connect() as connection:
        results = connection.execute(
            text(
                """
                SELECT
                    customer_state,
                    COUNT(DISTINCT order_id) AS order_count,
                    ROUND(
                        AVG(order_total_value)::numeric,
                        2
                    ) AS average_order_value
                FROM analytics.order_analytics
                WHERE customer_state IS NOT NULL
                GROUP BY customer_state
                HAVING COUNT(DISTINCT order_id) >= 100
                ORDER BY order_count DESC
                LIMIT 10;
                """
            )
        ).all()

        assert len(results) == 10

        for row in results:
            assert row[0] is not None
            assert row[1] >= 100
            assert row[2] is not None
            assert row[2] >= 0