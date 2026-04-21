import type { Task } from "../types/task"

export type TaskQueryParams = {
  skip?: number
  limit?: number
  program_name?: string
  specialty_need_name?: string
  task_type?: string
}

function buildTasksUrl(params: TaskQueryParams = {}) {
  const searchParams = new URLSearchParams()

  if (params.skip !== undefined) {
    searchParams.set("skip", String(params.skip))
  }

  if (params.limit !== undefined) {
    searchParams.set("limit", String(params.limit))
  }

  if (params.program_name) {
    searchParams.set("program_name", params.program_name)
  }

  if (params.specialty_need_name) {
    searchParams.set("specialty_need_name", params.specialty_need_name)
  }

  if (params.task_type) {
    searchParams.set("task_type", params.task_type)
  }

  const query = searchParams.toString()
  return `/api/evaluation/${query ? `?${query}` : ""}`
}

export async function fetchTasks(params: TaskQueryParams = {}): Promise<Task[]> {
  const response = await fetch(buildTasksUrl(params), {
    headers: {
      Accept: "application/json",
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch evaluation tasks: ${response.status}`)
  }

  return response.json()
}

export async function fetchTaskEvaluationByPatientId(
  patientId: number
): Promise<Task[]> {
  const response = await fetch(`/api/evaluation/${patientId}`, {
    headers: {
      Accept: "application/json",
    },
  })

  if (!response.ok) {
    throw new Error(
      `Failed to fetch evaluation for patient ${patientId}: ${response.status}`
    )
  }

  return response.json()
}
