"""create_patient_diagnoses_view

Revision ID: 48aac5265e85
Revises: 3fb0d805be2f
Create Date: 2026-04-19 15:25:31.058046

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '48aac5265e85'
down_revision: Union[str, Sequence[str], None] = '3fb0d805be2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add View: care.patient_diagnoses"""
    op.execute("""
    CREATE OR REPLACE VIEW care.patient_diagnoses AS
    SELECT
        row_number() OVER () AS row_id,
        p.id,
        p.date_of_birth,
        d.icd_code_ref,
        di.icd_family,
        dlt.test_name,
        lr.result_value,
        d.diagnosed_date
    FROM
        CORE.patients p
        JOIN core.diagnoses d ON p.id = d.patient_id
        JOIN core.dim_icd di ON d.icd_code_ref = di.icd_code
        JOIN core.lab_results lr ON lr.patient_id = p.id
        JOIN core.dim_lab_tests dlt ON dlt.id = lr.lab_test_id
    """)


def downgrade() -> None:
    """Drop View: care.patient_diagnoses"""
    op.execute("DROP VIEW IF EXISTS care.patient_diagnoses")
