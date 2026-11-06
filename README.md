# NushHACK-26
This is the repository for our NushHACK 2026 submission.
# Dependencies
- Flask
- Supabase
# Plan (For Now)
1. Check whether the application is online.
2. If online:
   - Sync changes from the JSON file to the database.
   - Update both the JSON file and database together.
3. If offline:
   - Temporarily store changes in the JSON file.

# Functionality for Officer (Might impliment)

1. Patrols
Guard tour: follow a set patrol route with checkpoints in order
Checkpoint scanning: scan a QR code or NFC tag at each point to prove presence, with time and GPS saved on the phone
Missed or late checkpoint alerts: the app counts down to the next checkpoint and warns the officer locally if it’s overdue
Ad-hoc observations at any checkpoint: “door ajar”, “light faulty”
Offline notes: the route, checkpoints and schedule are downloaded at the start of the shift
2. Inspections and checklists
Fire safety walks: exits, extinguishers, emergency lighting, fire doors
Equipment checks: CCTV, alarms, barrier gates, panic buttons
Opening and closing routines: lock-up and unlock checklists for buildings
PASS / FAIL / N/A per step, with a required photo and note on FAIL
A FAIL automatically creates a follow-up (maintenance ticket or incident)
3. Incident reporting
Quick report: pick a type (trespass, theft, injury, fire, suspicious person or package, vandalism, medical), severity, location, photos, voice note and short description
Templates by incident type, with required fields (e.g. injury needs the person’s details, first aid given, ambulance called)
Witness and involved-person details, with an ID scan
Live timeline: add updates to the same incident as it develops
Offline notes: fully usable offline, and photos and voice notes upload when the connection returns
4. Emergencies
SOS / panic button: sends an alert as soon as possible. If there’s no data, fall back to an SMS or a phone call, which often still works without internet. Make this clear on screen.
Lone-worker check: “are you OK?” prompts at intervals. A missed reply raises an alert.
Emergency procedures stored offline: evacuation, bomb threat, fire, medical, with step-by-step checklists
Emergency contacts stored offline, with one-tap dialling
Muster / headcount during evacuations
5. Access control and visitors
Visitor registration: name, ID, host, purpose, vehicle, time in and out
Pre-registered visitor list downloaded for offline check-in
Watchlist / banned persons stored offline, so a match flags at the gate
Contractor permits: check that a work permit is valid before letting a contractor in
Vehicle log: licence plate, time in and out, parking bay
6. Keys and assets
Key log: who took which key, and when it was returned
Equipment checkout: radios, torches, body cams
Lost and found log with photos
7. Shift handover
Daily occurrence book (DOB): a running log of everything during the shift, which security companies in Singapore commonly keep
Handover summary: open incidents, unfinished checks, keys out, notes for the next officer
Clock in / out with location
Post orders: site-specific instructions stored offline
8. Officer support
Sync status everywhere: “saved on device”, “pending upload”, “synced”
My tasks today: assigned patrols and checklists with due times
Supervisor messages/broadcasts, shown once synced
Offline maps / floor plans with checkpoints marked
For your 24-hour build, pick a story with 3 or 4 features
Priority	Feature	Why
Core	Checklists / inspections	The challenge brief literally asks for “security processes”
Core	Incident report with photo	Shows offline media queuing, and is very relatable
Core	Patrol with QR checkpoint scan	Visual, shows proof of presence, and phones can scan QR codes with the camera
Wow	SOS that falls back to SMS when there’s no data	Shows you thought about real offline emergencies
Nice	Shift handover summary	Brings everything together into one closing screen for the demo
Skip	Visitors, keys, lone-worker checks, maps	Mention them on a “roadmap” slide

Demo story: an officer starts a night patrol offline, scans 3 checkpoints, fails a fire-exit check, which creates an incident with a photo, then reconnects. Everything syncs, and the supervisor sees the incident and the full patrol trail.
