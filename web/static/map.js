const copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osm = L.tileLayer(url, { attribution: copy })
const map = L.map('map', { layers: [osm], minZoom: 5 })
map.locate()
  .on('locationfound', e => map.setView(e.latlng, 14))
  .on('locationerror', () => map.setView([60.170823591711397, 24.942526799246199], 12))
map.fitWorld();

async function load_stations() {
    const stations_url = `/api/stations/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(stations_url)
    const geojson = await response.json()
    return geojson
  }
  async function render_stations() {
    const stations = await load_stations()
    L.geoJSON(stations).bindPopup(layer => layer.feature.properties.name).addTo(map)
  }
  map.on('moveend', render_stations)