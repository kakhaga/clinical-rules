export type Task = {
  row_id: number
  patient_id: number
  program_name: string | null
  tier_name: string | null
  previous_specialty_encounter: string | null
  specialty_need_name: string | null
  needs: string | null
  encounter_date: string | null
  last_evaluated_at: string | null
  days_since_last_evaluation: number | null
  cadence_days: number | null
  task_type: string | null
}
