# A-029 sources (checked 25 Nov 2026)
- Classic controller rumble = small motors spinning an off-centre (eccentric) weight; the uneven spin shakes the controller:
  - TechRadar, "Meet the minds behind Nintendo Switch's HD Rumble tech": console gamepads "have instead used spinning 'eccentric rotating mass'
    (ERM) motors. An uneven weight spins around, and its centrifugal force creates the sensation of rumble" — https://www.techradar.com/news/meet-the-minds-behind-nintendo-switchs-hd-rumble-tech
  - Precision Microdrives (vibration-motor maker), ERM / game controller teardown article — https://www.precisionmicrodrives.com/?p=9168
  - Cheat Code Central, "How the DualSense's haptic motors actually work": earlier controllers used "rotary motors, the classic setup with an
    off-center weight spinning on a tiny shaft" — https://www.cheatcc.com/articles/how-the-dualsense-s-haptic-motors-actually-work/
- One motor in each handle; left = low-frequency (heavy) rumble, right = high-frequency (light) buzz (worded "on many controllers"):
  - Microsoft Learn, XINPUT_VIBRATION: "The left motor is the low-frequency rumble motor. The right motor is the high-frequency rumble motor."
    — https://learn.microsoft.com/en-us/gaming/gdk/docs/reference/input/xinputongameinput/structs/xinput_vibration
  - Precision Microdrives (above): the two motors have different masses, giving different amplitudes at different frequencies.
  - Unity Input System docs, IDualMotorRumble (low-frequency + high-frequency motor speeds) — https://docs.unity3d.com/Packages/com.unity.inputsystem@1.9/api/UnityEngine.InputSystem.Haptics.IDualMotorRumble.html
- "Dozens of times a second": rumble motors vibrate at roughly 15–45 Hz (US patent 11707765 "Game controller with vibration actuators":
  "vibrations ranging from around 15 Hz to 45 Hz" — https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11707765); the game sets the
  motor speed (PWM 0–255 per motor, same patent family; Microsoft XInput speeds 0–65535). Animation shows ~25–30 spins in one second.
- Newer controllers add coil/magnet (linear / voice-coil) actuators for finer taps:
  - TechRadar (above): HD Rumble uses "linear resonant actuators" instead of spinning motors.
  - Cheat Code Central (above): the newer controller "uses linear actuators instead of spinning off-center weights".
- Trend context (not stated in the video): GTA 6 release 19 Nov 2026 (Rockstar Newswire); The Game Awards 10 Dec 2026 (Wikipedia "2026 in video games").
