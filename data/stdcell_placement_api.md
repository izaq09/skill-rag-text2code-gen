# Cadence SKILL APIs for Standard Cell Placement Optimization

This document serves as a comprehensive reference for Cadence SKILL Application Programming Interfaces (APIs) designed to facilitate and control the optimization of standard cell placement for VLSI designs. These APIs empower users to define specific objectives and constraints for the placement process, thereby achieving desired layout characteristics.

## 1. `genOpt` - Initiate Placement Optimization

**Purpose:**
This API initiates the core standard cell placement optimization routine. It allows the designer to specify whether the primary optimization goal should be minimizing wire length or achieving a compact layout area. This command must be run after all the constraints are set.

**Usage:**

```skill
genOpt( [g_priority] )
```

**Parameters:**

| Parameter | Type | Description |
| - | - | - |
| `g_priority` | `string` | **Optional.** Determines the optimizer's main focus. Valid options are: <br> - `"HPWL"`: Optimizes primarily for Half-Perimeter Wire Length. This typically improves timing performance by reducing signal delays. <br> - `"Area"`: Optimizes primarily for minimizing the total silicon area occupied by the placed cells, leading to a more compact design. <br> If this parameter is omitted, the optimizer will proceed with its default balanced strategy. |

**Return Value:**

* `t`: Indicates successful initiation of the optimization process.
* `nil`: Signifies an error or failure to start the optimization.

**Examples:**

```skill
; Start optimization with a strong emphasis on reducing wire length
genOpt("HPWL")

; Start optimization, prioritizing a smaller layout area
genOpt("Area")

; Start optimization using the tool's default balancing criteria
genOpt()
```

## 2. `genConstrainNet` - Prioritize Net

**Purpose:**
This API enables designers to assign priority to specific nets. Nets listed earlier in the input will receive higher consideration during optimization, potentially resulting in shorter connections or more favorable routing for those critical signals.

**Usage:**

```skill
genConstrainNet( g_netList )
```

**Parameters:**

| Parameter | Type | Description |
| - | - | - |
| `g_netList` | `list` | **Required.** A list of strings, where each string corresponds to the name of a net. The sequence of nets in this list dictates their optimization priority (the first net has the highest priority). Example: `list("clk_div_out" "reset_sync")`. |

**Return Value:**

* `t`: Indicates successful application of the net constraints.
* `nil`: Signifies an invalid input list or a failure to apply constraints.

**Examples:**

```skill
; Prioritize 'clock_data' first, followed by 'address_bus' for placement
genConstrainNet( '("clock_data" "address_bus") )

; Apply high priority only to the 'enable_signal' net
genConstrainNet( '("enable_signal") )
```

---

## 3. `genConstrainAspectRatio` - Control Placement Aspect Ratio

**Purpose:**
This API allows the user to impose constraints on the aspect ratio (width divided by height) of the standard cell placement area. This is vital for aligning the placement with specific chip core dimensions or for ensuring balanced routing density in both horizontal and vertical directions.

**Usage:**

```skill
genConstrainAspectRatio( g_minAspectRatio g_maxAspectRatio )
```

**Parameters:**

| Parameter | Type | Description |
| - | - | - |
| `g_minAspectRatio` | `number` | **Required.** The minimum allowed value for the placement aspect ratio (Width/Height). Must be a non-negative numerical value.                                                         |
| `g_maxAspectRatio` | `number` | **Required.** The maximum allowed value for the placement aspect ratio (Width/Height). Must be a non-negative numerical value and greater than or equal to `g_minAspectRatio`. |

**Return Value:**

* `t`: Indicates successful application of the aspect ratio constraint.
* `nil`: Signifies invalid input values (e.g., `g_minAspectRatio` exceeding `g_maxAspectRatio`, or negative values).

**Examples:**

```skill
; Restrict the aspect ratio to be between 0.9 and 1.1 (nearly square)
genConstrainAspectRatio( 0.9 1.1 )

; Force the placement to be as close to a 2:1 width-to-height ratio as possible
genConstrainAspectRatio( 2.0 2.0 )

; Allow a range for wider-than-tall layouts
genConstrainAspectRatio( 1.3 1.8 )
```

