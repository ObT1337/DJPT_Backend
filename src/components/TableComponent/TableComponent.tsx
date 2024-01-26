import { ColumnOrderState, SortingState, flexRender, getCoreRowModel, getFilteredRowModel, getSortedRowModel, useReactTable } from "@tanstack/react-table";
import React from "react";
import { ContextMenu } from "../MenuContextComponent/MenuContextComponent.style.tsx";
import { columns } from "./Columns/Columns.ts";
import styles from "./TableComponent.module.css";
const TableComponent = ({ tracks, setCurrentTrackByIndex }) => {
    const [data, setData] = React.useState(() => [...tracks]);
    const [editRow, setEditRow] = React.useState();
    const [editCol, setEditCol] = React.useState();
    const [selectedRow, setSelectedRow] = React.useState<null | string>(null);
    const [resizingColumnId, setResizingColumnId] = React.useState(null)
    const [sorting, setSorting] = React.useState<SortingState>([]);
    const [filtering, setFiltering] = React.useState("");
    const [columnVisibility, setColumnVisibility] = React.useState({});
    const [columnOrder, setColumnOrder] = React.useState<ColumnOrderState>([])
    let columnBeingDragged: number;
    let rowBeingDragged: number;
    const [clicked, setClicked] = React.useState(false);
    const [points, setPoints] = React.useState({
        x: 0,
        y: 0,
    });
    console.log(tracks)
    // const rerender = React.useReducer(() => ({}), {})[1]
    const columnResizeMode = 'onChange'
    const columnResizeDirection = 'ltr'
    const table = useReactTable({
        columns: columns,
        data: data,
        enableColumnResizing: true,
        columnResizeMode: columnResizeMode,
        columnResizeDirection: columnResizeDirection,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        state: {
            sorting: sorting,
            globalFilter: filtering,
            columnVisibility: columnVisibility,
            columnOrder: columnOrder,
        },
        meta: {
            updateData: (rowIndex: number, columnId: string, value: string) => {
                setData((old) =>
                    old.map((row, index) => {
                        if (index === rowIndex) {
                            return {
                                ...old[rowIndex],
                                [columnId]: value,
                            };
                        }
                        return row;
                    })
                );
            },
            editRow,
            editCol,
            selectedRow,
            setEditRow,
            setEditCol,
            setSelectedRow,
        },
        onSortingChange: setSorting,
        onGlobalFilterChange: setFiltering,
        onColumnVisibilityChange: setColumnVisibility,
        onColumnOrderChange: setColumnOrder,
        debugTable: true,
        debugHeaders: true,
        debugColumns: true,
        enableSorting: true
    })

    const onRowDragStart = (e) => {
        rowBeingDragged = Number(e.currentTarget.dataset.columnIndex);
        console.log(rowBeingDragged)
    }
    const onDropRow = (e) => {
        e.preventDefault();
        const newPosition = Number(e.currentTarget.dataset.rowIndex);
        // data.findIndex(rowBeingDragged)

    }

    const onDragStart = (e) => {
        columnBeingDragged = Number(e.currentTarget.dataset.columnIndex);
    };
    const onDrop = (e) => {
        e.preventDefault();
        const newPosition = Number(e.currentTarget.dataset.columnIndex);
        const currentCols = table.getVisibleLeafColumns().map((c) => c.id);
        const colToBeMoved = currentCols.splice(columnBeingDragged, 1);

        currentCols.splice(newPosition, 0, colToBeMoved[0]);
        table.setColumnOrder(currentCols);
    }
    const colToggle = (
        <div key="ColToggle" style={{ display: "flex" }}>
            <hr />
            <div key="AllColToggle">

                <label>
                    <input
                        {...{
                            type: "checkbox",
                            checked: table.getIsAllColumnsVisible(),
                            onChange: table.getToggleAllColumnsVisibilityHandler(),
                        }}
                    />{" "}
                    Toggle All
                </label>
            </div>
            <hr />
            <div key="IndividualColToggle">
                {table.getAllLeafColumns().map((column) => {
                    return (
                        <div style={{
                            display: "inline-block",
                            position: "relative",
                            left: "0",
                        }} key={column.id}>
                            <label >
                                <input
                                    {...{
                                        type: "checkbox",
                                        checked: column.getIsVisible(),
                                        onChange: column.getToggleVisibilityHandler(),
                                    }}
                                />{" "}
                                {column.id}
                            </label>
                        </div>
                    );
                })}

            </div>
            <hr />
        </div>
    )
    const searchPanel = (
        <div key="GlobalFilter" style={{ alignContent: "left" }}>
            <input type="text" value={filtering} onChange={e => setFiltering(e.target.value)} />
        </div>
    )
    const theadDiv = (<thead>
        {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                    <th
                        key={header.id}
                        style={{
                            width: header.isPlaceholder
                                ? '0px'
                                : resizingColumnId === header.id
                                    ? header.column.getSize() + (table.getState().columnSizingInfo.deltaOffset ?? 0)
                                    : header.getSize(),
                        }}
                        draggable={
                            !table.getState().columnSizingInfo.isResizingColumn
                        }
                        data-column-index={header.index}
                        onDragStart={onDragStart}
                        onDragOver={(e) => {
                            e.preventDefault();
                        }}
                        onDrop={onDrop}
                    >
                        <div
                            {...{
                                className: header.column.getCanSort()
                                    ? 'cursor-pointer grabbable select-none'
                                    : '',
                                onClick: header.column.getToggleSortingHandler(),
                            }}
                        >
                            {flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                            )}
                            {{
                                asc: '⬆︎',
                                desc: '⬇︎',
                            }[header.column.getIsSorted() as string] ?? null}
                        </div>
                        <div
                            {...{
                                onDoubleClick: () => header.column.resetSize(),
                                onMouseDown: header.getResizeHandler()
                                ,
                                onTouchStart: header.getResizeHandler()
                                ,
                                className: `${styles.resizer} ${table.options.columnResizeDirection}`,
                                style: {
                                    transform: resizingColumnId === header.id
                                        ? `translateX(${(table.options.columnResizeDirection === 'rtl' ? -1 : 1) *
                                        (table.getState().columnSizingInfo.deltaOffset ?? 0)}px)`
                                        : '',
                                },
                            }}
                        />
                    </th>
                ))}
            </tr>
        ))}
    </thead>)
    const tbodyDiv = (
        <tbody>
            {table.getRowModel().rows.map(row => (
                < tr
                    draggable={true}
                    key={row.id}
                    className={`${selectedRow === row.id ? styles.selectedRow : ''}`}
                    onClick={() => setSelectedRow(row.id)} onDoubleClick={() => setCurrentTrackByIndex(row.id)}>

                    {row.getVisibleCells().map(cell => (
                        <td key={cell.id}>
                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </td>
                    ))}
                </tr>
            ))
            }
        </tbody >
    )
    const tfootDiv = (
        <tfoot>
            {table.getFooterGroups().map(footerGroup => (
                <tr key={footerGroup.id}>
                    {footerGroup.headers.map(header => (
                        <th className={`footer`} key={header.id}>
                            {header.isPlaceholder
                                ? null
                                : flexRender(
                                    header.column.columnDef.footer,
                                    header.getContext()
                                )}
                        </th>
                    ))}
                </tr>
            ))}
        </tfoot>
    )
    const tableDiv = (
        <table
            className={styles.table}
            style={{ width: table.getCenterTotalSize() }}
            onContextMenu={(e) => {
                e.preventDefault();
                setClicked(true);
                setPoints({
                    x: e.pageX,
                    y: e.pageY,
                });
                console.log("Right Click", e.pageX, e.pageY);
            }}
            onClick={() => {
                setClicked(false);
            }}>
            {clicked && (
                <ContextMenu top={points.y} left={points.x}>
                    <ul>
                        <li>Add to Playlist</li>
                        <li>Play next</li>
                        <li>Playback later</li>
                        <hr />
                        <li>Information</li>
                        <li>Favorite</li>
                        <li>Show Album</li>
                        <hr />
                        <li>Copy</li>
                        <li>Download</li>
                        <li>Delete</li>
                    </ul>
                </ContextMenu>
            )
            }
            {theadDiv}
            {tbodyDiv}
            {tfootDiv}
        </table>
    )
    return (
        <>
            <div onContextMenu={(e) => {
                e.preventDefault();
                console.log("Right Click", e.pageX, e.pageY);
            }}>
                {colToggle}
                {searchPanel}
                <div style={{ direction: table.options.columnResizeDirection }}>
                    {tableDiv}
                </div>
            </div >
        </>
    )
}
export default TableComponent;