import React from "react";
import { MenuContextContainer } from "./MenuContextComponent.style";
const Menu = ({ title, key }) => {
  return (
    <>
      <MenuContextContainer key={key}>{title}</MenuContextContainer >
    </>
  );
};
export default Menu;

export const mainMenu = [
  {
    id: 1,
    title: "Message 1",
  },
  {
    id: 2,
    title: "Message 2",
  },
  {
    id: 3,
    title: "Message 3",
  },
  {
    id: 4,
    title: "Message 4",
  },
];