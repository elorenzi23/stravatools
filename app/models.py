from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# todo: refactor this file into a directory

# app/models/activity_streams.py


class ActivityStreams:
    def __init__(self, activity_id, latlngs, times, name):
        self.activity_id = activity_id
        self.latlngs = latlngs
        self.times = times
        self.name = name

    def generate_gpx(self):
        from datetime import datetime, timedelta

        from lxml import etree

        nsmap = None
        gpx = etree.Element("gpx", version="1.1", creator="MyApp", nsmap=nsmap)

        metadata = etree.SubElement(gpx, "metadata")
        name = etree.SubElement(metadata, "name")
        name.text = self.name

        trk = etree.SubElement(gpx, "trk")
        trk_name = etree.SubElement(trk, "name")
        trk_name.text = self.name
        trkseg = etree.SubElement(trk, "trkseg")

        start_time = datetime.utcnow()  # or use activity start time from API
        for (lat, lon), sec in zip(self.latlngs, self.times):
            trkpt = etree.SubElement(
                trkseg, "trkpt", lat=str(lat), lon=str(lon)
            )
            time_elem = etree.SubElement(trkpt, "time")
            point_time = start_time + timedelta(seconds=sec)
            time_elem.text = point_time.isoformat() + "Z"

        return etree.tostring(
            gpx, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )
