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

### Category:
- `name`
- `description`
- `requires_training`
#### Examples:
Camera; DLSR Bodies/Video Cameras; requires_training=True

Audio; Microphones/Recorders; requires_training=False

### Equipment:
- `asset_tag`
- `name`
- `status`
- `category_id`
- `notes`
#### Examples:
R7-001; Canon EOS R7; Available; Camera; Body Only

VMG-002; Rode Video Mic GO; Audio; Includes shock mount
### Checkout:
- `event_id`
- `crew_member_id`
- `equipment_id`
- `checkout_time`
- `checkin_time`
- `condition_notes`
#### Examples:
> (this does not show using IDs for related entities, but should still make sense) 

SirenCon 2025; John Appleseed; R7-001; 2025-05-29 18:00; null; Clean, good condition

University of Montana Speech; Cameron Seaman; VMG-002; 2025-12-01 08:00; 2025-12-01 13:00; Foam needs replacing

## Questions/use-cases
I think this database could be used to answer these questions:

Who is all helping with a certain event, and when does said event end?

Which checkouts are currently active, and what events do they correspond to?

What categories of equipment were utilized the most (total checkout hours)?
