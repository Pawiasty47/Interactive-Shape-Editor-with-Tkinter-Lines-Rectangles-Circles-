Interactive Shape Editor (Tkinter)

This project is a Python application that allows users to draw, edit, and manipulate geometric shapes (lines, rectangles, and circles) on a Tkinter canvas.
It includes an intuitive interface with mouse interactions, draggable control handles, and the ability to save/load drawings using JSON.

🚀 Features
✔ Drawing

Draw lines, rectangles, and circles

Create shapes by clicking on the canvas (point-to-point)

Alternatively, enter numeric shape parameters:

Line / Rectangle: x1, y1, x2, y2

Circle: cx, cy, r

✔ Editing

Switch to Edit Mode to modify existing shapes

Select shapes by clicking them

Drag control handles to reshape objects:

Line: move endpoints

Rectangle: move corners

Circle: move center and radius point

Move entire shapes by dragging them

✔ File Operations

Save drawings to a JSON file

Load drawings from a JSON file

Automatically reconstructs shapes from saved coordinates

✔ UI & Controls

Escape key → Clear selection

Simple Tkinter-based interface

Cleanly separated drawing/editing modes

🖼 Preview

The interface consists of:

A left panel with controls:

Drawing/editing mode selection

Parameter input

Buttons for saving, loading, applying parameters

A large canvas on the right where shapes are drawn
