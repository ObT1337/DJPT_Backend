import { createColumnHelper } from "@tanstack/react-table";
import TableCell from "./TableCell.tsx";
export type Track = {
    id: number,
    title: string,
    artist: string,
    album: string,
    duration: string,
    bpm: number,
    genre: string,
    openKey: string,
    musicalKey: string,
    musicalKeySharps: string,
    added: string,
    date: string,
    playCount: number,
    fileLocation: string,
};

const columnHelper = createColumnHelper<Track>();

export const columns = [
    columnHelper.accessor('id', {
        cell: info => info.getValue(),
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor('title', {
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor('artist', {
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor('album', {
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor('duration', {
        cell: info => info.getValue(),
    }),
    columnHelper.accessor('bpm', {
        cell: TableCell,
        meta: {
            type: "number",
        },
    }),
    columnHelper.accessor('genre', {
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor('openKey', {
        cell: TableCell,
        meta: {
            type: "text",
        },
    }),
    columnHelper.accessor('added', {
        cell: info => info.getValue(),
    }),
    columnHelper.accessor('date', {
        cell: info => info.getValue(),
    }),
    columnHelper.accessor('playCount', {
        cell: info => info.getValue(),
    }),
    columnHelper.accessor('fileLocation', {
        cell: info => info.getValue(),
    }),
]
export default columns;