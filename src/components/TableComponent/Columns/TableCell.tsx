import React from "react";
import styles from "../TableComponent.module.css";

const TableCell = ({ getValue, row, column, table }) => {
  const initialValue = getValue()
  const [value, setValue] = React.useState(initialValue)
  const tableMeta = table.options.meta
  React.useEffect(() => {
    setValue(initialValue)
  }, [initialValue])


  const onBlur = () => {
    tableMeta.updateData(row.index, column.id, value)
    console.log("blur", row.id, column.id, value)
    // TODO: Send updated data to backend
  }

  const onDoubleClick = () => {
    tableMeta.setEditRow(row.id);
    tableMeta.setEditCol(column.id);
  };

  const highlightRow = () => {
    tableMeta.setSelectedRow(row.id)
  }

  //   TODO:
  //   Handle triple click
  //   class Test extends React.Component{
  //     onClick(e){
  //         console.log(e.detail === 3? "tripple click" : "not tripple click");
  //     }
  //     render(){
  //         return <div onClick={this.onClick}>click</div>;
  //     }
  // }

  const handleClickOutside = (event) => {
    if (
      tableMeta.editRow &&
      tableMeta.editCol &&
      !event.target.closest(`.${styles.tableInput}`)
    ) {
      tableMeta.setEditRow(null)
      tableMeta.setEditCol(null)
      tableMeta.setSelectedRow(null)
    };
  };
  const inputDiv = (
    <input
      className={styles.tableInput}
      value={value}
      onChange={(e) => setValue(e.target.value)}
      onBlur={onBlur}
      type={column.columnDef.meta?.type || "text"}
      style={{ minWidth: "100 %" }}
    />
  )

  React.useEffect(() => {
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [tableMeta, row.id, column.id]);
  if (tableMeta?.editRow == row.id && tableMeta.editCol == column.id) {
    return inputDiv;
  }

  return <span onDoubleClick={onDoubleClick} onClick={highlightRow} style={{ cursor: "pointer", width: "100%", float: "left", display: "inline-block" }}>&nbsp;
    {value}
  </span>
}

export default TableCell;