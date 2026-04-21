import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { fetchDashboardSummary } from "../api/dashboardApi"
import type { DashboardSummary } from "../types/dashboard"

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardSummary().then((data) => {
      setSummary(data)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return <div className="status-message">Loading dashboard...</div>
  }

  if (!summary) {
    return <div className="error-message">Error: Unknown dashboard error</div>
  }

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Dashboard</h1>
        <p>Overview of evaluation rows from the API.</p>
      </header>

      <section className="stats-grid" aria-label="Dashboard summary">
        <article className="stat-card">
          <h2>Total Evaluation Rows</h2>
          <p>{summary.totalEvaluationRows ?? "Unavailable"}</p>
        </article>
        <article className="stat-card">
          <h2>Unique Patients</h2>
          <p>{summary.uniquePatients ?? "Unavailable"}</p>
        </article>
        <article className="stat-card">
          <h2>Unique Programs</h2>
          <p>{summary.uniquePrograms ?? "Unavailable"}</p>
        </article>
        <article className="stat-card">
          <h2>Unique Task Types</h2>
          <p>{summary.uniqueTaskTypes ?? "Unavailable"}</p>
        </article>
      </section>

      {summary.evaluationError && (
        <section className="panel error-panel">
          <h2>Evaluation data unavailable</h2>
          <p>{summary.evaluationError}. Expected endpoint: `GET /api/evaluation/`.</p>
        </section>
      )}

      <section className="panel quick-links">
        <h2>Quick Links</h2>
        <div className="quick-links-row">
          <Link className="quick-link" to="/patients">
            View Patients
          </Link>
          <Link className="quick-link" to="/tasks">
            View Tasks
          </Link>
        </div>
      </section>
    </div>
  )
}
