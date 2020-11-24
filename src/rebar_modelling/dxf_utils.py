"""Utils to work with DXF files."""
import sys
from typing import Any
from typing import Dict
from typing import Tuple

import ezdxf
from ezdxf.layouts.layout import Modelspace

from rebar_modelling.data.constants import Constants


class DXFModel:
    """Class that handles methods to work with DXF files."""

    def __init__(self, filename: str, axis: str) -> None:
        """Initialize DXF model."""
        self.open_dxf(filename)
        self.axis = axis
        self.msp = self.doc.modelspace()
        self.x_min = self.find_border_coordinate(axis="x", extrema="min")
        self.y_min = self.find_border_coordinate(axis="y", extrema="min")
        self.x_max = self.find_border_coordinate(axis="x", extrema="max")
        self.y_max = self.find_border_coordinate(axis="y", extrema="max")

    def open_dxf(self, filename: str) -> Modelspace:
        """Tries to open provided dxf file and returns modelspace."""
        try:
            self.doc = ezdxf.readfile(filename)
            print("DXF opened without any issues")
            return self.doc.modelspace()

        except IOError:
            print("Not a DXF file or a generic I/O error.")
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print("Invalid or corrupted DXF file.")
            sys.exit(2)

    def print_entity(self, e: Any) -> None:
        """Prints entity coordinates and layer."""
        print("LINE on layer: %s" % e.dxf.layer)
        print("first corner: %s" % e.dxf.vtx0)
        print("second corner: %s" % e.dxf.vtx1)
        print("third corner: %s" % e.dxf.vtx2)
        print("fourth corner: %s" % e.dxf.vtx3)

    def print_all_entities(self) -> None:
        """Prints data for all entities in modelspace."""
        for e in self.msp:
            self.print_entity(e)

    def find_border_coordinate(self, axis: str, extrema: str) -> float:
        """Find borders coordinates.

        Args:
            axis: input desired 'x' or 'y' axis.
            extrema: input desired 'max' or 'min' values.

        Returns:
             Float value

        Raises:
            ValueError: Unknown axis provided. You should provide axes 'x' or 'y'.
        """
        if axis == "x":
            axis_value = 0
        elif axis == "y":
            axis_value = 1
        else:
            raise ValueError(
                "Unknown axis provided. You should provide axes 'x' or 'y'."
            )

        value = 0

        for e in self.msp:

            i = 0

            if i == 0:
                value = e[0][axis_value]

            while i <= 3:
                candidate_value = e[i][axis_value]
                i += 1
                if extrema == "max":
                    if candidate_value > value:
                        value = candidate_value
                elif extrema == "min":
                    if candidate_value < value:
                        value = candidate_value

        return value

    def minimal_rebar_length(self) -> float:
        """Minimal rebar length with anker length equal 1."""
        if self.axis == "x":
            min_border_coordinate = self.x_min
            max_border_coordinate = self.x_max
        elif self.axis == "y":
            min_border_coordinate = self.y_min
            max_border_coordinate = self.y_max
        else:
            raise ValueError(
                "Unknown axis provided. You should provide axes 'x' or 'y'."
            )

        anchorage_length = 1000
        equivalent_anchorage_length = anchorage_length / 1000

        min_coordinate = min_border_coordinate - equivalent_anchorage_length
        max_coordinate = max_border_coordinate + equivalent_anchorage_length
        minimal_length = max_coordinate - min_coordinate
        return minimal_length

    def rebar_length(self, minimal_length: float) -> float:
        """Find appropriate rebar length."""
        for i in Constants.LENGTH_OF_REBARS:
            equivalent_length = i / 1000
            if equivalent_length > minimal_length:
                return equivalent_length
        raise Exception("Cannot iterate through possible rebars length list.")

    def minimal_zone_width(self) -> float:
        """Find minimal zone width with indent 50."""
        if self.axis == "x":
            min_border_coordinate = self.y_min
            max_border_coordinate = self.y_max
        elif self.axis == "y":
            min_border_coordinate = self.x_min
            max_border_coordinate = self.x_max
        else:
            raise ValueError(
                "Unknown axis provided. You should provide axes 'x' or 'y'."
            )

        indent = 50
        equivalent_indent = indent / 1000

        min_coordinate = min_border_coordinate - equivalent_indent
        max_coordinate = max_border_coordinate + equivalent_indent
        minimal_width = max_coordinate - min_coordinate

        return minimal_width

    def zone_width(self, minimal_width: float) -> float:
        """Find reinforcement zone width."""
        reinforcement_pitch = 200
        equivalent_reinforcement_pitch = reinforcement_pitch / 1000

        zone_width = (
            minimal_width
            + equivalent_reinforcement_pitch
            - minimal_width % equivalent_reinforcement_pitch
        )
        return zone_width

    def reinforcement_zone_coordinates(
        self, rebar_length: float, zone_width: float
    ) -> Dict[str, Tuple[float, float]]:
        """Find reinforcement zone coordinates."""
        if self.axis == "x":
            x_center = (self.x_max + self.x_min) / 2
            zone_x_min_coordinate = x_center - rebar_length / 2
            zone_x_max_coordinate = x_center + rebar_length / 2

            y_center = (self.y_max + self.y_min) / 2
            zone_y_min_coordinate = y_center - zone_width / 2
            zone_y_max_coordinate = y_center + zone_width / 2

        elif self.axis == "y":
            y_center = (self.y_max + self.y_min) / 2
            zone_y_min_coordinate = y_center - rebar_length / 2
            zone_y_max_coordinate = y_center + rebar_length / 2

            x_center = (self.x_max + self.x_min) / 2
            zone_x_min_coordinate = x_center - zone_width / 2
            zone_x_max_coordinate = x_center + zone_width / 2

        else:
            raise ValueError(
                "Unknown axis provided. You should provide axes 'x' or 'y'."
            )

        zone_coordinates = {
            "bl": (zone_x_min_coordinate, zone_y_min_coordinate),
            "br": (zone_x_max_coordinate, zone_y_min_coordinate),
            "tr": (zone_x_max_coordinate, zone_y_max_coordinate),
            "tl": (zone_x_min_coordinate, zone_y_max_coordinate),
        }

        return zone_coordinates
