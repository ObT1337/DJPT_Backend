import React, { MouseEvent } from "react"
export const EditCell = ({ row, table }) => {
    const meta = table.options.meta
    const setEditedRows = (e: MouseEvent<HTMLButtonElement>) => {
      meta?.setEditedRows((old: []) => ({
        ...old,
        [row.id]: !old[row.id],
      }))
    }
    return meta?.editedRows[row.id] ? (
      <>
        <button>X</button> <button onClick={setEditedRows}>✔</button>
      </>
    ) : (
      <button onClick={setEditedRows}>✐</button>
    )
}
