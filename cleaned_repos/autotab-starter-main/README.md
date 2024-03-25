# autotab

Welcome to autotab! autotab makes it easy to create auditable browser automations using AI. Go from a point & click demonstration in the browser to live code for those actions in seconds.

> Note: This project is alpha release and actively being developed. Expect breaking changes and exciting new features regularly!
## Usage

### Recording an automation

To record a new automation, run `autotab record`. You can optionally add a `--agent <agent_name>` argument. This will launch a Chrome session controlled by Selenium and then log you in to Google and open the autotab extension in the sidepanel.

If the sidepanel does not open, type `Command - Shift - Y` to open the sidepanel.

Once the sidepanel is open, you can use record mode to record clicks and typing (`Command - E`) or select mode (`Command I`) to select an element to be hovered, copied to clipboard or to inject text into.

At the end of recording make sure to copy all the code. autotab will have created a `<agent_name>.py` file in the `agents/` folder with boilerplate code. Paste the code in there, format it and then your agent is ready to run!

### Running an automation

To play an automation you've already created, run `autotab play --agent <agent_name>`. Leaving out `--agent <agent_name>` has it default to run `agents/agent.py`. This just runs the Python script, so you can set debug as you would any other Python script. Often times interactions fail if the Chrome window running the automation isn't focused. We are working on a headless version that runs in the cloud which we hope to release soon to address this.