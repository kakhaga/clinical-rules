import { createBrowserRouter } from "react-router-dom"
import AppLayout from "../components/AppLayout"
import DashboardPage from "../pages/DashboardPage"
import PatientsPage from "../pages/PatientsPage"
import TasksPage from "../pages/TasksPage"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "patients",
        element: <PatientsPage />,
      },
      {
        path: "tasks",
        element: <TasksPage />,
      },
    ],
  },
])
