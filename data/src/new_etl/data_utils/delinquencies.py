from ..classes.featurelayer import FeatureLayer
from ..constants.services import DELINQUENCIES_QUERY


def delinquencies(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds property tax delinquency information to the primary feature layer by
    joining with a tax delinquencies dataset.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with added columns for tax delinquency
        information, including total due, actionable status, payment agreements, and more.
    """
    tax_delinquencies = FeatureLayer(
        name="Property Tax Delinquencies",
        carto_sql_queries=DELINQUENCIES_QUERY,
        use_wkb_geom_field="the_geom",
        cols=[
            "opa_number",
            "total_due",
            "is_actionable",
            "payment_agreement",
            "num_years_owed",
            "most_recent_year_owed",
            "total_assessment",
            "sheriff_sale",
        ],
    )

    primary_featurelayer.opa_join(
        tax_delinquencies.gdf,
        "opa_number",
    )

    delinquency_cols = [
        "total_due",
        "is_actionable",
        "payment_agreement",
        "num_years_owed",
        "most_recent_year_owed",
        "total_assessment",
    ]
    primary_featurelayer.gdf[delinquency_cols] = primary_featurelayer.gdf[
        delinquency_cols
    ].fillna("NA")

    primary_featurelayer.gdf["sheriff_sale"] = primary_featurelayer.gdf[
        "sheriff_sale"
    ].fillna("N")

    return primary_featurelayer