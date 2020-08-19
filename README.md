# balsam-serial-mode-profiling
Contains application tools and scripts for measuring balsam performance in serial mode.


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
```
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
