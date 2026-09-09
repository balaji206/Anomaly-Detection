import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
  Polygon,
  Polyline,
  useMap,
  useMapEvents,
} from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix for default markers in React-Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdn.21st.dev/assets/mirror/00/00179c4c1ee830d3a108412ae0d294f55776cfeb085c60129a39aa6fc4ae2528.png",
  iconUrl:
    "https://cdn.21st.dev/assets/mirror/57/574c3a5cca85f4114085b6841596d62f00d7c892c7b03f28cbfa301deb1dc437.png",
  shadowUrl:
    "https://cdn.21st.dev/assets/mirror/26/264f5c640339f042dd729062cfc04c17f8ea0f29882b538e3848ed8f10edb4da.png",
});

// Custom marker icons
const createCustomIcon = (color = "blue", size: "small" | "medium" | "large" = "medium") => {
  const sizes: Record<string, [number, number]> = {
    small: [20, 32],
    medium: [25, 41],
    large: [30, 50],
  };

  return new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl:
      "https://cdn.21st.dev/assets/mirror/26/264f5c640339f042dd729062cfc04c17f8ea0f29882b538e3848ed8f10edb4da.png",
    iconSize: sizes[size],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });
};

// Smooth city navigation controller: flies to city coordinates whenever center changes
function RecenterMap({ center, zoom = 12 }: { center: [number, number]; zoom?: number }) {
  const map = useMap();

  useEffect(() => {
    if (!center || !Array.isArray(center) || center.length < 2) return;
    const [lat, lng] = center;
    if (typeof lat !== "number" || typeof lng !== "number") return;
    
    const timer = setTimeout(() => {
      map.invalidateSize();
      map.setView([lat, lng], zoom, { animate: true });
    }, 50);

    return () => clearTimeout(timer);
  }, [center[0], center[1], zoom, map]);

  return null;
}

// Map event handler component
const MapEvents = ({ onMapClick, onLocationFound }: any) => {
  const map = useMapEvents({
    click: (e) => {
      onMapClick && onMapClick(e.latlng);
    },
    locationfound: (e) => {
      onLocationFound && onLocationFound([e.latlng.lat, e.latlng.lng]);
      map.flyTo(e.latlng, map.getZoom(), { animate: true, duration: 1.2 });
    },
  });

  return null;
};

// Custom control component with stable reference to prevent re-creation
const CustomControls = ({ onToggleLayer }: any) => {
  const map = useMap();

  useEffect(() => {
    const control = (L as any).control({ position: "topright" });

    control.onAdd = () => {
      const div = L.DomUtil.create("div", "custom-controls");
      div.innerHTML = `
        <div style="background: rgba(15, 25, 50, 0.92); border: 1px solid #2e4372; color: #f1f5f9; padding: 6px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); font-size: 12px; display: flex; gap: 4px;">
          <button id="satellite-btn" style="background: #162447; border: 1px solid #2e4372; color: #2dd4bf; padding: 6px 10px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 12px;">🛰️ Satellite</button>
        </div>
      `;

      L.DomEvent.disableClickPropagation(div);

      const satelliteBtn = div.querySelector("#satellite-btn") as HTMLElement;

      if (satelliteBtn) satelliteBtn.onclick = () => onToggleLayer("satellite");

      return div;
    };

    control.addTo(map);

    return () => {
      control.remove();
    };
  }, [map]); // Stable dependencies prevent layout shaking

  return null;
};

export interface MapMarker {
  id?: string | number;
  position: [number, number];
  color?: string;
  size?: "small" | "medium" | "large";
  icon?: any;
  popup?: {
    title: string;
    content: string;
    image?: string;
  };
}

export interface AdvancedMapProps {
  center?: [number, number];
  zoom?: number;
  markers?: MapMarker[];
  polygons?: any[];
  circles?: any[];
  polylines?: any[];
  onMarkerClick?: (marker: MapMarker) => void;
  onMapClick?: (latlng: any) => void;
  enableClustering?: boolean;
  enableSearch?: boolean;
  enableControls?: boolean;
  mapLayers?: {
    openstreetmap: boolean;
    satellite: boolean;
    traffic: boolean;
  };
  className?: string;
  style?: React.CSSProperties;
}

