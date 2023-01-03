import { useMapEvents } from "react-leaflet"

function MyComponent() {
  const map = useMapEvents({
    click: (e) => {
      console.log(e.latlng.lng)
      console.log(e.latlng.lat)
    },
    locationfound: (location) => {
      console.log('location found:', location)
    },
  })
  return null
}

export default MyComponent;