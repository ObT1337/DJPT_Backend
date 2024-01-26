import { columnHelper, getCoreRowModel, getPaginationRowModel, getSortedRowModel, useReactTable } from '@tanstack/react-table';
import React from "react";
import styles from "./TableComponent.module.css";
const TableComponent = ({ data, columns, theme }) => {
    const defaultColumn = React.useMemo(
        () => ({
            minWidth: 30,
            width: 150,
            maxWidth: 400
        }),
        []
    );
    const table = useReactTable({ columns, data })
    // Use the state and functions returned from useTable to build your UI
    const tableInstance = useReactTable({
        columns,
        data,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        getSortedRowModel: getSortedRowModel(), //order doesn't matter anymore!
        // etc.
    })
    columnHelper.accessor('firstName', {//accessorKey
        header: 'First Name',
    })
    return (
        <div>
            <button onClick={resetResizing}>Reset Resizing</button>
            <table {...getTableProps()} className={`${styles.table} ${theme}`}>
                <thead>
                    {headerGroups.map((headerGroup) => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map((column) => (
                                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                                    {column.render("Header")}
                                    <div
                                        {...column.getResizerProps()}
                                        className={`${styles.resizer} ${column.isResizing ? `${styles.isResizing}` : ""
                                            }`}
                                    />
                                    <span>
                                        {column.isSorted ? (column.isSortedDesc ? '⬆︎' : '⬇︎') : ''}
                                    </span>
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map((row, i) => {
                        prepareRow(row);
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map((cell) => {
                                    return (
                                        <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                                    );
                                })}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div >
    );
};

export default TableComponent;