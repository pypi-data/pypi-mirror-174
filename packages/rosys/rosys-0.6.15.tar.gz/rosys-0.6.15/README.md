# RoSys - The Robot System

RoSys provides an easy-to-use robot system.
Its purpose is similar to [ROS](https://www.ros.org/).
But RoSys is fully based on modern web technologies and focusses on mobile robotics.

The full documentation is available at [rosys.io](https://rosys.io/).

## Principles

### All Python

Business logic is written in pure Python.
Computation-heavy tasks are wrapped in processes, accessed through websockets or called via C++ bindings.
Like you would do in any other Python program.

### Modularity

You can structure your code as you please.
RoSys provides it's magic without assuming a specific file structure, config files or enforced naming.

### Async

Thanks to [asyncio](https://docs.python.org/3/library/asyncio.html) you can write your business logic without locks and mutexes.
The execution is [parallel but not concurrent](https://realpython.com/python-concurrency/) which makes it easier to write/read and debug.
In real case scenarios this is also much faster than [ROS](https://www.ros.org/).
Their multiprocessing architecture requires too much inter-process communication.

### Web UI

Most machines need some kind of human interaction.
We made sure your robot can be operated fully off the grid with any web browser by incorporating [NiceGUI](https://nicegui.io/).
It is also possible to proxy the user interface through a gateway for remote operation.

### Simulation

Robot hardware is often slower than your own computer.
To rapidly test out new behavior and algorithms, RoSys provides a simulation mode.
Here, all hardware is mocked and can even be manipulated to test wheel blockages and similar.

### Testing

You can use [pytest](https://docs.pytest.org/) to write high-level integration tests.
It is based on the above-described simulation mode and accelerates the robot's time for super fast execution.

## Architecture and Features

### Modules

RoSys modules are just Python modules which encapsulate certain functionality.
They can hold their own state, register lifecycle hooks, run methods repeatedly and subscribe to or raise [events](#events).
Modules can depend on other modules which is mostly implemented by passing them into the constructor.

### Lifecycle Hooks And Loops

Modules can register functions for being called `on_startup` or `on_shutdown` as well as repeatedly with a given interval with `on_repeat`.

### Events

Modules can provide events to allow connecting otherwise separated modules of the system.
For example on module might read sensor data and raise an event `NEW_SENSOR_DATA`, without knowing of any consumers.
Another module can register on `NEW_SENSOR_DATA` and act accordingly when being called.

### Automations

RoSys provides an `Automator` module for running "automations".
Automations are coroutines that can not only be started and stopped, but also paused and resumed, e.g. using `AutomationControls`.
Have a look at our [Click-and-drive](examples/click-and-drive.md) example.

### Persistence

Modules can register backup and restore methods to read and write their state to disk.

### RoSys Time

If you want to delay the execution, you should invoke `await rosys.sleep(seconds: float)`.
This causes to wait until the _RoSys time_ has elapsed the desired amount of time.
In pytests the RoSys time is simulated and can advance much faster if no CPU-intensive operation is performed.

### Threading And Multiprocessing

RoSys makes extensive use of [async/await](#async) to archive parallelism without threading or multiprocessing.
But not every piece of code you want to integrate is offering an asyncio interface.
Therefore RoSys provides two handy wrappers:

IO-bound:
If you need to read from an external device or use a non-async HTTP library like [requests](https://requests.readthedocs.io/),
you should wrap the code in a function and await it with `await rosys.run.io_bound(...)`.

CPU-bound:
If you need to do some heavy computation and want to spawn another process,
you should wrap the code in a function and await it with `await rosys.run.cpu_bound(...)`.

### Safety

Python (and Linux) is fast enough for most high level logic, but has no realtime guarantees.
Safety-relevant behavior should therefore be put on a suitable microcontroller.
It governs the hardware of the robot and must be able to perform safety actions like triggering emergency hold etc.

We suggest you use an industrial PC with an integrated controller like the [Zauberzeug Robot Brain](https://www.zauberzeug.com/robot-brain.html).
It provides a Linux system to run RoSys, offers AI acceleration via NVidia Jetson and two integrated [ESP32](https://www.espressif.com/en/products/socs/esp32) microcontrollers and six I/O sockets with up to 24 GPIOs for digital I/Os, CAN, RS485, SPI, I2C, etc. It also has two hardware ENABLE switches and one which is controllable via software.

To have flexible configuration for the microcontroller we created another Open Source project called [Lizard](https://lizard.dev/).
It's a domain-specific language interpreted by the microcontroller which enables you to write reactive hardware behavior without recompiling and flashing.

### User Interface

RoSys builds upon the open source project [NiceGUI](https://nicegui.io/) and offers many robot-related UI elements.
NiceGUI is a high-level UI framework for the web.
This means you can write all UI code in Python and the state is automatically reflected in the browser through WebSockets.
See any of our [examples](examples/steering.md).

RoSys can also be used with other user interfaces or interaction models if required, for example a completely app-based control through Bluetooth Low Energy with Flutter.

### Notifications

Modules can notify the user through `rosys.notify('message to the user')`.
When using NiceGUI, the notifications will show as snackbar messages.
The history of notifications is stored in the list `rosys.notifications`.
