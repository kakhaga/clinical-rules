import { fetchTasks } from "./tasksApi"
import type { DashboardSummary } from "../types/dashboard"

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  try {
    const evaluations = await fetchTasks({ skip: 0, limit: 1000 })

    const uniquePatients = new Set(evaluations.map((row) => row.patient_id)).size
    const uniquePrograms = new Set(
      evaluations
        .map((row) => row.program_name)
        .filter((value): value is string => Boolean(value))
    ).size
    const uniqueTaskTypes = new Set(
      evaluations
        .map((row) => row.task_type)
        .filter((value): value is string => Boolean(value))
    ).size

    return {
      totalEvaluationRows: evaluations.length,
      uniquePatients,
      uniquePrograms,
      uniqueTaskTypes,
      evaluationError: null,
    }
  } catch (error) {
    return {
      totalEvaluationRows: null,
      uniquePatients: null,
      uniquePrograms: null,
      uniqueTaskTypes: null,
      evaluationError:
        error instanceof Error ? error.message : "Failed to fetch evaluation rows",
    }
  }
}
