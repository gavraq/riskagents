# Complete BPMN Diagram Interchange (DI) Generation Guide

## Critical Requirement

**BPMN files MUST include complete BPMNDiagram sections** with positioning for every element to render in tools like demo.bpmn.io, Camunda Modeler, and Signavio.

## Why BPMN DI is Required

BPMN 2.0 XML defines the **process logic** (tasks, gateways, flows), but **BPMN DI defines the visual layout** (where each element appears on the canvas).

**Without DI:** File loads but shows only empty swim lanes or doesn't render at all.
**With complete DI:** File renders immediately with all tasks, gates, and flows visible.

---

## Complete BPMN File Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
                   id="sample-diagram"
                   targetNamespace="http://bpmn.io/schema/bpmn">

  <!-- SECTION 1: Process Definition (Logic) -->
  <bpmn2:process id="Process_1" isExecutable="false">
    <!-- Tasks, gateways, events, flows -->
  </bpmn2:process>

  <!-- SECTION 2: BPMN DI (Visual Layout) -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">
      <!-- Shapes for tasks, gateways, events -->
      <!-- Edges for sequence flows -->
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</bpmn2:definitions>
```

---

## Element Positioning Reference

### Standard Dimensions

| Element Type | Width | Height | Shape |
|--------------|-------|--------|-------|
| **Task** | 100px | 80px | Rectangle |
| **User Task** | 100px | 80px | Rectangle with user icon |
| **Service Task** | 100px | 80px | Rectangle with gear icon |
| **Send Task** | 100px | 80px | Rectangle with envelope icon |
| **Receive Task** | 100px | 80px | Rectangle with envelope icon |
| **Exclusive Gateway** | 50px | 50px | Diamond |
| **Parallel Gateway** | 50px | 50px | Diamond with + |
| **Inclusive Gateway** | 50px | 50px | Diamond with O |
| **Start Event** | 36px | 36px | Circle |
| **End Event** | 36px | 36px | Circle (thick border) |
| **Intermediate Event** | 36px | 36px | Circle (double border) |
| **Swim Lane (Participant)** | 1200-1600px | 200-350px | Horizontal rectangle |

### Standard Spacing

| Spacing Type | Distance |
|--------------|----------|
| **Between tasks** (horizontal) | 50px minimum |
| **Between tasks** (vertical) | 30px minimum |
| **Task to gateway** | 50px |
| **Gateway to task** | 50px |
| **Swim lane vertical spacing** | 20px between lanes |
| **Left margin** (first element) | 180px from swim lane start |
| **Top margin** (within lane) | 60px from swim lane top |

---

## Positioning Algorithm

### Single Process (No Swim Lanes)

```python
def layout_simple_process(elements):
    x = 150  # Starting X
    y = 100  # Starting Y
    spacing = 50

    positions = {}

    for elem in elements:
        if elem.type == 'startEvent':
            positions[elem.id] = {'x': x, 'y': y, 'width': 36, 'height': 36}
            x += 36 + spacing

        elif elem.type in ['task', 'userTask', 'serviceTask']:
            positions[elem.id] = {'x': x, 'y': y - 20, 'width': 100, 'height': 80}
            x += 100 + spacing

        elif elem.type in ['exclusiveGateway', 'parallelGateway']:
            positions[elem.id] = {'x': x, 'y': y - 7, 'width': 50, 'height': 50}
            x += 50 + spacing

        elif elem.type == 'endEvent':
            positions[elem.id] = {'x': x, 'y': y, 'width': 36, 'height': 36}

    return positions
```

### With Swim Lanes (Collaboration)

```python
def layout_with_swimlanes(collaboration):
    lane_height = 250
    lane_y = 80
    lane_width = 1400

    swim_lanes = []

    for idx, participant in enumerate(collaboration.participants):
        y_pos = lane_y + (idx * (lane_height + 20))

        swim_lanes.append({
            'id': participant.id,
            'x': 150,
            'y': y_pos,
            'width': lane_width,
            'height': lane_height
        })

        # Position elements within this lane
        x = 180  # Start 30px inside lane
        y_center = y_pos + (lane_height / 2)

        for elem in participant.elements:
            if elem.type == 'startEvent':
                positions[elem.id] = {
                    'x': x,
                    'y': y_center - 18,  # Center vertically
                    'width': 36,
                    'height': 36
                }
                x += 86  # 36 + 50 spacing

            elif elem.type in ['task', 'userTask']:
                positions[elem.id] = {
                    'x': x,
                    'y': y_center - 40,  # Center vertically
                    'width': 100,
                    'height': 80
                }
                x += 150  # 100 + 50 spacing

            # ... continue for other element types

    return swim_lanes, positions
