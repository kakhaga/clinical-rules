type PaginationControlsProps = {
  page: number
  pageSize: number
  pageSizeOptions: number[]
  isNextDisabled: boolean
  isPreviousDisabled?: boolean
  onPageChange: (nextPage: number) => void
  onPageSizeChange: (nextPageSize: number) => void
}

export default function PaginationControls({
  page,
  pageSize,
  pageSizeOptions,
  isNextDisabled,
  isPreviousDisabled = page <= 1,
  onPageChange,
  onPageSizeChange,
}: PaginationControlsProps) {
  return (
    <div className="pagination-controls" role="navigation" aria-label="Pagination">
      <div className="pagination-buttons">
        <button
          type="button"
          onClick={() => onPageChange(page - 1)}
          disabled={isPreviousDisabled}
        >
          Previous
        </button>
        <span>Page {page}</span>
        <button
          type="button"
          onClick={() => onPageChange(page + 1)}
          disabled={isNextDisabled}
        >
          Next
        </button>
      </div>

      <label className="page-size-selector">
        Page size
        <select
          value={pageSize}
          onChange={(event) => onPageSizeChange(Number(event.target.value))}
        >
          {pageSizeOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
    </div>
  )
}
