// components/MainComponent.js
import React from 'react';
import AudioPlayer from '../AudioPlayer/AudioPlayer.js';
import dataJSON from "../TableComponent/Columns/defaultData.json";
import TableComponent from '../TableComponent/TableComponent.tsx';
const MainComponent = () => {
  const [tracks, setTracks] = React.useState(() => [...dataJSON]);
  const [receivedData, setReceivedData] = React.useState(false);
  const [trackIndex, setTrackIndex] = React.useState(0);
  const [currentTrack, setCurrentTrack] = React.useState(
    tracks[trackIndex]
  );

  const setCurrentTrackByIndex = (index) => {
    setTrackIndex(index)
    setCurrentTrack(tracks[trackIndex])

  }

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/data');
        const result = await response.json();
        setTracks(result);
        setCurrentTrack(result[0]); // Set the first track as the current track
        setReceivedData(true)
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []); // Empty dependency array ensures useEffect runs only once on component mount
  console.log(tracks)

  if (!receivedData) {
    return <p>Loading....</p>
  }
  return (
    <div>
      <AudioPlayer  {...{ tracks, trackIndex, setTrackIndex, currentTrack, setCurrentTrack }} />
      <TableComponent {...{ tracks, setCurrentTrackByIndex }} />
    </div>
  );
}


export default MainComponent;