```

### Parallel Gateway Branching

When a parallel gateway splits into multiple paths:

```python
def layout_parallel_branches(gateway_pos, num_branches):
    """
    Layout tasks after a parallel gateway.
    Branches go vertically, then converge.
    """
    branch_spacing = 120  # Vertical spacing between branches

    # Starting positions for each branch
    base_y = gateway_pos['y'] - ((num_branches - 1) * branch_spacing / 2)

    branch_positions = []
    for i in range(num_branches):
        y = base_y + (i * branch_spacing)
        x = gateway_pos['x'] + 100  # Move right from gateway

        branch_positions.append({
            'x': x,
            'y': y,
            'width': 100,
            'height': 80
        })

    return branch_positions
```

---

## Complete DI Template Examples

### Example 1: Simple Linear Process

```xml
<bpmn2:process id="Process_1" isExecutable="false">
  <bpmn2:startEvent id="StartEvent_1" name="Start">
    <bpmn2:outgoing>Flow_1</bpmn2:outgoing>
  </bpmn2:startEvent>

  <bpmn2:task id="Task_1" name="Review Document">
    <bpmn2:incoming>Flow_1</bpmn2:incoming>
    <bpmn2:outgoing>Flow_2</bpmn2:outgoing>
  </bpmn2:task>

  <bpmn2:exclusiveGateway id="Gateway_1" name="Approved?">
    <bpmn2:incoming>Flow_2</bpmn2:incoming>
    <bpmn2:outgoing>Flow_3_Yes</bpmn2:outgoing>
    <bpmn2:outgoing>Flow_3_No</bpmn2:outgoing>
  </bpmn2:exclusiveGateway>

  <bpmn2:task id="Task_2" name="Process Approval">
    <bpmn2:incoming>Flow_3_Yes</bpmn2:incoming>
    <bpmn2:outgoing>Flow_4</bpmn2:outgoing>
  </bpmn2:task>

  <bpmn2:task id="Task_3" name="Revise Document">
    <bpmn2:incoming>Flow_3_No</bpmn2:incoming>
    <bpmn2:outgoing>Flow_5</bpmn2:outgoing>
  </bpmn2:task>

  <bpmn2:exclusiveGateway id="Gateway_2">
    <bpmn2:incoming>Flow_4</bpmn2:incoming>
    <bpmn2:incoming>Flow_5</bpmn2:incoming>
    <bpmn2:outgoing>Flow_6</bpmn2:outgoing>
  </bpmn2:exclusiveGateway>

  <bpmn2:endEvent id="EndEvent_1" name="Complete">
    <bpmn2:incoming>Flow_6</bpmn2:incoming>
  </bpmn2:endEvent>

  <!-- Sequence Flows -->
  <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
  <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="Gateway_1"/>
  <bpmn2:sequenceFlow id="Flow_3_Yes" name="Yes" sourceRef="Gateway_1" targetRef="Task_2"/>
  <bpmn2:sequenceFlow id="Flow_3_No" name="No" sourceRef="Gateway_1" targetRef="Task_3"/>
  <bpmn2:sequenceFlow id="Flow_4" sourceRef="Task_2" targetRef="Gateway_2"/>
  <bpmn2:sequenceFlow id="Flow_5" sourceRef="Task_3" targetRef="Gateway_2"/>
  <bpmn2:sequenceFlow id="Flow_6" sourceRef="Gateway_2" targetRef="EndEvent_1"/>
</bpmn2:process>