// Main AdvancedMap component
export const AdvancedMap = ({
  center = [11.0168, 76.9558],
  zoom = 12,
  markers = [],
  polygons = [],
  circles = [],
  polylines = [],
  onMarkerClick,
  onMapClick,
  enableClustering = true,
  enableControls = true,
  mapLayers = {
    openstreetmap: true,
    satellite: false,
    traffic: false,
  },
  className = "",
  style = { height: "360px", width: "100%" },
}: AdvancedMapProps) => {
  const [currentLayers, setCurrentLayers] = useState(mapLayers);
  const [userLocation, setUserLocation] = useState<[number, number] | null>(null);
  const [clickedLocation, setClickedLocation] = useState<any>(null);

  // Handle layer toggling
  const handleToggleLayer = useCallback((layerType: string) => {
    setCurrentLayers((prev: any) => ({
      ...prev,
      [layerType]: !prev[layerType],
    }));
  }, []);

  // Handle geolocation
  const handleLocate = useCallback(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setUserLocation([latitude, longitude]);
        },
        (error) => {
          console.error("Geolocation error:", error);
        },
      );
    }
  }, []);

  // Handle map click
  const handleMapClick = useCallback(
    (latlng: any) => {
      setClickedLocation(latlng);
      onMapClick && onMapClick(latlng);
    },
    [onMapClick],
  );

  return (
    <div className={`advanced-map relative rounded-xl overflow-hidden border border-border shadow-xl ${className}`} style={style}>
      <MapContainer
        key={`${center[0]}-${center[1]}`}
        center={center}
        zoom={zoom}
        style={{ height: "100%", width: "100%", background: "#0b1329" }}
        scrollWheelZoom={true}
      >
        <RecenterMap center={center} zoom={zoom} />

        {/* Base tile layers */}
        {currentLayers.openstreetmap && (
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
        )}

        {currentLayers.satellite && (
          <TileLayer
            attribution='&copy; Esri'
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          />
        )}

        {/* Map events */}
        <MapEvents
          onMapClick={handleMapClick}
          onLocationFound={setUserLocation}
        />

        {/* Custom controls */}
        {enableControls && (
          <CustomControls
            onLocate={handleLocate}
            onToggleLayer={handleToggleLayer}
            layers={currentLayers}
          />
        )}

        {/* Markers with clustering */}
        {enableClustering ? (
          <MarkerClusterGroup>
            {markers.map((marker, index) => (
              <Marker
                key={marker.id || index}
                position={marker.position}
                icon={
                  marker.icon || createCustomIcon(marker.color, marker.size)
                }
                eventHandlers={{
                  click: () => onMarkerClick && onMarkerClick(marker),
                }}
              >
                {marker.popup && (
                  <Popup>
                    <div style={{ padding: "4px" }}>
                      <h4 style={{ margin: "0 0 4px 0", fontWeight: "bold", fontSize: "14px" }}>{marker.popup.title}</h4>
                      <p style={{ margin: "0", fontSize: "12px", color: "#475569" }}>{marker.popup.content}</p>
                      {marker.popup.image && (
                        <img
                          src={marker.popup.image}
                          alt={marker.popup.title}
                          style={{ maxWidth: "100%", height: "auto", marginTop: "6px", borderRadius: "4px" }}
                        />
                      )}
                    </div>
                  </Popup>
                )}
              </Marker>
            ))}
          </MarkerClusterGroup>
        ) : (
          markers.map((marker, index) => (
            <Marker
              key={marker.id || index}
              position={marker.position}
              icon={marker.icon || createCustomIcon(marker.color, marker.size)}
              eventHandlers={{
                click: () => onMarkerClick && onMarkerClick(marker),
              }}
            >
              {marker.popup && (
                <Popup>
                  <div>
                    <h4>{marker.popup.title}</h4>
                    <p>{marker.popup.content}</p>
                  </div>
                </Popup>
              )}
            </Marker>
          ))
        )}

        {/* User location marker */}
        {userLocation && (
          <Marker
            position={userLocation}
            icon={createCustomIcon("red", "medium")}
          >
            <Popup>Your current location</Popup>
          </Marker>
        )}

        {/* Clicked location marker */}
        {clickedLocation && (
          <Marker
            position={[clickedLocation.lat, clickedLocation.lng]}
            icon={createCustomIcon("orange", "small")}
          >
            <Popup>
              Lat: {clickedLocation.lat.toFixed(4)}
              <br />
              Lng: {clickedLocation.lng.toFixed(4)}
            </Popup>
          </Marker>
        )}

        {/* Polygons */}
        {polygons.map((polygon, index) => (
          <Polygon
            key={polygon.id || index}
            positions={polygon.positions}
            pathOptions={
              polygon.style || { color: "#8b5cf6", weight: 2, fillOpacity: 0.3 }
            }
          >
            {polygon.popup && <Popup>{polygon.popup}</Popup>}
          </Polygon>
        ))}

        {/* Circles */}
        {circles.map((circle, index) => (
          <Circle
            key={circle.id || index}
            center={circle.center}
            radius={circle.radius}
            pathOptions={
              circle.style || { color: "#3b82f6", weight: 2, fillOpacity: 0.2 }
            }
          >
            {circle.popup && <Popup>{circle.popup}</Popup>}
          </Circle>
        ))}

        {/* Polylines */}
        {polylines.map((polyline, index) => (
          <Polyline
            key={polyline.id || index}
            positions={polyline.positions}
            pathOptions={polyline.style || { color: "#ef4444", weight: 3 }}
          >
            {polyline.popup && <Popup>{polyline.popup}</Popup>}
          </Polyline>
        ))}
      </MapContainer>
    </div>
  );
};

export default AdvancedMap;
