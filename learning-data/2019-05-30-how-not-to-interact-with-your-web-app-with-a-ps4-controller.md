---
title: How Not To Interact With Your Web App With A PS4 Controller
summary: Play and experimenting with Web APIs.
date: 2019-05-30
tags: 
  - Javascript
  - Web API
  - Bluetooth API
  - USB API
  - Gamepad API
---
*Published originally on [Medium](https://itnext.io/how-not-to-interact-with-your-web-app-with-a-ps4-controller-a3e3036a2f6e)*

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_01.png)

*Today I’m sharing a facepalm experience that I had while I was trying to get my PS4 controller to work in my browser for a fun personal, yet useless project I’m working on. I’ll be writing another time regarding that project, but let’s now see about a typical facepalm experience that every coder will experience a few times in their career.*

## The Goal

My goal was to hook up a PS4 controller to the browser so I could listen to the events of the controller to interact with the web page. Why a PS4 controller? It just happens I have a PS4, so the first thing in reach was obviously the PS4 controller.

## Attempt 1: The Web Bluetooth API

The simple Idea was to just connect over Bluetooth, the primary way we use the PS4 on our console anyway. There is an experimental API in the browser, and a part of the journey was to experiment and learn new things. So, challenge accepted!

Full of excitement on learning about the Bluetooth protocol I stumbled upon this [Google tutorial](https://developers.google.com/web/updates/2015/07/interact-with-ble-devices-on-the-web#get_disconnected_from_a_bluetooth_device). Seems easy, right? I jumped on the [first article](https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt) I could find on how Bluetooth works so I would understand how to communicate over Bluetooth and connect my PS4 controller via Bluetooth to my local machine. Afterward, I wrote this hello-world attempt to connect over Bluetooth.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<button id="btn">Connect</button>

<script>
    document
        .getElementById('btn')
        .addEventListener('click', async function () {
            try {
                const options = {
                    filters: [
                        {services: [0x1800, 0x180F, 0x181C]}
                    ]
                };
                const device = await navigator.bluetooth.requestDevice(options);
                console.log(device);
            } catch (error) {
                console.log("Something went wrong. " + error);
            }
        });
</script>

</body>
</html>
```

When running this snippet in Chrome I got a popup to connect to a Bluetooth Device.

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_02.png)

Well… That was disappointing. My PS4 controller was properly connected, yet nothing shows up. Why? When I then read the “small” print of the aforementioned Google tutorial:

> It supports communication among devices that implement Bluetooth 4.0 or later.

Apparently, the PS4 controller is Bluetooth v2.1. So hooking up the controller over Bluetooth won’t work out.

**Time Spent**: *1 day (researching Bluetooth and troubleshooting why the controller doesn’t show for the Bluetooth API)*

## Attempt 2: The Web USB API

Bluetooth didn’t work out, so I thought, well, we can also use the USB cable. This must work, right?

Like before, I tried to simply discover the PS4 controller in the browser. It’s important to note that we can only request access to a USB device by a user gesture, like by the click of a button (just like with the Bluetooth API). This is for safety precaution, in addition to that, the web application has to run on HTTPS, although browsers should allow it for localhost. We can access our PS4 controller with the following snippet;

```html
<!DOCTYPE html>
<html lang="en">
<body>

<button id="btn">Connect</button>

<script>
    
    const btn = document.getElementById('btn');

    btn.addEventListener('click', async function onClick() {
        cost device = await navigator.usb.requestDevice({
            filters: [{vendorId: 0x054c, productId: 0x05c4}]
        });
        // Print out the details of our device, being our PS4 Controller
        console.log(device);
    })

</script>

</body>
</html>
```
Let’s break down the script for a moment:

* We have defined a simple button with id `btn`
* We attach an event listener for the `click` event that will request the device based on our filter `{vendorId: 0x054c, productId: 0x05c4}` . (These values don’t come out of thin air, I found the correct values [here](http://www.linux-usb.org/usb.ids))
* We’ll log out the device to the console, just to validate if it worked.

When we preview this in the browser, we can hit the “connect” button and (if your PS4 controller is connected) a popup should arise with the PS4 controller listed. For some reason, the PS4 controller is listed as “Wireless Controller” even when connected over USB, but that’s the name that the vendor gave, so no worries. Anyhow, select the device and click “connect” in the popup.

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_03.png)

If everything went according to plan, we can find our device in the console output. We can verify we have our PS4 controller, inspecting the `manufacturerName` property of our logged USBDevice.

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_04.png)

Perfect! I was able to discover the PS4 controller via USB! Next step is to try to receive data from it. Therefore we need to select a configuration and claim an interface.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<button id="btn">Connect</button>

<script>
    var btn = document.getElementById('btn');
    btn.addEventListener('click', async function () {
        const device = await navigator.usb.requestDevice({
            filters: [{vendorId: 0x054c, productId: 0x05c4}]
        });

        try {
            await device.open();
            await device.selectConfiguration(1);
            await device.claimInterface(0x0);
        } catch (e) {
            console.log(e);
        }
    })
</script>

</body>
</html>
```

When I tested this in the browser I got the following obscure warning:

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_05.png)

