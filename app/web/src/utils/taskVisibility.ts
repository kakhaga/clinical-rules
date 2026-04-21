import type { Task } from "../types/task"

export type WorklistView = "clinical_team" | "scheduler"

export function filterVisibleWorklistRows(
  rows: Task[],
  view: WorklistView
): Task[] {
  if (view === "scheduler") {
    return rows.filter((row) => row.task_type === "Scheduling Task")
  }

  return rows
}
