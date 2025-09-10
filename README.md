# Database Idea: Event Media Gear Tracker

## Entities:
### Event:
- `name`
- `start_date`
- `end_date`
- `location`
#### Examples:
University of Montana Speech; 2025-12-01; 2025-12-02; Missoula, MT

SirenCon 2025; 2025-05-30; 2025-06-01; Rhinelander, WI 

### CrewMember:
- `first_name`
- `last_name`
- `email`
- `role`
- `is_trained`
#### Examples:
Cameron; Seaman; cameron@example.com; Director; is_trained=True

John; Appleseed; john@example.com; Audio; is_trained=False

### Equipment:
- `asset_tag`
- `name`
- `status`
- `notes`
- `equipment_type`
#### Examples:
R7-001; Canon EOS R7; Available; Camera; Body Only

VMG-002; Rode Video Mic GO; Checked_Out; Audio; Includes shock mount

### Equipment Type:
- `name`
- `requires_training`
- `description`
#### Examples:
Camera; DLSR Bodies/Video Cameras; requires_training=True

Audio; Microphones/Recorders; requires_training=False

#### Video:
> Subset of equipment
- `asset_tag`
- `model_number`
- `resolution`
- `frame_rate`
- `media_type`
#### Example:
R7-001; R7; 3840x2160; 60; SD

#### Audio:
> Subset of equipment
- `asset_tag`
- `model_number`
- `mic_type`
- `interface`
- `phantom_power`
#### Examples:
VMG-0012; VMG; Wireless Lavalier; 3.5mm TRS; False

### Checkout:
- `event_id`
- `crew_member_id`
- `equipment_id`
- `checkout_time`
- `checkin_time`
- `condition_notes_out`
- `condition_notes_in`
#### Examples:
> (this does not show using IDs for related entities, but should still make sense)

SirenCon 2025; John Appleseed; R7-001; 2025-05-29 18:00; null; Clean; good condition

University of Montana Speech; Cameron Seaman; VMG-002; 2025-12-01 08:00; 2025-12-01 13:00; Good condition; Foam needs replacing

## Questions/use-cases
I think this database could be used to answer these questions:

Who is all helping with a certain event, and when does said event end?

Which checkouts are currently active, and what events do they correspond to?

What categories of equipment were utilized the most (total checkout hours)?