<!-- BPMN DI (Visual Layout) -->
<bpmndi:BPMNDiagram id="BPMNDiagram_1">
  <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">

    <!-- Start Event -->
    <bpmndi:BPMNShape id="StartEvent_1_di" bpmnElement="StartEvent_1">
      <dc:Bounds x="152" y="102" width="36" height="36"/>
      <bpmndi:BPMNLabel>
        <dc:Bounds x="158" y="145" width="25" height="14"/>
      </bpmndi:BPMNLabel>
    </bpmndi:BPMNShape>

    <!-- Task 1 -->
    <bpmndi:BPMNShape id="Task_1_di" bpmnElement="Task_1">
      <dc:Bounds x="240" y="80" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <!-- Gateway 1 (Decision) -->
    <bpmndi:BPMNShape id="Gateway_1_di" bpmnElement="Gateway_1" isMarkerVisible="true">
      <dc:Bounds x="395" y="95" width="50" height="50"/>
      <bpmndi:BPMNLabel>
        <dc:Bounds x="390" y="65" width="60" height="14"/>
      </bpmndi:BPMNLabel>
    </bpmndi:BPMNShape>

    <!-- Task 2 (Yes path) -->
    <bpmndi:BPMNShape id="Task_2_di" bpmnElement="Task_2">
      <dc:Bounds x="500" y="80" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <!-- Task 3 (No path) -->
    <bpmndi:BPMNShape id="Task_3_di" bpmnElement="Task_3">
      <dc:Bounds x="500" y="200" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <!-- Gateway 2 (Merge) -->
    <bpmndi:BPMNShape id="Gateway_2_di" bpmnElement="Gateway_2" isMarkerVisible="true">
      <dc:Bounds x="655" y="95" width="50" height="50"/>
    </bpmndi:BPMNShape>

    <!-- End Event -->
    <bpmndi:BPMNShape id="EndEvent_1_di" bpmnElement="EndEvent_1">
      <dc:Bounds x="762" y="102" width="36" height="36"/>
      <bpmndi:BPMNLabel>
        <dc:Bounds x="754" y="145" width="52" height="14"/>
      </bpmndi:BPMNLabel>
    </bpmndi:BPMNShape>

    <!-- Edges (Connections) -->
    <bpmndi:BPMNEdge id="Flow_1_di" bpmnElement="Flow_1">
      <di:waypoint x="188" y="120"/>
      <di:waypoint x="240" y="120"/>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_2_di" bpmnElement="Flow_2">
      <di:waypoint x="340" y="120"/>
      <di:waypoint x="395" y="120"/>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_3_Yes_di" bpmnElement="Flow_3_Yes">
      <di:waypoint x="445" y="120"/>
      <di:waypoint x="500" y="120"/>
      <bpmndi:BPMNLabel>
        <dc:Bounds x="464" y="102" width="18" height="14"/>
      </bpmndi:BPMNLabel>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_3_No_di" bpmnElement="Flow_3_No">
      <di:waypoint x="420" y="145"/>
      <di:waypoint x="420" y="240"/>
      <di:waypoint x="500" y="240"/>
      <bpmndi:BPMNLabel>
        <dc:Bounds x="428" y="190" width="15" height="14"/>
      </bpmndi:BPMNLabel>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_4_di" bpmnElement="Flow_4">
      <di:waypoint x="600" y="120"/>
      <di:waypoint x="655" y="120"/>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_5_di" bpmnElement="Flow_5">
      <di:waypoint x="600" y="240"/>
      <di:waypoint x="680" y="240"/>
      <di:waypoint x="680" y="145"/>
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_6_di" bpmnElement="Flow_6">
      <di:waypoint x="705" y="120"/>
      <di:waypoint x="762" y="120"/>
    </bpmndi:BPMNEdge>

  </bpmndi:BPMNPlane>
</bpmndi:BPMNDiagram>
```

### Key DI Patterns:

#### Pattern 1: Horizontal Sequence
```
Task1 (x=240) --50px--> Task2 (x=390)
```
Waypoints: [340, y], [390, y]

#### Pattern 2: Gateway Split (Vertical)
```
Gateway (x=420, y=120)
  |-- Yes --> Task (x=500, y=120)
  |-- No  --> Task (x=500, y=240)
```
Waypoints for No path: [420, 145], [420, 240], [500, 240]

#### Pattern 3: Gateway Merge (Vertical to Horizontal)
```
Task (x=600, y=240)
  |
  v
Gateway (x=680, y=120)
```
Waypoints: [600, 240], [680, 240], [680, 145]

---

## Example 2: Swim Lane Process with Message Flows

```xml
<bpmn:collaboration id="Collaboration_1">
  <bpmn:participant id="Participant_Credit" name="Credit Team" processRef="Process_Credit"/>
  <bpmn:participant id="Participant_Legal" name="Legal Team" processRef="Process_Legal"/>

  <!-- Message Flow -->
  <bpmn:messageFlow id="Flow_RequestReview" sourceRef="Task_Credit_Request" targetRef="Task_Legal_Review"/>
  <bpmn:messageFlow id="Flow_ReturnReview" sourceRef="Task_Legal_Review" targetRef="Task_Credit_Receive"/>
