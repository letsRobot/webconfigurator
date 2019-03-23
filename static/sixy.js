// get the html objects
const volumeSlider = document.getElementById("volumeSlider");
const speedSlider = document.getElementById("speedSlider");
const tableButton = document.getElementById("tableButton");
const micButton = document.getElementById("micButton");
// value of the objects when the page first loads
let volumeSliderValue = volumeSlider.value;
let speedSliderValue = speedSlider.value;
let tableButtonValue = tableButton.checked;
let micButtonValue = micButton.checked;
// values of various objects are placed here for easy manipulation
const server = 'wss://letsrobot.tv';
const port = '8000';
const sleepTime = '1000';
const robotName = 'sixy';
const robotID = '80459902';
const chatRoom = 'jill';
let commands = []; // array for the command queue
const socket = io.connect(server + ':' + port); // Socket.io connection

/**
 * Get the value of the slider and add it to the command queue.
 */
function setVolume() {
    let str = "vol " + volumeSlider.value;
    commands.push(str);
}

/**
 * Get the value of the slider and add it to the command queue.
 */
function setSpeed() {
    let str = "speed " + speedSlider.value;
    commands.push(str);
}

/**
 * Get the value of the table button and add it to the command queue.
 */
function setTableMode() {
    let str = "table";
    if (tableButton.checked === true) {
        str += " on";
    } else {
        str += " off";
    }
    commands.push(str);
}

/**
 * Get the value of the mic button and add it to the command queue.
 */
function setMicEnabled() {
    let str = "mic";
    if (micButton.checked === true) {
        str += " unmute";
    } else {
        str += " mute";
    }
    commands.push(str);
}

function reboot() {
    derp = confirm("Are you sure you want to reboot?");
    if (derp) {
        sendMessage("reboot");
    }
}

/**
 * dummy delay function
 * @param {Number} ms milliseconds to delay 
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Check values of the objects on the webpage against stored values for deltas
 * and update accordingly. Iterate through updated values and send the commands
 * to the chat.
 */
async function update() {
    if (volumeSlider.value !== volumeSliderValue) {
        setVolume();
        volumeSliderValue = volumeSlider.value;
    }
    if (speedSlider.value !== speedSliderValue) {
        setSpeed();
        speedSliderValue = speedSlider.value;
    }
    if (tableButton.checked !== tableButtonValue) {
        setTableMode();
        tableButtonValue = tableButton.checked;
    }
    if (micButton.checked !== micButtonValue) {
        setMicEnabled();
        micButtonValue = micButton.checked;
    }

    if (commands.length > 0) {
        for (let i = 0; i < commands.length; i++) {
            sendMessage(commands[i]);
            await sleep(sleepTime)
        }
    }
    commands = [];
}

/**
 * Send a message to the chat.
 * @param {String} message 
 */
function sendMessage(message) {
    socket.emit("chat_message", {
        "message": "[" + robotName + "] ." + message,
        "robot_name": robotName,
        "robot_id": robotID,
        "room": chatRoom,
        "secret": "iknowyourelookingatthisthatsfine"
    });
}