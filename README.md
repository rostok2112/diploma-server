# diploma-server
Server for reading, modifying and transfering data from FBT module to SteamVR

---

Server side of [FBT module project](https://github.com/rostok2112/diploma)

Dependencies:
- pipenv


Initialization:

```bash
pipenv sync
cat .env.sample > .env
docker compose up -d
```

Run:

```bash
pipenv run python src/ble_main.py
pipenv run python src/worker_main.py
pipenv run python src/ws_main.py
```

Exit:

`CTRL + C`

Optionally run test web app by opening `src/test_web_app.html`
