# Trap

## Setup

- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `mkdir faces`


## Run

Start a service with *systemd*. This will start the program when the computer starts and revive it when it dies:

- `mkdir -p ~/.config/systemd/user`
- Paste the contents of `get_faces.service` into `~/.config/systemd/user/get_faces.service`

Start the service using the commands below.

- `systemctl --user daemon-reload`
- `systemctl --user enable get_faces.service`
- `systemctl --user start get_faces.service`

Start it on boot: `sudo loginctl enable-linger pi`

Get the logs: `journalctl --user -u get_faces.service`
