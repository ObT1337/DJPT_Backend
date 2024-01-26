import styled, { css } from "styled-components";
export const MenuContextContainer = styled.div`
  border: 1px solid #ffffff2d;
  border-radius: 4px;
  padding: 18px;
  margin: 5px 0;
  box-sizing: border-box;
`;

interface ContextMenuProps {
  top: number;
  left: number;
}

export const ContextMenu = styled.div<ContextMenuProps>`
  position: absolute;
  width: 200px;
  background-color: #383838;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 20px;

  ${({ top, left }) => css`
    top: ${top}px;
    left: ${left}px;
  `}

  ul {
    box-sizing: border-box;
    padding: 10px;
    margin: 0;
    list-style: none;
  }

  ul li {
    padding: 18px 12px;
  }

  /* hover */
  ul li:hover {
    cursor: pointer;
    background-color: #000000;
  }

  z-index: 1;
`;