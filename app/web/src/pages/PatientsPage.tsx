import { useEffect, useState } from "react"
import type { FormEvent } from "react"
import PaginationControls from "../components/PaginationControls"
import { fetchPatientById, fetchPatients } from "../api/patientsApi"
import type { Patient } from "../types/patient"

const PAGE_SIZE_OPTIONS = [10, 25, 50, 100]

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(25)
  const [hasNextPage, setHasNextPage] = useState(false)

  const [patientIdInput, setPatientIdInput] = useState("")
  const [patientIdLookup, setPatientIdLookup] = useState<number | null>(null)

  useEffect(() => {
    let isCancelled = false

    async function loadPatients() {
      setLoading(true)
      setError(null)

      try {
        if (patientIdLookup !== null) {
          const patient = await fetchPatientById(patientIdLookup)
          if (!isCancelled) {
            setPatients([patient])
            setHasNextPage(false)
          }
          return
        }

        const skip = (page - 1) * pageSize
        const list = await fetchPatients({ skip, limit: pageSize })

        if (!isCancelled) {
          setPatients(list)
          setHasNextPage(list.length === pageSize)
        }
      } catch (err) {
        if (!isCancelled) {
          setPatients([])
          setHasNextPage(false)

          const message = err instanceof Error ? err.message : "Failed to load patients"
          if (patientIdLookup !== null && message.includes("404")) {
            setError(`No record found for patient ID ${patientIdLookup}`)
          } else {
            setError(message)
          }
        }
      } finally {
        if (!isCancelled) {
          setLoading(false)
        }
      }
    }

    void loadPatients()

    return () => {
      isCancelled = true
    }
  }, [page, pageSize, patientIdLookup])

  function onPatientSearchSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    const trimmed = patientIdInput.trim()

    if (!trimmed) {
      setPatientIdLookup(null)
      setPage(1)
      return
    }

    const patientId = Number(trimmed)
    if (!Number.isInteger(patientId) || patientId <= 0) {
      setError("Patient ID must be a positive integer")
      return
    }

    setPatientIdLookup(patientId)
  }

  function clearPatientSearch() {
    setPatientIdInput("")
    setPatientIdLookup(null)
    setError(null)
    setPage(1)
  }

  const isLookupMode = patientIdLookup !== null

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Patients</h1>
        <p>Patient records returned by the API service.</p>
      </header>

      <section className="filters-card">
        <form onSubmit={onPatientSearchSubmit}>
          <div className="filters-grid single-row">
            <label>
              Search by Patient ID
              <input
                value={patientIdInput}
                onChange={(event) => setPatientIdInput(event.target.value)}
                placeholder="e.g. 123"
                inputMode="numeric"
              />
            </label>
          </div>
          <div className="filters-actions">
            <button type="submit">Search</button>
            <button type="button" className="secondary" onClick={clearPatientSearch}>
              Clear Search
            </button>
          </div>
        </form>
      </section>

      {loading && <div className="status-message">Loading patients...</div>}
      {error && <div className="error-message">Patients: {error}</div>}

      {!loading && !error && patients.length === 0 && (
        <div className="empty-state">
          {isLookupMode
            ? `No record found for patient ID ${patientIdLookup}`
            : "No patients found for this page."}
        </div>
      )}

      {!loading && !error && patients.length > 0 && (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>External ID</th>
                  <th>Name</th>
                  <th>Date of Birth</th>
                  <th>Gender</th>
                  <th>Phone</th>
                  <th>Language</th>
                </tr>
              </thead>
              <tbody>
                {patients.map((patient) => (
                  <tr key={patient.id}>
                    <td>{patient.id}</td>
                    <td>{patient.external_patient_id}</td>
                    <td>{`${patient.first_name} ${patient.last_name}`}</td>
                    <td>{patient.date_of_birth}</td>
                    <td>{patient.gender ?? "-"}</td>
                    <td>{patient.phone ?? "-"}</td>
                    <td>{patient.language ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {!isLookupMode && (
            <PaginationControls
              page={page}
              pageSize={pageSize}
              pageSizeOptions={PAGE_SIZE_OPTIONS}
              isNextDisabled={!hasNextPage}
              onPageChange={setPage}
              onPageSizeChange={(nextPageSize) => {
                setPageSize(nextPageSize)
                setPage(1)
              }}
            />
          )}
        </>
      )}
    </div>
  )
}