</bpmn:collaboration>

<!-- Credit Process -->
<bpmn:process id="Process_Credit" isExecutable="false">
  <bpmn:startEvent id="Start_Credit"/>
  <bpmn:task id="Task_Credit_Request" name="Request Legal Review"/>
  <bpmn:task id="Task_Credit_Receive" name="Receive Legal Opinion"/>
  <bpmn:endEvent id="End_Credit"/>
  <!-- Flows omitted for brevity -->
</bpmn:process>

<!-- Legal Process -->
<bpmn:process id="Process_Legal" isExecutable="false">
  <bpmn:task id="Task_Legal_Review" name="Review Documentation"/>
  <!-- Flows omitted for brevity -->
</bpmn:process>

<!-- BPMN DI -->
<bpmndi:BPMNDiagram id="BPMNDiagram_1">
  <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_1">

    <!-- Swim Lane: Credit Team -->
    <bpmndi:BPMNShape id="Participant_Credit_di" bpmnElement="Participant_Credit" isHorizontal="true">
      <dc:Bounds x="150" y="80" width="1000" height="250"/>
    </bpmndi:BPMNShape>

    <!-- Elements in Credit Lane -->
    <bpmndi:BPMNShape id="Start_Credit_di" bpmnElement="Start_Credit">
      <dc:Bounds x="202" y="187" width="36" height="36"/>
    </bpmndi:BPMNShape>

    <bpmndi:BPMNShape id="Task_Credit_Request_di" bpmnElement="Task_Credit_Request">
      <dc:Bounds x="290" y="165" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <bpmndi:BPMNShape id="Task_Credit_Receive_di" bpmnElement="Task_Credit_Receive">
      <dc:Bounds x="440" y="165" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <bpmndi:BPMNShape id="End_Credit_di" bpmnElement="End_Credit">
      <dc:Bounds x="592" y="187" width="36" height="36"/>
    </bpmndi:BPMNShape>

    <!-- Swim Lane: Legal Team -->
    <bpmndi:BPMNShape id="Participant_Legal_di" bpmnElement="Participant_Legal" isHorizontal="true">
      <dc:Bounds x="150" y="350" width="1000" height="200"/>
    </bpmndi:BPMNShape>

    <!-- Elements in Legal Lane -->
    <bpmndi:BPMNShape id="Task_Legal_Review_di" bpmnElement="Task_Legal_Review">
      <dc:Bounds x="290" y="410" width="100" height="80"/>
    </bpmndi:BPMNShape>

    <!-- Message Flows (dashed lines between lanes) -->
    <bpmndi:BPMNEdge id="Flow_RequestReview_di" bpmnElement="Flow_RequestReview">
      <di:waypoint x="340" y="245"/>  <!-- Bottom of Credit Task -->
      <di:waypoint x="340" y="410"/>  <!-- Top of Legal Task -->
    </bpmndi:BPMNEdge>

    <bpmndi:BPMNEdge id="Flow_ReturnReview_di" bpmnElement="Flow_ReturnReview">
      <di:waypoint x="390" y="410"/>  <!-- Top of Legal Task -->
      <di:waypoint x="390" y="300"/>  <!-- Mid point -->
      <di:waypoint x="490" y="300"/>  <!-- Mid point -->
      <di:waypoint x="490" y="245"/>  <!-- Bottom of Credit Task -->
    </bpmndi:BPMNEdge>

  </bpmndi:BPMNPlane>
</bpmndi:BPMNDiagram>
```

---

## Automation Guidelines for process-documenter Skill

### Step 1: Analyze Process Structure

```python
def analyze_process(elements):
    return {
        'num_lanes': count_swim_lanes(elements),
        'max_depth': calculate_max_parallel_depth(elements),
        'has_loops': detect_loops(elements),
        'num_elements': len(elements)
    }
```

### Step 2: Calculate Canvas Dimensions

```python
def calculate_canvas_size(analysis):
    if analysis['num_lanes'] > 1:
        width = max(1400, analysis['num_elements'] * 150)
        height = analysis['num_lanes'] * 270  # 250 lane + 20 gap
    else:
        width = analysis['num_elements'] * 150 + 300
        height = max(400, analysis['max_depth'] * 150)

    return width, height
```

### Step 3: Generate Positions for All Elements

```python
def generate_all_positions(process):
    positions = {}

    if process.has_swimlanes:
        positions = layout_swimlane_process(process)
    else:
        positions = layout_simple_process(process)

    return positions
