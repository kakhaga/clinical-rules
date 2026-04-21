"""add_patient_evaluation_needs_view

Revision ID: 69a4094f8da0
Revises: 7b48857f06c2
Create Date: 2026-04-20 16:05:30.378218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69a4094f8da0'
down_revision: Union[str, Sequence[str], None] = '7b48857f06c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add View: patient_evaluation_needs"""
    op.execute("""
    CREATE OR REPLACE VIEW care.patient_evaluation_needs AS
        WITH
                base AS (
                        SELECT DISTINCT
                                p.id AS patient_id,
                                dp.program_name,
                                drt.tier_name,
                                p2.specialty AS previous_specialty_encounter,
                                dnt.need_name AS specialty_need_name,
                                pe.needs,
                                e.encounter_date,
                                date (pe.last_evaluated_at) AS last_evaluated_at,
                                now()::date - date (pe.last_evaluated_at)::date AS days_since_last_evaluation,
                                substring(
                                        pe.needs
                                        FROM
                                                '[0-9]+'
                                )::INTEGER AS cadence_days
                        FROM
                                core.patients p
                                LEFT JOIN care.patient_evaluation pe ON pe.patient_id = p.id
                                LEFT JOIN core.encounters e ON p.id = e.patient_id
                                LEFT JOIN core.providers p2 ON p2.id = p.pcp_provider_id
                                LEFT JOIN care.dim_need_types dnt ON dnt.id = pe.specialty_id
                                LEFT JOIN care.dim_program dp ON dp.id = pe.program_id
                                LEFT JOIN care.dim_risk_tier drt ON drt.id = pe.risk_tier_id
                        ORDER BY
                                p.id
                ),
                max_encounter AS (
                        SELECT
                                patient_id,
                                max(encounter_date) AS max_encounter_date
                        FROM
                                base
                        GROUP BY
                                patient_id
                ),
                final_base AS (
                        SELECT
                                b.*
                        FROM
                                base b
                                LEFT JOIN max_encounter me ON me.patient_id = b.patient_id
                        WHERE
                                b.encounter_date = me.max_encounter_date
                )
        SELECT
                row_number() OVER () AS row_id,
                b.*,
                (
                        CASE
                                WHEN program_name = 'Diabetes Management'
                                AND b.specialty_need_name != b.previous_specialty_encounter THEN 'Referral Task'
                                WHEN program_name = 'Diabetes Management'
                                AND b.days_since_last_evaluation > b.cadence_days THEN 'Scheduling Task'
                                WHEN program_name = 'Primary Care Wellness'
                                AND b.days_since_last_evaluation > b.cadence_days THEN 'Scheduling Task'
                                ELSE 'N/A'
                        END
                ) AS task_type
        FROM
                final_base b;
    """)


def downgrade() -> None:
    """Drop View: patient_evaluation_needs"""
    op.execute("DROP VIEW IF EXISTS care.patient_evaluation_needs")
