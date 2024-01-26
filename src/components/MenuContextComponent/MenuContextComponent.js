import { default as React, useEffect, useState } from "react";
import Menu from "./Menu";
import { ContextMenu } from "./MenuContextComponent.style.js";
const MenuContext = ({ data }) => {
    const [clicked, setClicked] = useState(false);
    const [points, setPoints] = useState({
        x: 0,
        y: 0,
    });
    useEffect(() => {
        const handleClick = () => setClicked(false);
        window.addEventListener("click", handleClick);
        return () => {
            window.removeEventListener("click", handleClick);
        };
    }, []);
    return (
        <div>
            {data.map((item) => (
                <div
                    onContextMenu={(e) => {
                        e.preventDefault();
                        setClicked(true);
                        setPoints({
                            x: e.pageX,
                            y: e.pageY,
                        });
                        console.log("Right Click", e.pageX, e.pageY);
                    }}
                >
                    <Menu id={item.id} title={item.title} />
                </div>
            ))}
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
        </div >
    );
};
export default MenuContext;