```

### Step 4: Write Complete BPMN DI Section

For EVERY element in the process, generate:

1. **BPMNShape** for tasks, gateways, events
2. **BPMNEdge** for sequence flows and message flows

**DO NOT:**
- Skip elements
- Only add participant shapes without content
- Assume tools will auto-layout

---

## Validation Checklist

Before finalizing BPMN file, verify:

- [ ] Every `<bpmn:task>` has a corresponding `<bpmndi:BPMNShape>`
- [ ] Every `<bpmn:gateway>` has a corresponding `<bpmndi:BPMNShape>`
- [ ] Every `<bpmn:startEvent>` and `<bpmn:endEvent>` have shapes
- [ ] Every `<bpmn:sequenceFlow>` has a corresponding `<bpmndi:BPMNEdge>`
- [ ] Every `<bpmn:messageFlow>` has a corresponding `<bpmndi:BPMNEdge>`
- [ ] All swim lanes (`<bpmn:participant>`) have shapes with isHorizontal="true"
- [ ] Waypoints connect correctly (edge endpoints match shape positions)
- [ ] No overlapping elements
- [ ] Canvas is large enough for all elements

---

## Testing

### Test Files

1. Load in **demo.bpmn.io** (online, free)
2. Load in **Camunda Modeler** (desktop app)
3. Load in **bpmn.io library** (if integrating programmatically)

### Expected Result

- All swim lanes visible with labels
- All tasks, gateways, events visible in correct lanes
- All flows visible connecting elements
- No "diagram may not render correctly" warnings
- No "unresolved reference" errors

---

## Common Errors and Fixes

### Error: "Diagram may not render correctly"
**Cause:** Missing DI elements
**Fix:** Add `<bpmndi:BPMNShape>` for every task/gateway/event

### Error: "Unresolved reference <ElementID>"
**Cause:** Element referenced but not defined
**Fix:** Ensure all `sourceRef`/`targetRef` match defined element IDs

### Error: Empty swim lanes
**Cause:** Participant shapes defined but no element shapes inside
**Fix:** Add BPMNShape for every element within that participant's process

### Error: Elements overlap
**Cause:** Incorrect x/y positioning
**Fix:** Recalculate positions with proper spacing (50px min horizontal, 30px min vertical)

---

## Quick Reference: Element Positioning

### Start Event
```xml
<bpmndi:BPMNShape id="Start_di" bpmnElement="Start">
  <dc:Bounds x="152" y="102" width="36" height="36"/>
</bpmndi:BPMNShape>
```
Center point: (170, 120)

### Task
```xml
<bpmndi:BPMNShape id="Task_di" bpmnElement="Task">
  <dc:Bounds x="240" y="80" width="100" height="80"/>
</bpmndi:BPMNShape>
```
Center point: (290, 120)

### Exclusive Gateway
```xml
<bpmndi:BPMNShape id="Gateway_di" bpmnElement="Gateway" isMarkerVisible="true">
  <dc:Bounds x="395" y="95" width="50" height="50"/>
</bpmndi:BPMNShape>
```
Center point: (420, 120)

### Sequence Flow (Straight)
```xml
<bpmndi:BPMNEdge id="Flow_di" bpmnElement="Flow">
  <di:waypoint x="340" y="120"/>  <!-- From Task end -->
  <di:waypoint x="395" y="120"/>  <!-- To Gateway start -->
</bpmndi:BPMNEdge>
```

### Sequence Flow (Vertical turn)
```xml
<bpmndi:BPMNEdge id="Flow_di" bpmnElement="Flow">
  <di:waypoint x="420" y="145"/>  <!-- From Gateway bottom -->
  <di:waypoint x="420" y="240"/>  <!-- Down vertically -->
  <di:waypoint x="500" y="240"/>  <!-- Then horizontal to Task -->
</bpmndi:BPMNEdge>
```

---

## Summary for Skill Implementation

When process-documenter skill generates BPMN:

1. **Parse process** → identify all elements, lanes, flows
2. **Calculate layout** → position every element using spacing rules
3. **Generate process XML** → tasks, gateways, events, flows
4. **Generate complete DI** → shapes for every element, edges for every flow
5. **Validate** → every element has DI, no missing references
6. **Test** → file loads cleanly in demo.bpmn.io

**Key principle:** BPMN DI is NOT optional. Every BPMN file must have complete positioning data.
