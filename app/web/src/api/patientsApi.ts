import type { Patient } from "../types/patient"

export type PatientQueryParams = {
  skip?: number
  limit?: number
}

function buildPatientsUrl(params: PatientQueryParams = {}) {
  const searchParams = new URLSearchParams()

  if (params.skip !== undefined) searchParams.set("skip", String(params.skip))
  if (params.limit !== undefined) searchParams.set("limit", String(params.limit))

  const query = searchParams.toString()
  return `/api/patients/${query ? `?${query}` : ""}`
}

export async function fetchPatients(
  params: PatientQueryParams = {}
): Promise<Patient[]> {
  const response = await fetch(buildPatientsUrl(params), {
    headers: { Accept: "application/json" },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch patients: ${response.status}`)
  }

  return response.json()
}

export async function fetchPatientById(patientId: number): Promise<Patient> {
  const response = await fetch(`/api/patients/${patientId}`, {
    headers: { Accept: "application/json" },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch patient ${patientId}: ${response.status}`)
  }

  return response.json()
}