---

## 4. `genConstrainOrient` - Set Instance Orientation

**Purpose:**
This API provides the capability to fix the physical orientation of one or more specified standard cell instances. This is particularly useful for cells with unique routing requirements, power connections, or those critical for signal integrity.

**Usage:**

```skill
genConstrainOrient( g_instanceNameList g_orientation )
```

**Parameters:**

| Parameter | Type | Description |
| - | - | - |
| `g_instanceNameList` | `list` | **Required.** A list of strings, where each string represents the hierarchical instance name of a standard cell to be constrained.                                                                                                                                                                                |
| `g_orientation`      | `string` | **Required.** The desired final orientation for the specified instances. Common valid orientation codes include: <br> - `"R0"`: Default orientation (0 degrees rotation). <br> - `"R90"`: Rotated 90 degrees clockwise. <br> - `"R180"`: Rotated 180 degrees. <br> - `"R270"`: Rotated 270 degrees clockwise. <br> - `"MX"`: Mirrored horizontally (around the X-axis). <br> - `"MY"`: Mirrored vertically (around the Y-axis). <br> Note: Specific technology libraries may support additional orientation codes. |

**Return Value:**

* `t`: Indicates successful application of the orientation constraints.
* `nil`: Signifies an invalid input list, an unrecognized orientation, or if specified instances do not exist.

**Examples:**

```skill
; Set instance 'top/blockA/U_FIFO_CTRL' to its default R0 orientation
genConstrainOrient( '("top/blockA/U_FIFO_CTRL") "R0" )

; Mirror 'U_MEM_DRV1' and 'U_MEM_DRV2' horizontally
genConstrainOrient( '("U_MEM_DRV1" "U_MEM_DRV2") "MX" )

; Rotate an I/O buffer 'U_PAD_BUFFER' by 90 degrees clockwise
genConstrainOrient( '("U_PAD_BUFFER") "R90" )
```

---

## 5. `genConstrainBlockage` - Create Placement Blockage

**Purpose:**
This API defines a rectangular area within the design where standard cells are explicitly forbidden from being placed. This is crucial for reserving space for various purposes such as manual routing channels, sensitive analog circuitry, pre-placed hard IP macros, or other regions unsuitable for automated cell placement.

**Usage:**

```skill
genConstrainBlockage( g_boundingBox )
```

**Parameters:**

| Parameter | Type | Description |
| - | - | - |
| `g_boundingBox`  | `list` | **Required.** A list representing the coordinates of the blockage area. The expected format is `list(ll_x:ll_y ur_x:ur_y)`, where `ll_x:ll_y` specify the lower-left X and Y coordinates, and `ur_x:ur_y` specify the upper-right X and Y coordinates of the rectangle. Coordinates are typically expressed in the design's database units (e.g., microns or nanometers). Example: `list(10.0:12.5 25.0:30.0)`. |

**Return Value:**

* `t`: Indicates successful creation of the placement blockage.
* `nil`: Signifies an invalid bounding box format or coordinates that are outside the valid design boundaries.

**Examples:**

```skill
; Create a blockage in the area from (5.0, 6.0) to (15.0, 18.0)
genConstrainBlockage( list(5.0:6.0 15.0:18.0) )

; Define a blockage for a large, pre-placed memory block
genConstrainBlockage( list(50.0:75.0 100.0:120.0) )
```

## Example procedure

```skill

procedure(gen_test_cell_a()
    prog(()
        ; Command to constraint net in the sequence of clk_sync, a, b, out
        genConstrainNet(list("clk_sync" "a" "b" "out"))

        ; Command to constraint placement aspect ratio to be between 1.4 and 1.6 (Width longer than height)
        genConstrainAspectRatio(1.4 1.6)

        ; Command to constraint the instances I1 and I2 to be MX
        genConstrainOrient(list("I1" "I2") "MX")


        ; Command to create a blockage at list(1:1 2:2)
        genConstrainBlockage(list(1.0:1.0 2.0:2.0))

        ; Command to run optimizer with balanced setting
        genOpt()
    );prog
);procedure

```