After a long (inefficient) google search, I found this [post](https://groups.google.com/a/chromium.org/forum/#!msg/blink-dev/LZXocaeCwDw/GLfAffGLAAAJ). Which states:

> The following set of USB interface classes, which should not be claimed using the WebUSB API, will be explicitly blocked by Blink: Audio, Video, HID, Mass Storage, Smart Card, Wireless Controller (Bluetooth and Wireless USB).

God, our Wireless Controller (although connected over USB) is being blocked because of the specification. Yet another dead end!

**Time Spent**: *2 days (researching USB and troubleshooting the obscure error)*

So it seemed that HID (Human Interface Devices) are blocked from the Web USB API. Apparently, there is also an HID API in the making but still far from properly implemented. But going from one article to another I found out there is…. drumroll

## Attempt 3: The Gamepad API

Yes, can you believe it? There is a [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API) out there! After a detour through the Bluetooth and USB API, there is a straightforward Gamepad API which does (almost) exactly what we want. Comes even with a copy/pasteable [example from the MDN](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API) site.

Here is a naive implementation for the sake of simplicity:

```html{9,13,16,18}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Gamepad Log</title>
</head>
<body>
<h1>Gamepad log</h1>
<pre id="output"></pre>

<script>

    const refreshRate = 100;
    const output = document.getElementById('output');

    setInterval(getGamepadState, refreshRate);

    function getGamepadState() {

        // Returns up to 4 gamepads.
        const gamepads = navigator.getGamepads();

        // We take the first one, for simplicity
        const gamepad = gamepads[0];

        // Escape if no gamepad was found
        if (!gamepad) {
            console.log('No gamepad found.');
            return;
        }

        // Filter out only the buttons which are pressed
        const pressedButtons = gamepad.buttons
            .map((button, id) => ({id, button}))
            .filter(isPressed);

        // Print the pressed buttons to our HTML
        for (const button of pressedButtons) {
            console.log(button);
            log(`Button ${button.id} was pressed.`)
        }

    }

    function isPressed({button: {pressed}}) {
        return !!pressed;
    }

    function log(message) {
        const date = new Date().toISOString();
        output.innerHTML += `${date}: ${message}\n`;
    }

</script>

</body>
</html>
```

If we run this page in the browser (preferably the latest version of Chrome), we get the following output after pressing some buttons on our gamepad:

![PS4 Controller](./assets/how-not-to-interact-with-your-web-app-with-a-ps4-controller_06.png)

Let’s analyze what’s happening here:

* We created on line 9 a container where we want to print out all the buttons that the user has pressed.
* On line 18 we create a function `getGamepadState` which will retrieve all connected gamepads to the browser, pick the first one, and print out whatever buttons are pressed.
* On line 16 we run the `getGamepadState` function at a given interval that we have set on line 13.
* A working example can be found on my [website](https://webapistudio.com/#/gamepad/debugger).

Basically, we retrieve the state of our gamepad at a given interval. The state giving us information on which buttons are pressed, and we print this out on the page. Aside from the buttons, we can also query the state of the gamepad’s axes. When a gamepad has a joystick, the state of our joystick will be available in the `gamepad.axes` property. For a PS4 controller, we have 4 axes. 2 axes for each joystick (left and right one), and each joystick having a state for the x and y-axes.

**For the sake of brevity of the example, I only print the pressed buttons and ignored the axes.**

**Time Spent**: *2 hours (read MDN article and get a working hello world example)*

## Some interesting observations about the Gamepad API

Notice that we “poll” for the state of our gamepad(s) pressed buttons and axes, it is not “event-driven” which is very typical for JS and for DOM events. The challenge with this solution is finding the right “balance” of the interval rate that we run the `getGamepadState` function.

If the interval is too low (e.g 2 seconds) we might “miss out” about the fact that the user pressed a button within that given time interval. When the interval is too high (e.g. 10ms), we will register multiple times that a particular button is pressed. As pressing a button might take much longer (e.g 100ms) than the set interval.

Depending on how we want the user experience to be of our end product, we might desire a more “event-driven” experience (e.g. Do only something once, when a button is pressed, and do not repeat that action till the button was released) or rather a “polling-driven” experience (e.g. Keep moving my character forward as long a button is pressed).

In case we prefer an “event-driven” experience I’d consider to use RxJs. We would then “poll” the state of our gamepad, map the state of each button as an “event” and feed all these self-created events to an RxJs observable. From the observable, we could create a stream that filters these events so that we would pass on events conditionally.

An example: *When we receive an event that says “button 5 is pressed”, filter out all similar events of “button 5 is pressed” until we have received at least one “button 5 is not pressed”. When that happens, allow again a “button 5 is pressed” event to flow through.* I might write a blog post in the near future about this to elaborate, stay tuned!

## How do we know which button is which?

You might have noticed from the code that buttons their ids are just simple indexes values. If you would press one button at a time, you will be able to figure out which index maps to which button on your controller. It is safe to assume that the button indexes are always the same for the same type of gamepad.

The very first button on a PS4 DualShock is the “cross” (aka “X”) button that maps to index 0. On my website [WebApiStudio](https://webapistudio.com/#/gamepad/debugger) you can find a playground to connect your PS4 controller to the web browser, modify the refresh rate interval and check out the button/axes mapping.

## Summary

I went through a long journey (3 days) to only discover that there was already an easy solution (2h) to my problem. With this story, I wanted to show that even the more experienced programmer can lose a lot of time by not doing proper “research” for possible solutions to their problem.

We saw the different angles I looked at and found the Gamepad API which comes with some interesting behavior (being “poll-driven”) that comes with its challenges on how to consume this API based on your use case. We’ll see in another blog post soon how we make fun projects with this API.

As mentioned before, make sure yo check out my website [WebApiStudio](https://webapistudio.com/#/gamepad/debugger) to find a working example, more information and fun projects that I’m working on.

## Used resources

* [PS4 Controller — USB reference](https://www.psdevwiki.com/ps4/DS4-USB)
* [Web USB API introduction](https://developers.google.com/web/updates/2016/03/access-usb-devices-on-the-web) and in a [nutshell](https://www.beyondlogic.org/usbnutshell/usb1.shtml)
* [Web USB API MDN](https://developer.mozilla.org/en-US/docs/Web/API/USB)
* [Web USB API Spec](https://wicg.github.io/webusb/)
* [How the USB protocol works](https://www.beyondlogic.org/usbnutshell/usb3.shtml)
* [USB Id Vendor And Device Id List](http://www.linux-usb.org/usb.ids)
* [USB Spec](https://www.usb.org/)

