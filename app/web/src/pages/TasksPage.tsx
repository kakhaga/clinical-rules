import { useEffect, useState } from "react"
import type { FormEvent } from "react"
import PaginationControls from "../components/PaginationControls"
import {
  fetchTaskEvaluationByPatientId,
  fetchTasks,
  type TaskQueryParams,
} from "../api/tasksApi"
import {
  PROGRAM_NAME_OPTIONS,
  SPECIALTY_NEED_OPTIONS,
  TASK_TYPE_OPTIONS,
} from "../constants/evaluationFilters"
import type { Task } from "../types/task"
import {
  filterVisibleWorklistRows,
  type WorklistView,
} from "../utils/taskVisibility"

const PAGE_SIZE_OPTIONS = [10, 25, 50, 100]

const DEFAULT_FILTERS: Pick<
  TaskQueryParams,
  "task_type" | "specialty_need_name" | "program_name"
> = {
  task_type: "",
  specialty_need_name: "",
  program_name: "",
}

function formatDate(value: string | null): string {
  if (!value) {
    return "-"
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleDateString()
}

function formatCadenceDays(cadenceDays: number | null): string {
  if (cadenceDays === null) {
    return "-"
  }

  return `${cadenceDays} days`
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(25)
  const [hasNextPage, setHasNextPage] = useState(false)

  const [filtersInput, setFiltersInput] = useState(DEFAULT_FILTERS)
  const [appliedFilters, setAppliedFilters] = useState(DEFAULT_FILTERS)

  const [patientIdInput, setPatientIdInput] = useState("")
  const [patientIdLookup, setPatientIdLookup] = useState<number | null>(null)

  const [worklistView, setWorklistView] = useState<WorklistView>("clinical_team")

  useEffect(() => {
    let isCancelled = false

    async function loadTasks() {
      setLoading(true)
      setError(null)

      try {
        if (patientIdLookup !== null) {
          const rows = await fetchTaskEvaluationByPatientId(patientIdLookup)
          const visibleRows = filterVisibleWorklistRows(rows, worklistView)

          if (!isCancelled) {
            setTasks(visibleRows)
            setHasNextPage(false)
          }
          return
        }

        const skip = (page - 1) * pageSize
        const rows = await fetchTasks({
          skip,
          limit: pageSize,
          task_type: appliedFilters.task_type || undefined,
          specialty_need_name: appliedFilters.specialty_need_name || undefined,
          program_name: appliedFilters.program_name || undefined,
        })

        const visibleRows = filterVisibleWorklistRows(rows, worklistView)

        if (!isCancelled) {
          setTasks(visibleRows)
          setHasNextPage(visibleRows.length === pageSize)
        }
      } catch (err) {
        if (!isCancelled) {
          setTasks([])
          setHasNextPage(false)

          const message =
            err instanceof Error ? err.message : "Failed to load evaluation tasks"

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

    void loadTasks()

    return () => {
      isCancelled = true
    }
  }, [page, pageSize, appliedFilters, patientIdLookup, worklistView])

  function onFilterSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)
    setAppliedFilters(filtersInput)
    setPatientIdLookup(null)
    setPatientIdInput("")
    setPage(1)
  }

  function resetAll() {
    setFiltersInput(DEFAULT_FILTERS)
    setAppliedFilters(DEFAULT_FILTERS)
    setPatientIdInput("")
    setPatientIdLookup(null)
    setError(null)
    setPage(1)
  }

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

  const isLookupMode = patientIdLookup !== null

  return (
    <div className="page-container tasks-page">
      <header className="page-header">
        <h1>Tasks</h1>
        <p>Evaluation worklist with scheduling/referral context from backend evaluation rows.</p>
      </header>

      <section className="filters-card">
        <div className="worklist-toggle" role="tablist" aria-label="Worklist View">
          <button
            type="button"
            role="tab"
            aria-selected={worklistView === "clinical_team"}
            className={
              worklistView === "clinical_team"
                ? "worklist-toggle-btn active"
                : "worklist-toggle-btn"
            }
            onClick={() => {
              setWorklistView("clinical_team")
              setPage(1)
            }}
          >
            Clinical Team
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={worklistView === "scheduler"}
            className={
              worklistView === "scheduler"
                ? "worklist-toggle-btn active"
                : "worklist-toggle-btn"
            }
            onClick={() => {
              setWorklistView("scheduler")
              setPage(1)
            }}
          >
            Scheduler
          </button>
        </div>

        <p className="worklist-helper">
          Clinical Team: referral + scheduling tasks. Scheduler: scheduling-only worklist.
        </p>

        <form onSubmit={onPatientSearchSubmit}>
          <div className="filters-grid single-row">
            <label>
              Get evaluation by Patient ID
              <input
                value={patientIdInput}
                onChange={(event) => setPatientIdInput(event.target.value)}
                placeholder="e.g. 123"
                inputMode="numeric"
              />
            </label>
          </div>
          <div className="filters-actions">
            <button type="submit">Search Patient</button>
            <button type="button" className="secondary" onClick={resetAll}>
              Reset All
            </button>
          </div>
        </form>
      </section>

      <section className="filters-card">
        <form onSubmit={onFilterSubmit}>
          <div className="filters-grid">
            <label>
              Program Name
              <select
                value={filtersInput.program_name}
                onChange={(event) =>
                  setFiltersInput((prev) => ({
                    ...prev,
                    program_name: event.target.value,
                  }))
                }
              >
                <option value="">All</option>
                {PROGRAM_NAME_OPTIONS.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Specialty Need Name
              <select
                value={filtersInput.specialty_need_name}
                onChange={(event) =>
                  setFiltersInput((prev) => ({
                    ...prev,
                    specialty_need_name: event.target.value,
                  }))
                }
              >
                <option value="">All</option>
                {SPECIALTY_NEED_OPTIONS.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Task Type
              <select
                value={filtersInput.task_type}
                onChange={(event) =>
                  setFiltersInput((prev) => ({
                    ...prev,
                    task_type: event.target.value,
                  }))
                }
              >
                <option value="">All</option>
                {TASK_TYPE_OPTIONS.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="filters-actions">
            <button type="submit">Apply Filters</button>
            <button type="button" className="secondary" onClick={resetAll}>
              Clear Filters
            </button>
          </div>
        </form>
      </section>

      {loading && <div className="status-message">Loading evaluation rows...</div>}
      {error && <div className="error-message">Tasks/Evaluation: {error}</div>}

      {!loading && !error && tasks.length === 0 && (
        <div className="empty-state">
          {isLookupMode
            ? `No record found for patient ID ${patientIdLookup} in the selected worklist view.`
            : "No worklist rows found for the current view, filters, and page."}
        </div>
      )}

      {!loading && !error && tasks.length > 0 && (
        <>
          <div className="table-wrapper">
            <table className="task-table">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Task Type</th>
                  <th>Program</th>
                  <th>Specialty Need</th>
                  <th>Tier</th>
                  <th>Needs</th>
                  <th>Cadence</th>
                  <th>Last Eval</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.row_id}>
                    <td className="cell-mono">{task.patient_id}</td>
                    <td>{task.task_type ?? "-"}</td>
                    <td className="cell-wrap">{task.program_name ?? "-"}</td>
                    <td className="cell-wrap">{task.specialty_need_name ?? "-"}</td>
                    <td className="cell-wrap">{task.tier_name ?? "-"}</td>
                    <td className="cell-wrap">{task.needs ?? "-"}</td>
                    <td>{formatCadenceDays(task.cadence_days)}</td>
                    <td>{formatDate(task.last_evaluated_at)}</td>
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
