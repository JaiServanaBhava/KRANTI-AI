from flask import Flask, request, jsonify
import os
import pyautogui

app = Flask(__name__)

# -------------------------- HOME -------------------------- #
@app.route("/")
def home():
    return """
  <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kranti AI Remote</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    background: #0d1117;
    color: white;
    font-family: Arial;
    text-align: center;
    padding: 15px;
}

h1 {
    margin-bottom: 10px;
}

button {
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    background: #238636;
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 18px;
}

button.red { background: #f85149; }
button.blue { background: #005cc5; }

#touchpad {
    width: 100%;
    height: 280px;
    background: #161b22;
    border-radius: 14px;
    margin-top: 15px;
    touch-action: none;
    border: 2px solid #30363d;
}

/* ---------------- PIN LOCK SCREEN ---------------- */
#lockscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #0d1117;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

#pinInput {
    padding: 15px;
    font-size: 24px;
    text-align: center;
    width: 160px;
    border-radius: 10px;
    border: none;
    outline: none;
    margin-bottom: 15px;
}

#unlockBtn {
    padding: 12px 20px;
    background: #238636;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 18px;
}
</style>
</head>
<body>

<!-- 🔐 PIN Lock Screen -->
<div id="lockscreen">
    <h2>Enter PIN</h2>
    <input type="password" id="pinInput" maxlength="4" placeholder="••••">
    <button id="unlockBtn">Unlock</button>
    <p id="pinMsg" style="color:red; margin-top:10px;"></p>
</div>


<h1>Kranti AI Remote</h1>

<!-- Mouse Touchpad -->
<h3>Touchpad</h3>
<div id="touchpad"></div>

<!-- Button Controls -->


<button onclick="send('/click')">Left Click</button>
<button onclick="send('/right_click')">Right Click</button>
<button onclick="send('/double_click')">Double Click</button>

<button class="blue" onclick="send('/volume_up')">Volume +</button>
<button class="blue" onclick="send('/volume_down')">Volume -</button>
<button class="blue" onclick="send('/mute')">Mute</button>

<button class="red" onclick="send('/shutdown')">Shutdown</button>
<button class="red" onclick="send('/restart')">Restart</button>
<button class="red" onclick="send('/lock')">Lock</button>

<!-- Keyboard -->
<h3>Keyboard Input</h3>
<input id="kb" type="text" placeholder="Type text here" 
style="width: 90%; padding: 12px; border-radius: 10px;">

<button onclick="typeText()">Send Text</button>

<script>
function send(url) {
    fetch(url)
        .then(r => r.text())
        .then(alert);
}

// Send keyboard text
function typeText() {
    let text = document.getElementById("kb").value;
    fetch(`/type?text=${encodeURIComponent(text)}`);
    alert("Typed on PC: " + text);
}

// ---------------- PIN CHECK ----------------
document.getElementById("unlockBtn").onclick = function() {
    let pin = document.getElementById("pinInput").value;

    if (pin === "2025") {
        document.getElementById("lockscreen").style.display = "none";
    } else {
        document.getElementById("pinMsg").innerText = "Incorrect PIN!";
    }
};

// Touchpad Movement
const pad = document.getElementById("touchpad");
let lastX = 0, lastY = 0;

pad.addEventListener("touchstart", e => {
    lastX = e.touches[0].clientX;
    lastY = e.touches[0].clientY;
});

pad.addEventListener("touchmove", e => {
    e.preventDefault(); 

    let x = e.touches[0].clientX;
    let y = e.touches[0].clientY;

    let dx = x - lastX;
    let dy = y - lastY;

    lastX = x;
    lastY = y;

    fetch(`/move_relative?dx=${dx}&dy=${dy}`);
});



</script>

</body>
</html>


    """

# -------------------------- SYSTEM CONTROL -------------------------- #
@app.route("/shutdown")
def shutdown():
    try:
        os.system("shutdown /s /t 1")
        return "PC is shutting down..."
    except Exception as e:
        return f"Error: {e}"




@app.route("/restart")
def restart():
    try:
        os.system("shutdown /r /t 1")
        return "PC restarting..."
    except Exception as e:
        return f"Error: {e}"

@app.route("/lock")
def lock():
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "PC Locked"
    except Exception as e:
        return f"Error: {e}"

# -------------------------- VOLUME CONTROL -------------------------- #
@app.route("/volume_up")
def volume_up():
    pyautogui.press("volumeup")
    return "Volume Up"

@app.route("/volume_down")
def volume_down():
    pyautogui.press("volumedown")
    return "Volume Down"

@app.route("/mute")
def mute():
    pyautogui.press("volumemute")
    return "Muted"

# -------------------------- MOUSE CONTROL -------------------------- #
@app.route("/move_relative")
def move_relative():
    try:
        dx = float(request.args.get("dx"))
        dy = float(request.args.get("dy"))

        # Faster + smoother movement
        pyautogui.moveRel(dx, dy)

        return f"Mouse moved by {dx},{dy}"
    except Exception as e:
        return f"Error: {e}"



@app.route("/click")
def click():
    pyautogui.click()
    return "Clicked"

@app.route("/right_click")
def right_click():
    pyautogui.rightClick()
    return "Right Clicked"

@app.route("/double_click")
def double_click():
    pyautogui.doubleClick()
    return "Double Clicked"

# -------------------------- KEYBOARD -------------------------- #
@app.route("/type")
def type_text():
    text = request.args.get("text", "")
    pyautogui.typewrite(text)
    return f"Typed: {text}"

@app.route("/press")
def press_key():
    key = request.args.get("key", "")
    pyautogui.press(key)
    return f"Pressed: {key}"

# -------------------------- RUN SERVER -------------------------- #
if __name__ == "__main__":
    print("\n>> Kranti AI Remote Control Server Running...")
    print(">> Open from another device:")
    print("   http://YOUR_PC_IP:5000")
    print("")
    app.run(host="0.0.0.0", port=5000, debug=False)
