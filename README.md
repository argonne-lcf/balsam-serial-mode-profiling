# balsam-serial-mode-profiling
Contains application tools and scripts for measuring balsam performance in serial mode.

# Timing Definitions

For each Job, we will measure the following timestamps:

| Timestamp | Description |
| --------- | ----------- |
| `t_0`     | *Balsam worker start:* the launcher log timestamp immediately before worker Popens the job |
| `t_1`     | *RUNNING database time:* when job recorded as `RUNNING` in database |
| `t_2`     | *Application start:* timestamp emitted by application upon startup |
| `t_3`     | *Application end:* timestamp emitted by application at the end |
| `t_4`     | *Balsam worker end:* the launcher log timestamp immediately after Popen polls return 0 |
| `t_5`     | *RUN_DONE database time* the timestamp when `RUN_DONE` is recorded in database |
| `t_err`     | *Balsam worker error* launcher log timestamp when nonzero return code is polled |

`t3 - t2` is the *inner app runtime*: how long the app takes to run measured purely by the application itself.
This time delta is important in case applications are running intrinsically slower at scale.

`t2 - t0` is the *Popen start delay*: All the time between `t0` and `t2` is spent in Popen; a large delay here
indicates that subprocess `fork()` and `exec()` is taking a long time.

`t4 - t3` is the *Popen end delay*: A large delay here indicates excessive lag time between the application end and when a return code is propagated back to the Popen object.

# First Steps

This is meant to be run on Theta.  First, run the script to build a virtual env for these tests, using the latest balsam serial mode:
```bash
/balsam-installer.sh /path/to/balsam-serial-tests-venv/
```

If you get an error like `fatal: destination path 'mpi4py' already exists and is not an empty directory.` you probably are re-running the script.  It caches and builds in the /tmp area, so remove the folder here:

```bash
rm -r /tmp/$(whoami)/balsam-install
```

Once it completes (it builds mpi4py, it takes a few minutes), you can activate the environment with:
```bash
source /path/to/balsam-serial-tests-venv/bin/activate
```

On future logins, you can set the virtual env and all modules needed with:
```bash
source env_setup.sh /path/to/balsam-serial-tests-venv/
```

## Create a balsam DB:

The balsam database is created and initialized like this:
```bash
balsam init /path/to/balsam-serial-tests-db/
```

Once initialized, activate the database with:
```bash
source balsamactivate /path/to/balsam-serial-tests-db/
```

## Initializing applications

This repo contains several applications:
- Python-based array addition
- Singularity based C++ simulation code
- An empty bash script that sleeps for 60 seconds

You can initialize all of them in your database, once activated, with the script in `applications/initialize_apps.sh`

## Initializing workloads

We plan to scan over workloads as a function of node packing count and job size (n_nodes).  To facilitate sorting these and loading jobs into the DB, several scripts are provided for creating these workflows and their jobs:

```bash
# Add the empty app with 4 nodes, 16 ranks per node:
python workflows/add_workflow_empty_app.py -n 4 -npc 16

# Add the array_add app with 32 nodes, 32 ranks per node:
python workflows/add_workflow_array_add.py -n 32 -npc 32

# Add the cosmics_gen_stage app with 256 nodes, 1 rank per node:
python workflows/add_workflow_cosmics_gen_stage.py -n 256 --node-packing-count 1
```

Each of these apps will produce at the end the correct submit-launch command with balsam, though you may want/need to change the allocation.
