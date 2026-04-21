export type Patient = {
  id: number
  external_patient_id: string
  first_name: string
  last_name: string
  date_of_birth: string
  gender: string | null
  phone: string | null
  language: string | null
  pcp_provider_id: number | null
}
